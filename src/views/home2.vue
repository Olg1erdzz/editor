<script lang="ts">
import { defineComponent, ref, watch, nextTick, onMounted } from "vue";
import type { ChatMessage } from "@/types";
import { chat, RAG } from "./libs/gpt";
import cryptoJS from "crypto-js";
import Loding from "@/components/Loding.vue";
import Copy from "@/components/Copy.vue";
import { md } from "./libs/markdown";

export default defineComponent({
components: {
  Loding,
  Copy
},
props: {
  document: {
    type: Object,
    required: true
  },
},
setup() {
  let apiKey = "";
  let isConfig = ref(true);
  let isTalking = ref(false);
  let messageContent = ref("");
  const chatListDom = ref<HTMLDivElement>();
  const decoder = new TextDecoder("utf-8");
  const roleAlias = { user: "ME", assistant: "ChatGPT", system: "System" };
  const messageList = ref<ChatMessage[]>([
    {
      role: "system",
      content: "你是 ChatGPT，OpenAI 训练的大型语言模型，尽可能简洁地回答。",
    },
    {
      role: "assistant",
      content: `你好，我是AI语言模型，我可以提供一些常用服务和信息，例如：

  1. 翻译：我可以把中文翻译成英文，英文翻译成中文，还有其他一些语言翻译，比如法语、日语、西班牙语等。

  2. 咨询服务：如果你有任何问题需要咨询，例如健康、法律、投资等方面，我可以尽可能为你提供帮助。

  3. 闲聊：如果你感到寂寞或无聊，我们可以聊一些有趣的话题，以减轻你的压力。

  请告诉我你需要哪方面的帮助，我会根据你的需求给你提供相应的信息和建议。`,
    },
  ]);

  onMounted(() => {
    if (getAPIKey()) {
      switchConfigStatus();
    }
  });

  // ... 其他函数和方法
  const sendChatMessage = async (content: string = messageContent.value) => {
    try {
      isTalking.value = true;
      if (messageList.value.length === 2) {
        messageList.value.pop();
      }
      messageList.value.push({ role: "user", content });
      clearMessageContent();
      messageList.value.push({ role: "assistant", content: "" });

      const { data, status } = await RAG([{ role: "user", content }], "username"); // replace "username" with actual username
      if (data) {
        const content = data.response ?? ""; // replace "response" with actual key in the response object
        appendLastMessageContent(content);
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
      return {
        isConfig,
        isTalking,
        messageContent,
        chatListDom,
        roleAlias,
        messageList,
        sendOrSave,
        clickConfig
      };
    },
  });
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
