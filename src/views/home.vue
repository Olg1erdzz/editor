<template>
  <section class="agent-shell">
    <header class="agent-header">
      <div class="agent-title-block">
        <span class="agent-eyebrow">Agent Workspace</span>
        <div class="agent-title-row">
          <h2>文星 Agent</h2>
          <span class="model-badge" v-if="lastModelLabel">{{ lastModelLabel }}</span>
        </div>
        <p class="agent-subtitle">面向编辑任务的规划、检索、改写和多模态协同工作台。</p>
      </div>

      <div class="agent-toolbar">
        <button type="button" class="toolbar-button" @click="refreshContext" :disabled="isTalking">
          <el-icon><RefreshRight /></el-icon>
          <span>刷新上下文</span>
        </button>
        <button type="button" class="toolbar-button danger" @click="resetAgentWorkspace" :disabled="isTalking">
          <el-icon><Delete /></el-icon>
          <span>清空会话</span>
        </button>
      </div>
    </header>

    <section class="context-band">
      <div class="context-grid">
        <div class="context-metric">
          <span class="metric-label">当前文档</span>
          <strong>{{ activeDocumentTitle }}</strong>
        </div>
        <div class="context-metric">
          <span class="metric-label">知识范围</span>
          <strong>{{ resourceSummary.scopedResources }} 项</strong>
        </div>
        <div class="context-metric">
          <span class="metric-label">向量索引</span>
          <strong>{{ resourceSummary.indexedChunks }} 段</strong>
        </div>
        <div class="context-metric">
          <span class="metric-label">会话标识</span>
          <strong>{{ shortSessionId }}</strong>
        </div>
      </div>

      <div class="resource-strip">
        <span class="resource-chip">
          <el-icon><Files /></el-icon>
          文档 {{ resourceSummary.starredDocuments }}
        </span>
        <span class="resource-chip">
          <el-icon><Picture /></el-icon>
          图片 {{ resourceSummary.starredImages }}
        </span>
        <span class="resource-chip">
          <el-icon><Microphone /></el-icon>
          音频 {{ resourceSummary.starredAudio }}
        </span>
        <span class="resource-chip selection" v-if="selectionPreview">
          <el-icon><Reading /></el-icon>
          选中文本已纳入上下文
        </span>
      </div>

      <div class="selection-band" v-if="selectionPreview">
        <span class="metric-label">当前选中</span>
        <p>{{ selectionPreview }}</p>
      </div>
    </section>

    <section class="quick-band">
      <button v-for="prompt in quickPrompts" :key="prompt.title" type="button" class="quick-action" @click="applyQuickPrompt(prompt.prompt)">
        <span>{{ prompt.title }}</span>
        <small>{{ prompt.helper }}</small>
      </button>
    </section>

    <section class="timeline-band" ref="chatListDom">
      <article v-for="item in messageList" :key="item.id" class="message-row" :class="item.role">
        <div class="message-meta">
          <div class="message-role">
            <span class="role-mark">{{ item.role === "assistant" ? "AG" : "ME" }}</span>
            <div>
              <strong>{{ item.role === "assistant" ? "文星 Agent" : "你" }}</strong>
              <small>{{ formatTimestamp(item.createdAt) }}</small>
            </div>
          </div>

          <div class="message-actions" v-if="item.role === 'assistant' && item.content">
            <button type="button" class="mini-action" @click="insertIntoEditor(item.content)">
              <el-icon><EditPen /></el-icon>
              <span>插入文档</span>
            </button>
          </div>
        </div>

        <div class="message-body">
          <div v-if="item.pending" class="message-loading">
            <Loding />
          </div>
          <div v-else class="markdown-body" v-html="md.render(item.content)"></div>
        </div>

        <div v-if="item.role === 'assistant' && item.steps.length" class="trace-band">
          <h3>执行轨迹</h3>
          <ol>
            <li v-for="(step, index) in item.steps" :key="`${item.id}-${index}`" :class="step.status">
              <span class="trace-index">{{ index + 1 }}</span>
              <div class="trace-copy">
                <strong>{{ toolAlias[step.tool] || step.tool }}</strong>
                <p v-if="step.reason">{{ step.reason }}</p>
                <small v-if="step.outputSummary">{{ step.outputSummary }}</small>
              </div>
            </li>
          </ol>
        </div>

        <details v-if="item.role === 'assistant' && item.sources.length" class="source-band">
          <summary>引用来源 {{ item.sources.length }}</summary>
          <ul>
            <li v-for="(source, index) in item.sources" :key="`${item.id}-source-${index}`">
              <div class="source-headline">
                <strong>{{ source.title }}</strong>
                <span>{{ sourceTypeAlias[source.sourceType] || source.sourceType }}</span>
              </div>
              <p>{{ source.snippet }}</p>
            </li>
          </ul>
        </details>
      </article>
    </section>

    <footer class="composer-band">
      <label class="composer-frame" for="agent-prompt">
        <div class="composer-label">
          <span>任务输入</span>
          <small>Agent 会自动结合当前文档、选中文本和已勾选知识资源。</small>
        </div>
        <textarea id="agent-prompt" v-model="messageContent" class="composer-input" rows="4" placeholder="例如：结合当前文档和我的知识资料，给出下一步写作计划；或把当前选中文本改写成更正式的摘要。" @keydown.enter.exact.prevent="isTalking || sendMessage()"></textarea>
      </label>

      <div class="composer-actions">
        <button type="button" class="send-button ghost" @click="insertSelectionIntoPrompt" :disabled="!selectionPreview || isTalking">
          <el-icon><Position /></el-icon>
          <span>带入选中</span>
        </button>
        <button type="button" class="send-button" @click="sendMessage" :disabled="isTalking || !messageContent.trim()">
          <el-icon><MagicStick /></el-icon>
          <span>{{ isTalking ? "处理中" : "发送给 Agent" }}</span>
        </button>
      </div>
    </footer>
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from "vue";
import { Delete, EditPen, Files, MagicStick, Microphone, Picture, Position, Reading, RefreshRight } from "@element-plus/icons-vue";
import type { Document } from "@/types/types";
import type { AgentChatResult, AgentContextResult, AgentSource, AgentStep } from "./agent/types";
import { clearAgentSession, fetchAgentContext, sendAgentMessage } from "./agent/api";
import { md } from "./libs/markdown";
import Loding from "@/components/Loding.vue";

