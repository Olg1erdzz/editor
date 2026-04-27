import torch
from PyPDF2 import PdfReader
import os
import uuid
from transformers import AutoTokenizer, ErnieModel
import textwrap
import gc
from docx import Document
import jieba.analyse
import requests
import re
import jieba
import pdfplumber as ppl
from paddlespeech.cli.asr.infer import ASRExecutor
from paddlenlp import Taskflow


# 加载预训练的ERNIE模型和分词器
tokenizer = AutoTokenizer.from_pretrained("knowledge/models--nghuyong--ernie-3.0-base-zh/snapshots/8ad12310fa2e9668f9df5dd15e3857e374ab8147")
model = ErnieModel.from_pretrained("knowledge/models--nghuyong--ernie-3.0-base-zh/snapshots/8ad12310fa2e9668f9df5dd15e3857e374ab8147")


def extract_keywords(text, topK=10):
    # 使用jieba的textrank方法提取关键词
    keywords = jieba.analyse.textrank(text, topK=topK)
    return keywords


def process_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def process_docx(docx_file):
    doc = Document(docx_file)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    return text


def process_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def pdfReader(file):
    pdf = ppl.open(file)
    texts = []
    for page in pdf.pages:
        text = page.extract_text()
        texts.append(text)
    txt_string = ''.join(texts)
    file_extension = 'txt'
    unique_filename = str(uuid.uuid4()) + '.' + file_extension  # 使用UUID生成唯一的文件名
    file_path = os.path.join('knowledge/pdf', unique_filename)
    file_path = file_path.replace('\\', '/')
    with open(file_path, 'w') as f:
        f.write(txt_string)
    return file_path


# def to_knowledge(text):
#     chunks = chunk_text(text, 510)  # 分割文本
#     text_vectors = []
#     keywords_list = []
#     for chunk in chunks:  # 对每个文本块进行分词
#         inputs = tokenizer(chunk, return_tensors='pt', padding='max_length', truncation=True, max_length=510,
#                            add_special_tokens=True)
#         input_ids = inputs['input_ids']
#         # 将词索引转换为词向量
#         attention_mask = inputs['attention_mask']
#         chunk_vectors = model(input_ids, attention_mask=attention_mask)['last_hidden_state']
#         chunk_vectors = chunk_vectors.half()
#         text_vectors.append(chunk_vectors)
#
#         keywords = extract_keywords(chunk)  # 提取关键词
#         keywords_list.append(keywords)
#
#         # 释放不再需要的变量
#         del inputs, input_ids, attention_mask, chunk_vectors, chunk
#         gc.collect()  # 强制进行垃圾回收
#     file_extension = 'pt'
#     unique_filename = str(uuid.uuid4()) + '.' + file_extension
#
#     vector_file_path = os.path.join('knowledge', unique_filename)
#     torch.save((text_vectors, keywords_list), vector_file_path)  # 使用 torch.save() 保存张量)
#     return vector_file_path


def to_knowledge(text):
    sentences = re.split('。|？|！', text)
    print(sentences)
    sentence_vectors = []
    for sentence in sentences:  # 对每个句子进行向量化
        inputs = tokenizer(sentence, return_tensors='pt', padding='max_length', truncation=True, max_length=510,
                           add_special_tokens=True)
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']
        sentence_vector = model(input_ids, attention_mask=attention_mask)['last_hidden_state']
        sentence_vector = sentence_vector.half()
        sentence_vectors.append(sentence_vector)
        print(sentence_vector)
        # 释放不再需要的变量
        del inputs, input_ids, attention_mask, sentence_vector, sentence
        gc.collect()  # 强制进行垃圾回收
    file_extension = 'pt'
    unique_filename = str(uuid.uuid4()) + '.' + file_extension

    vector_file_path = os.path.join('knowledge', unique_filename)
    torch.save((sentence_vectors, sentences), vector_file_path)  # 使用 torch.save() 保存张量)
    return vector_file_path

