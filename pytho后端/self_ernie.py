import torch
from transformers import BertForSequenceClassification, AdamW, BertTokenizer, BertModel, AutoTokenizer, ErnieModel
from sklearn.semi_supervised import SelfTrainingClassifier
from sklearn.base import BaseEstimator, ClassifierMixin
import pandas as pd
import numpy as np
from torch.nn import functional as F
from sklearn.metrics import accuracy_score, recall_score, f1_score
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader
from torch.cuda.amp import GradScaler, autocast
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

device = torch.device('cuda')


class MyDataset(torch.utils.data.Dataset):
    def __init__(self, data, targets):
        self.data = data
        self.targets = targets

    def __getitem__(self, index):
        x = self.data[index]
        if self.targets is not None:
            y = self.targets[index]
            return x, y
        else:
            return x

    def __len__(self):
        return len(self.data)


def collate_fn(batch):
    data, targets = zip(*batch)
    data = pad_sequence(data, batch_first=True)
    targets = torch.stack(targets)
    return data, targets


class ErnieClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, model_name='nghuyong/ernie-3.0-base-zh', num_labels=8, epochs=3):
        self.model_name = model_name
        self.num_labels = num_labels
        self.epochs = epochs
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.optimizer = AdamW(self.model.parameters(), lr=1e-5)
        self.scaler = GradScaler()

    def fit(self, loader,val_loader):
        self.model.train()
        for epoch in range(self.epochs):
            for inputs, labels in loader:
                inputs, labels = inputs.to(device), labels.to(device)
                inputs = inputs.squeeze()
                attention_mask = (inputs != 0).long()
                with autocast():
                    outputs = self.model(inputs, attention_mask=attention_mask, labels=labels)
                    loss = outputs.loss
                self.scaler.scale(loss).backward()
                self.scaler.step(self.optimizer)
                self.scaler.update()
                self.optimizer.zero_grad()
                # 在每个epoch后进行验证
            self.model.eval()
            val_loss = 0
            with torch.no_grad():
                for inputs, labels in val_loader:
                    inputs, labels = inputs.to(device), labels.to(device)
                    inputs = inputs.squeeze()
                    attention_mask = (inputs != 0).long()
                    outputs = self.model(inputs, attention_mask=attention_mask, labels=labels)
                    loss = outputs.loss
                    val_loss += loss.item()
            print(f'Validation Loss at epoch {epoch}: {val_loss / len(val_loader)}')
            accuracy, precision, recall, f1 = self.evaluate(val_loader)
            print(f'Epoch: {epoch}, Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}')

            # 在每个epoch后保存模型
            save_model = input("Do you want to save the model? (yes/no): ")
            if save_model.lower() == 'yes':
                torch.save(self.model.state_dict(), f'base_classifier_epoch_{epoch}.pth')

        return self

    def predict(self, loader):
        self.model.eval()
        predictions = []
        with torch.no_grad():
            for inputs, _ in loader:
                inputs = inputs.to(device)
                inputs = inputs.squeeze()
                attention_mask = (inputs != 0).long()
                outputs = self.model(inputs, attention_mask=attention_mask)
                prediction = torch.argmax(outputs.logits, dim=-1).cpu().numpy()
                predictions.extend(prediction)
        return predictions

    def evaluate(self, loader):  # 添加了一个新的方法来进行模型评估
        self.model.eval()
        predictions = []
        true_labels = []
        with torch.no_grad():
            for inputs, labels in loader:
                inputs, labels = inputs.to(device), labels.to(device)
                inputs = inputs.squeeze()
                attention_mask = (inputs != 0).long()
                outputs = self.model(inputs, attention_mask=attention_mask)
                prediction = torch.argmax(outputs.logits, dim=-1).cpu().numpy()
                predictions.extend(prediction)
                true_labels.extend(labels.cpu().numpy())
        accuracy = accuracy_score(true_labels, predictions)
        precision = precision_score(true_labels, predictions, average='macro')
        recall = recall_score(true_labels, predictions, average='macro')
        f1 = f1_score(true_labels, predictions, average='macro')
        return accuracy, precision, recall, f1


# 加载预训练的BERT模型和分词器
tokenizer = AutoTokenizer.from_pretrained("nghuyong/ernie-3.0-base-zh")

# 读取标注的数据
labeled_data = pd.read_csv('data.csv', encoding='gbk')
X_labeled = labeled_data['text']
y_labeled = labeled_data['label']

# 将标注的文本转换为词索引
X_labeled_indices = []
for text in X_labeled:
    inputs = tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=510,
                       add_special_tokens=True)
    input_ids = torch.tensor(inputs['input_ids']).unsqueeze(0)
    X_labeled_indices.append(input_ids)
X_labeled_indices = torch.cat(X_labeled_indices, dim=0)

# 对标签进行编码
label_to_id = {'Title': 0,  'Body': 1, 'Heading 1': 2, 'Heading 2': 3, 'Heading 3': 4, 'Quote': 5, 'Directory': 6, 'Abstract': 7, }  # 这里应该包含所有的标签
y_labeled = torch.tensor([label_to_id[label] for label in y_labeled])

unlabeled_data = pd.read_csv('output.csv', encoding='gbk')
X_unlabeled = unlabeled_data['text']
X_unlabeled_indices = []
for text in X_unlabeled:
    inputs = tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=510,
                       add_special_tokens=True)
    input_ids = torch.tensor(inputs['input_ids']).unsqueeze(0)
    X_unlabeled_indices.append(input_ids)
X_unlabeled_indices = torch.cat(X_unlabeled_indices, dim=0)
# 对于无标签的数据，使用-1作为标签
y_unlabeled = torch.full((len(X_unlabeled_indices),), -1)

X = torch.cat([X_labeled_indices, X_unlabeled_indices], dim=0)
y = torch.cat([y_labeled, y_unlabeled])

# 创建基分类器
base_classifier = ErnieClassifier(epochs=30)

base_classifier.model.load_state_dict(torch.load('base_classifier_epoch_12.pth'))

test_data = MyDataset(X_unlabeled_indices, y_unlabeled)
test_loader = DataLoader(test_data, batch_size=16, collate_fn=collate_fn)

result = base_classifier.predict(test_loader)
for text, predict in zip(X_unlabeled, result):
    print(text)
    print(predict)