interface WorkspaceMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: number;
  pending?: boolean;
  steps: AgentStep[];
  sources: AgentSource[];
  model?: string;
  toolModel?: string;
}

const props = defineProps<{
  editor?: any;
  document?: Document | null;
  selectedText?: string;
}>();

const toolAlias: Record<string, string> = {
  search_knowledge_base: "检索知识库",
  search_current_document: "检索当前文档",
  summarize_text: "摘要生成",
  translate_text: "文本翻译",
  rewrite_text: "文风改写"
};

const sourceTypeAlias: Record<string, string> = {
  pdf: "PDF 文档",
  image: "图片 OCR",
  audio: "语音转写",
  current_document: "当前文档"
};

const defaultAssistantCopy = "你好，我是文星 Agent。我会优先结合当前文档、选中文本，以及你在多模态数据中心勾选的资源来规划和回答。";

const messageContent = ref("");
const isTalking = ref(false);
const chatListDom = ref<HTMLDivElement>();
const sessionId = ref<string | null>(null);
const lastModel = ref("");
const lastToolModel = ref("");
const username = ref(localStorage.getItem("userName") || "unknown_user");
const resourceSummary = ref({
  starredDocuments: 0,
  starredImages: 0,
  starredAudio: 0,
  indexedResources: 0,
  indexedChunks: 0,
  scopedResources: 0,
  lastSyncedAt: null as string | null
});

const createAssistantGreeting = (): WorkspaceMessage => ({
  id: `assistant-greeting-${Date.now()}`,
  role: "assistant",
  content: defaultAssistantCopy,
  createdAt: Date.now(),
  steps: [],
  sources: []
});

const messageList = ref<WorkspaceMessage[]>([createAssistantGreeting()]);

const activeDocumentTitle = computed(() => props.document?.title || "未命名文档");
const selectionPreview = computed(() => {
  const value = (props.selectedText || "").trim();
  if (!value) return "";
  return value.length > 140 ? `${value.slice(0, 140)}...` : value;
});

const sessionStorageKey = computed(() => `agent-session:${username.value}:${props.document?.id || props.document?.title || "workspace"}`);
const shortSessionId = computed(() => (sessionId.value ? `${sessionId.value.slice(0, 8)}...` : "未建立"));
const lastModelLabel = computed(() => {
  if (!lastModel.value) return "";
  return lastToolModel.value ? `${lastModel.value} / ${lastToolModel.value}` : lastModel.value;
});