#
# def to_knowledge(text):
#     sentences = re.split('。|？|！', text)
#     print(sentences)
#     # 对每个句子进行分词，并将分词结果存储为一个字符串
#     sentences_words = [' '.join(jieba.lcut(sentence)) for sentence in sentences]
#     print(sentences_words)
#     file_extension = 'txt'
#     unique_filename = str(uuid.uuid4()) + '.' + file_extension
#     vector_file_path = os.path.join('knowledge', unique_filename)
#     with open(vector_file_path, 'w', encoding='utf-8') as f:
#         for sentence, words in zip(sentences, sentences_words):
#             f.write(sentence)
#             f.write(words)
#     return vector_file_path


def chunk_text(text, max_length):
    return textwrap.wrap(text, max_length)


# def generate_prompt(query, vector_file_path):
#     text_vectors, keywords_list = torch.load(vector_file_path)  # 读取文件
#     query_embedding = model(**tokenizer(query, return_tensors='pt'))[0]
#     similarities = []
#     for text_vector in text_vectors:
#         # 对文本块中的所有词向量取平均
#         text_vector_avg = text_vector.mean(dim=1)
#         similarity = torch.cosine_similarity(query_embedding, text_vector_avg.unsqueeze(0), dim=-1)
#         similarities.append(similarity.mean().item())
#     most_similar_index = torch.argmax(torch.tensor(similarities))
#     most_similar_keywords = keywords_list[most_similar_index]
#     print(similarities, most_similar_index, most_similar_keywords)
#     prompt = "你配置了一个RAG知识库，现在请根据以下内容：" + "，".join(most_similar_keywords) + "，生成专业的回答。"
#     print(prompt)
#     return prompt


def generate_prompt(query, vector_file_path):
    sentence_vectors, sentences = torch.load(vector_file_path)  # 读取文件
    query_embedding = model(**tokenizer(query, return_tensors='pt'))[0]
    similarities = []
    for sentence_vector in sentence_vectors:
        # 对文本块中的所有词向量取平均
        sentence_vector_avg = sentence_vector.mean(dim=1)
        similarity = torch.cosine_similarity(query_embedding, sentence_vector_avg.unsqueeze(0), dim=-1)
        similarities.append(similarity.mean().item())
    most_similar_index = torch.argmax(torch.tensor(similarities))
    most_similar_sentence = sentences[most_similar_index]
    print(similarities, most_similar_index, most_similar_sentence)
    prompt = "你配置了一个RAG知识库，现在请根据以下句子：" + most_similar_sentence + "。\n生成专业的回答。"
    print(prompt)
    return prompt


# def generate_prompt(query, files_path):
#     # 对查询进行分词
#     query_words = jieba.lcut(query)
#     # 从文件中读取句子和分词结果
#     relevant_sentences = []
#     print(files_path)
#     for file_path in files_path:
#         print(file_path[0])
#         with open(file_path[0], 'r', encoding='utf-8') as f:
#             lines = f.readlines()
#         sentences = lines[1::2]  # 原始句子在奇数行
#         # sentences_words = [line.split() for line in lines[::2]]  # 分词结果在偶数行
#         #
#         # # 提取包含查询关键词的句子，以及它们的上下文
#         # for i, words in enumerate(sentences_words):
#         #     if any(word in words for word in query_words):
#         #         # 获取当前句子以及前后各一句
#         #         context = sentences[max(0, i - 1):min(i + 2, len(sentences))]
#         #         relevant_sentences.extend(context)
#
#     # prompt = "你是一个配置了RAG知识库的AI助手，现在请根据以下句子：" + '。'.join(
#     #     sentence.strip() for sentence in relevant_sentences if sentence.strip()) + "。\n生成专业的回答。"
#     print(sentences)
#     prompt = "你是一个配置了RAG知识库的AI助手，现在请根据以下内容：" + '。'.join(sentence.strip() for sentence in sentences if sentence.strip()) + "。\n生成专业的回答。"
#     print(prompt)
#     return prompt