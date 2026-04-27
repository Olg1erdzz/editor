import type { ChatMessage } from "@/types";
import axios from "axios";

export async function chat(messageList: ChatMessage[], apiKey: string) {
  try {
    const result = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "post",
      // signal: AbortSignal.timeout(8000),
      // 开启后到达设定时间会中断流式输出
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        stream: true,
        messages: messageList,
      }),
    });
    return result;
  } catch (error) {
    throw error;
  }
}
export async function RAG(query: string, username: string) {
  const formData = new FormData();
  formData.append('query', query);
  formData.append('username', username);
  try {
    const result = await axios.post("http://127.0.0.1:5000/api/question", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(result);
    return result;
  } catch (error) {
    throw error;
  }
}