const quickPrompts = computed(() => [
  {
    title: "生成写作计划",
    helper: "围绕当前文档给出下一步执行顺序",
    prompt: `请结合当前文档《${activeDocumentTitle.value}》和我的知识资源，给出一个紧凑的下一步写作计划。`
  },
  {
    title: "检索关联资料",
    helper: "优先从已勾选资源中召回证据",
    prompt: "请先检索我的知识资源，再告诉我哪些内容最适合支持当前文稿。"
  },
  {
    title: "整理当前选中",
    helper: "将选中文本改写成更可直接插入的版本",
    prompt: selectionPreview.value ? `请结合上下文，把当前选中文本整理成更正式、可以直接插入文档的版本：${selectionPreview.value}` : "请结合当前文档内容，生成一段可以直接插入正文的正式表述。"
  }
]);

const clipText = (value: string, limit: number) => (value.length > limit ? value.slice(0, limit) : value);

const getEditorText = () => {
  if (typeof props.editor?.getText === "function") {
    return props.editor.getText();
  }
  if (typeof props.document?.content === "string") {
    return props.document.content;
  }
  return "";
};

const getEditorHtml = () => {
  if (typeof props.editor?.getHTML === "function") {
    return props.editor.getHTML();
  }
  return "";
};

const pushUserMessage = (content: string) => {
  messageList.value.push({
    id: `user-${Date.now()}`,
    role: "user",
    content,
    createdAt: Date.now(),
    steps: [],
    sources: []
  });
};

const pushPendingAssistant = () => {
  messageList.value.push({
    id: `assistant-pending-${Date.now()}`,
    role: "assistant",
    content: "",
    createdAt: Date.now(),
    pending: true,
    steps: [],
    sources: []
  });
};

const replacePendingAssistant = (result: AgentChatResult) => {
  const lastMessage = messageList.value[messageList.value.length - 1];
  if (!lastMessage || lastMessage.role !== "assistant") {
    return;
  }

  lastMessage.pending = false;
  lastMessage.content = result.answer;
  lastMessage.steps = result.steps || [];
  lastMessage.sources = result.sources || [];
  lastMessage.model = result.model;
  lastMessage.toolModel = result.toolModel;
};

const formatTimestamp = (value: number) =>
  new Intl.DateTimeFormat("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
    month: "2-digit",
    day: "2-digit"
  }).format(new Date(value));

const scrollToBottom = () => {
  if (!chatListDom.value) return;
  chatListDom.value.scrollTo({
    top: chatListDom.value.scrollHeight,
    behavior: "smooth"
  });
};

const refreshContext = async () => {
  try {
    const result = (await fetchAgentContext(username.value)) as AgentContextResult;
    resourceSummary.value = result.resourceSummary || resourceSummary.value;
  } catch (error) {
    console.error("Failed to refresh agent context:", error);
  }
};

const sendMessage = async () => {
  const prompt = messageContent.value.trim();
  if (!prompt) return;

  isTalking.value = true;
  pushUserMessage(prompt);
  pushPendingAssistant();
  messageContent.value = "";

  try {
    const result = await sendAgentMessage({
      username: username.value,
      prompt,
      sessionId: sessionId.value,
      documentTitle: activeDocumentTitle.value,
      documentText: clipText(getEditorText(), 12000),
      documentHtml: clipText(getEditorHtml(), 18000),
      selectionText: clipText((props.selectedText || "").trim(), 3000)
    });

    sessionId.value = result.sessionId;
    localStorage.setItem(sessionStorageKey.value, result.sessionId);
    lastModel.value = result.model;
    lastToolModel.value = result.toolModel;
    resourceSummary.value = result.resourceSummary;
    replacePendingAssistant(result);
  } catch (error) {
    const lastMessage = messageList.value[messageList.value.length - 1];
    if (lastMessage && lastMessage.role === "assistant") {
      lastMessage.pending = false;
      lastMessage.content = typeof error === "string" ? error : "Agent 调用失败，请检查后端配置。";
    }
  } finally {
    isTalking.value = false;
  }
};

const insertIntoEditor = (content: string) => {
  if (!props.editor?.chain) {
    return;
  }
  props.editor.chain().focus().insertContent(content).run();
};

const applyQuickPrompt = (prompt: string) => {
  messageContent.value = prompt;
};

const insertSelectionIntoPrompt = () => {
  if (!selectionPreview.value) return;
  messageContent.value = `${messageContent.value.trim()}\n\n当前选中文本：\n${selectionPreview.value}`.trim();
};

const resetAgentWorkspace = async () => {
  try {
    await clearAgentSession(username.value, sessionId.value);
  } catch (error) {
    console.error("Failed to clear session:", error);
  } finally {
    sessionId.value = null;
    localStorage.removeItem(sessionStorageKey.value);
    messageList.value = [createAssistantGreeting()];
    await refreshContext();
  }
};

