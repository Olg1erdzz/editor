<template>
    <div class="flex flex-col h-[80%] pt-11">
  
      <div class="flex-1 ml-5 mt-10 mb-2  overflow-y-auto whitespace-normal overflow-auto scrollbar-hide" ref="chatListDom">
        <div
          class="group flex flex-col px-4 py-3 hover:bg-slate-100 rounded-lg"
          v-for="item of messageList.filter((v) => v.role !== 'system')"
        >
          <div class="flex justify-between items-center mb-2">
            <div class="font-bold">{{ roleAlias[item.role] }}：</div>
            <Copy class="invisible group-hover:visible" :content="item.content" />
          </div>
          <div>
            <div
              class="prose text-sm text-slate-600 leading-relaxed"
              v-if="item.content"
              v-html="md.render(item.content)"
            ></div>
            <Loding v-else />
          </div>
        </div>
      </div>
  
      <div class="absolute -bottom-28 -right-9 w-full p-6 pb-8 bg-gray-100 rounded-lg">
        <div class="-mt-2 mb-2 text-sm text-gray-500" v-if="isConfig">
          请输入 API Key：
        </div>
        <div class="flex">
          <input
            class="input"
            :type="isConfig ? 'password' : 'text'"
            :placeholder="isConfig ? 'sk-xxxxxxxxxx' : '请输入'"
            v-model="messageContent"
            @keydown.enter="isTalking || sendOrSave()"
          />
          <button class="btn ml-5" :disabled="isTalking" @click="sendOrSave()">
            {{ isConfig ? "保存" : "发送" }}
          </button>
          <button class="btn ml-5" :disabled="isTalking" @click="clearChatHistory()">
            {{ isConfig ? "保存" : "清除" }}
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import type { ChatMessage } from "@/types";
  import { ref, watch, nextTick, onMounted } from "vue";
  import { chat, RAG } from "./libs/gpt";
  import cryptoJS from "crypto-js";
  import Loding from "@/components/Loding.vue";
  import Copy from "@/components/Copy.vue";
  import { md } from "./libs/markdown";
  import axios from "axios";

  let apiKey = "";
  let isConfig = ref(false);
  let isTalking = ref(false);
  let messageContent = ref("");
  const chatListDom = ref<HTMLDivElement>();
  const decoder = new TextDecoder("utf-8");
  const roleAlias = { user: "ME", assistant: "文星助手", system: "System" };
  const messageList = ref<ChatMessage[]>([
    {
      role: "system",
      content: "你是 ChatGPT，OpenAI 训练的大型语言模型，尽可能简洁地回答。",
    },
    {
      role: "assistant",
      content: `你好，我是文星小助手文星星~，我可以为你提供专属于您定制的检索增强服务以及一些常用的信息，下面是如何进行专属知识库构建的步骤：
  
  1. 上传图片：我可以将上传的图片进行识别，加入到您的多模态数据中心中。
  
  2. 进行录音：在您听专业讲座或者网课时，您可以将这些录音进行转文本，加入多模态数据中心。
  
  3. 上传电子文档：可以上传您需要了解的论文或者电子书以pdf的形式上传给我，并且加入到多模态数据中心。
  
  最后，您可以在数据中心中选择需要加入到知识库中的数据，我可以进行快速的学习并与你交流里面的内容~。`,
    },
  ]);
  
  onMounted(() => {
    if (getAPIKey()) {
      switchConfigStatus();
    }
  });
  
  const sendChatMessage = async (content: string = messageContent.value) => {
    console.log(content);
    try {
      isTalking.value = true;
      if (messageList.value.length === 2) {
        messageList.value.pop();
      }
      messageList.value.push({ role: "user", content });
      clearMessageContent();
      messageList.value.push({ role: "assistant", content: "" });
      
      const username = localStorage.getItem("userName") || "unknown_user"; 

      const response = await RAG(content, username); // replace "username" with actual username
      console.log(response);
      if (true) {
        appendLastMessageContent(response);
      }
    } catch (error: any) {
      appendLastMessageContent(error);
    } finally {
      isTalking.value = false;
    }
  };
  
  const readStream = async (
    reader: ReadableStreamDefaultReader<Uint8Array>,
    status: number
  ) => {
    let partialLine = "";
  
    while (true) {
      // eslint-disable-next-line no-await-in-loop
      const { value, done } = await reader.read();
      if (done) break;
  
      const decodedText = decoder.decode(value, { stream: true });
  
      if (status !== 200) {
        const json = JSON.parse(decodedText); // start with "data: "
        const content = json.error.message ?? decodedText;
        appendLastMessageContent(content);
        return;
      }
  
      const chunk = partialLine + decodedText;
      const newLines = chunk.split(/\r?\n/);
  
      partialLine = newLines.pop() ?? "";
  
      for (const line of newLines) {
        if (line.length === 0) continue; // ignore empty message
        if (line.startsWith(":")) continue; // ignore sse comment message
        if (line === "data: [DONE]") return; //
  
        const json = JSON.parse(line.substring(6)); // start with "data: "
        const content =
          status === 200
            ? json.choices[0].delta.content ?? ""
            : json.error.message;
        appendLastMessageContent(content);
      }
    }
  };
  
  const appendLastMessageContent = (content: string) =>
    (messageList.value[messageList.value.length - 1].content += content);
  
  const sendOrSave = () => {
    if (!messageContent.value.length) return;
    if (isConfig.value) {
      if (saveAPIKey(messageContent.value.trim())) {
        switchConfigStatus();
      }
      clearMessageContent();
    } else {
      sendChatMessage();
    }
  };
  
  const clearChatHistory = async () => {
    const username = localStorage.getItem("userName") || "unknown_user";
    if (messageList.value.length > 1) {
      messageList.value = [
        {
          role: "system",
          content: "你是 ChatGPT，OpenAI 训练的大型语言模型，尽可能简洁地回答。",
        },
        {
          role: "assistant",
          content: `你好，我是文星小助手文星星~，我可以为你提供专属于您定制的检索增强服务以及一些常用的信息，下面是如何进行专属知识库构建的步骤：
      
          1. 上传图片：我可以将上传的图片进行识别，加入到您的多模态数据中心中。
      
          2. 进行录音：在您听专业讲座或者网课时，您可以将这些录音进行转文本，加入多模态数据中心。
      
          3. 上传电子文档：可以上传您需要了解的论文或者电子书以pdf的形式上传给我，并且加入到多模态数据中心。
      
          最后，您可以在数据中心中选择需要加入到知识库中的数据，我可以进行快速的学习并与你交流里面的内容~。`,
        },
      ];

      try {
        const response = await axios.get('http://127.0.0.1:5000/api/question_clear', {
          params: {
            username: username
          }
        });
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }
  };

  const clickConfig = () => {
    if (!isConfig.value) {
      messageContent.value = getAPIKey();
    } else {
      clearMessageContent();
    }
    switchConfigStatus();
  };
  
  const getSecretKey = () => "lianginx";
  
  const saveAPIKey = (apiKey: string) => {
    if (apiKey.slice(0, 3) !== "sk-" || apiKey.length !== 51) {
      alert("API Key 错误，请检查后重新输入！");
      return false;
    }
    const aesAPIKey = cryptoJS.AES.encrypt(apiKey, getSecretKey()).toString();
    localStorage.setItem("apiKey", aesAPIKey);
    return true;
  };
  
  const getAPIKey = () => {
    if (apiKey) return apiKey;
    const aesAPIKey = localStorage.getItem("apiKey") ?? "";
    apiKey = cryptoJS.AES.decrypt(aesAPIKey, getSecretKey()).toString(
      cryptoJS.enc.Utf8
    );
    return apiKey;
  };
  
  const switchConfigStatus = () => (isConfig.value = !isConfig.value);
  
  const clearMessageContent = () => (messageContent.value = "");
  
  const scrollToBottom = () => {
    if (!chatListDom.value) return;
    scrollTo(0, chatListDom.value.scrollHeight);
  };
  
  watch(messageList.value, () => nextTick(() => scrollToBottom()));
  </script>
  
  <style scoped>
  pre {
    font-family: -apple-system, "Noto Sans", "Helvetica Neue", Helvetica,
      "Nimbus Sans L", Arial, "Liberation Sans", "PingFang SC", "Hiragino Sans GB",
      "Noto Sans CJK SC", "Source Han Sans SC", "Source Han Sans CN",
      "Microsoft YaHei", "Wenquanyi Micro Hei", "WenQuanYi Zen Hei", "ST Heiti",
      SimHei, "WenQuanYi Zen Hei Sharp", sans-serif;
  }
  </style>
  