onMounted(async () => {
  const storedSessionId = localStorage.getItem(sessionStorageKey.value);
  if (storedSessionId) {
    sessionId.value = storedSessionId;
  }
  await refreshContext();
});

watch(
  () => messageList.value.length,
  () => nextTick(scrollToBottom)
);
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");

.agent-shell {
  --agent-shell: #f4efe6;
  --agent-band: rgba(255, 251, 245, 0.92);
  --agent-band-strong: rgba(255, 248, 238, 0.98);
  --agent-ink: #1f2421;
  --agent-muted: #55615b;
  --agent-line: rgba(32, 45, 39, 0.12);
  --agent-accent: #1f7a72;
  --agent-warm: #b4583f;
  --agent-soft: rgba(31, 122, 114, 0.12);
  --agent-soft-warm: rgba(180, 88, 63, 0.14);
  display: grid;
  grid-template-rows: auto auto auto minmax(0, 1fr) auto;
  min-height: calc(100vh - 4rem);
  background: radial-gradient(circle at top right, rgba(31, 122, 114, 0.16), transparent 28%), linear-gradient(180deg, rgba(255, 255, 255, 0.7), rgba(244, 239, 230, 0.96)), var(--agent-shell);
  color: var(--agent-ink);
  font-family: "IBM Plex Sans", "PingFang SC", "Microsoft YaHei", sans-serif;
  overflow: hidden;
}

.agent-header,
.context-band,
.quick-band,
.composer-band {
  position: relative;
  padding: 18px 20px;
  border-bottom: 1px solid var(--agent-line);
  background: var(--agent-band);
}

.agent-header::after,
.context-band::after,
.quick-band::after,
.composer-band::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: linear-gradient(90deg, rgba(31, 122, 114, 0.04) 0, rgba(31, 122, 114, 0.04) 1px, transparent 1px, transparent 24px);
  opacity: 0.18;
  pointer-events: none;
}

.agent-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
}

.agent-eyebrow,
.metric-label,
.composer-label small,
.agent-subtitle,
.message-meta small,
.quick-action small {
  color: var(--agent-muted);
}

.agent-eyebrow,
.metric-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.agent-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.agent-title-block h2 {
  margin: 0;
  font-family: "Fraunces", "Songti SC", serif;
  font-size: 29px;
  font-weight: 700;
  line-height: 1.05;
}

.agent-subtitle {
  margin: 8px 0 0;
  max-width: 34rem;
  font-size: 13px;
  line-height: 1.6;
}

.model-badge,
.resource-chip,
.toolbar-button,
.quick-action,
.mini-action,
.send-button {
  min-height: 36px;
  border-radius: 6px;
  border: 1px solid var(--agent-line);
  background: rgba(255, 255, 255, 0.7);
  color: var(--agent-ink);
  cursor: pointer;
  transition: transform 140ms ease, border-color 140ms ease, background 140ms ease, box-shadow 140ms ease;
}

.model-badge,
.resource-chip {
  display: inline-flex;
  align-items: center;
  padding: 0 10px;
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
}

.model-badge {
  border-color: rgba(31, 122, 114, 0.28);
  background: var(--agent-soft);
  color: var(--agent-accent);
}

.agent-toolbar {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 10px;
}

.toolbar-button,
.send-button,
.mini-action {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0 12px;
  font: inherit;
}

.toolbar-button:hover,
.quick-action:hover,
.mini-action:hover,
.send-button:hover {
  transform: translateY(-1px);
  border-color: rgba(31, 122, 114, 0.34);
  box-shadow: 0 12px 22px -20px rgba(31, 36, 33, 0.9);
}

.toolbar-button.danger,
.send-button.ghost {
  border-color: rgba(180, 88, 63, 0.26);
  background: var(--agent-soft-warm);
  color: var(--agent-warm);
}

.context-band,
.quick-band,
.composer-band {
  display: grid;
  gap: 14px;
}

.context-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.context-metric {
  display: grid;
  gap: 6px;
  padding: 12px 14px;
  border: 1px solid var(--agent-line);
  background: rgba(255, 255, 255, 0.64);
}

.context-metric strong {
  font-size: 15px;
  line-height: 1.4;
}

.resource-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.resource-chip {
  gap: 8px;
}

.resource-chip.selection {
  border-color: rgba(31, 122, 114, 0.28);
  background: var(--agent-soft);
}

.selection-band {
  display: grid;
  gap: 6px;
  padding: 12px 14px;
  border-left: 3px solid var(--agent-accent);
  background: rgba(31, 122, 114, 0.08);
}

.selection-band p {
  margin: 0;
  font-size: 13px;
  line-height: 1.65;
}

.quick-band {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.quick-action {
  display: grid;
  gap: 4px;
  align-content: start;
  padding: 14px;
  text-align: left;
  font: inherit;
}

.quick-action span {
  font-weight: 600;
}

.timeline-band {
  overflow-y: auto;
  padding: 14px 20px 24px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.52), rgba(244, 239, 230, 0.76)), repeating-linear-gradient(180deg, transparent 0, transparent 47px, rgba(31, 122, 114, 0.04) 48px);
}

.message-row {
  display: grid;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid rgba(32, 45, 39, 0.1);
}

.message-row.user {
  border-left: 3px solid rgba(180, 88, 63, 0.62);
  padding-left: 14px;
}

.message-row.assistant {
  border-left: 3px solid rgba(31, 122, 114, 0.62);
  padding-left: 14px;
}

.message-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.message-role {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.message-role strong {
  display: block;
  font-size: 14px;
}

.role-mark {
  display: grid;
  width: 34px;
  height: 34px;
  place-items: center;
  border: 1px solid var(--agent-line);
  background: rgba(255, 255, 255, 0.86);
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
}

.message-actions {
  display: inline-flex;
  gap: 8px;
}

.message-body {
  font-size: 14px;
  line-height: 1.75;
}

.message-loading {
  padding: 8px 0;
}

.markdown-body :deep(p) {
  margin: 0 0 0.9em;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  font-family: "Fraunces", "Songti SC", serif;
  margin: 0.2em 0 0.55em;
}

.markdown-body :deep(code) {
  padding: 0.08rem 0.3rem;
  border-radius: 4px;
  background: rgba(31, 122, 114, 0.08);
  font-family: "IBM Plex Mono", monospace;
}

.trace-band,
.source-band {
  padding: 12px 14px;
  border: 1px solid var(--agent-line);
  background: rgba(255, 255, 255, 0.66);
}

.trace-band h3 {
  margin: 0 0 12px;
  font-family: "Fraunces", "Songti SC", serif;
  font-size: 16px;
}

.trace-band ol,
.source-band ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.trace-band li {
  display: grid;
  grid-template-columns: 28px minmax(0, 1fr);
  gap: 10px;
  padding: 8px 0;
}

.trace-band li + li,
.source-band li + li {
  border-top: 1px solid rgba(32, 45, 39, 0.08);
}

.trace-index {
  display: grid;
  width: 28px;
  height: 28px;
  place-items: center;
  border: 1px solid var(--agent-line);
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
}

.trace-copy {
  display: grid;
  gap: 4px;
}

.trace-copy p,
.trace-copy small,
.source-band p {
  margin: 0;
}

.trace-band li.error .trace-index {
  color: var(--agent-warm);
  border-color: rgba(180, 88, 63, 0.3);
}

.source-band summary {
  cursor: pointer;
  font-family: "IBM Plex Mono", monospace;
  font-size: 12px;
  text-transform: uppercase;
  color: var(--agent-muted);
}

.source-band ul {
  margin-top: 12px;
}

.source-band li {
  padding: 10px 0;
  display: grid;
  gap: 6px;
}

.source-headline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.source-headline strong {
  font-size: 13px;
}

.source-headline span {
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  color: var(--agent-muted);
}

.composer-band {
  background: var(--agent-band-strong);
}

.composer-frame {
  display: grid;
  gap: 10px;
}

.composer-label {
  display: grid;
  gap: 4px;
}

.composer-label span {
  font-weight: 600;
}

.composer-input {
  width: 100%;
  resize: none;
  border: 1px solid var(--agent-line);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.76);
  padding: 14px 15px;
  color: var(--agent-ink);
  font: inherit;
  line-height: 1.65;
  outline: none;
}

.composer-input:focus {
  border-color: rgba(31, 122, 114, 0.36);
  box-shadow: inset 0 0 0 1px rgba(31, 122, 114, 0.14);
}

.composer-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.send-button {
  min-width: 138px;
  justify-content: center;
}

@media (max-width: 1480px) {
  .context-grid,
  .quick-band {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 1080px) {
  .agent-header {
    grid-template-columns: 1fr;
  }

  .context-grid,
  .quick-band {
    grid-template-columns: 1fr;
  }

  .composer-actions {
    flex-direction: column;
  }

  .send-button {
    width: 100%;
  }
}
</style>
