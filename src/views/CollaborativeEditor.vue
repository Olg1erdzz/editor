<template>
  <section class="collab-shell">
    <header class="collab-bar">
      <div class="collab-summary">
        <span class="collab-status" :class="{ active: isCollaborating }"></span>
        <div>
          <strong>协同空间</strong>
          <small>{{ userLenth.length }} 人在线</small>
        </div>
      </div>

      <div class="collab-avatars" aria-label="在线用户">
        <span
          v-for="(item, index) in user"
          :key="`${item.name}-${index}`"
          class="collab-avatar"
          :title="item.name"
          :style="{ '--collab-color': item.color || '#2b3775' }"
        >
          {{ getInitial(item.name) }}
        </span>
        <span v-if="user.length === 0" class="collab-empty">等待协作者</span>
      </div>

      <div class="collab-actions">
        <span v-if="shareCode" class="share-code">分享码 {{ shareCode }}</span>
        <button type="button" class="shell-button primary" @click="toggleCollaboration">
          {{ isCollaborating ? "关闭协同" : "开始协同" }}
        </button>
        <button type="button" class="shell-button" @click="openModal">加入协同</button>
      </div>

      <form v-if="showModal" class="join-panel" @submit.prevent="joinCollaboration">
        <input v-model="inputShareCode" type="text" placeholder="请输入分享码" />
        <button type="submit">确定</button>
        <button type="button" @click="closeModal">取消</button>
      </form>
    </header>

    <CassieEditor
      :user="currentUser"
      footer-height="50"
      :body-width="w"
      :body-height="h"
      :content="pageContentHtml"
      :is-paging="false"
      @onCreate="onCreate"
      :collaboration-url="url"
      @onStatus="onStatus"
      @onAwarenessChange="onAwarenessChange"
      @onUpdate="onUpdate"
      :bodyWidth="750"
      :menu-list="menulist"
      :header-data="headerlist"
      :footer-data="footerlist"
    />
  </section>
</template>

<script lang="ts">
import CassieEditor from "../components/CassieEditor.vue";
import { pageContentHtml, headerlist, footerlist } from "./content";
import { getRandomColor } from "@/denoutils";
import { UnitConversion } from "@/extension/page/core";
import * as Y from "yjs";
import { TiptapCollabProvider } from "@hocuspocus/provider";
import axios from "axios";

const unitConversion = new UnitConversion();
export default {
  components: { CassieEditor },
  data() {
    return {
      isCollaborating: false,
      showModal: false,
      inputShareCode: "",
      shareCode: "",
      userLenth: [],
      user: [],
      currentUser: {
        name: localStorage.getItem("userName") || "协作者",
        color: getRandomColor()
      },
      url: "ws://39.101.177.50:1234",
      w: unitConversion.mmConversionPx(210),
      h: unitConversion.mmConversionPx(297),
      menulist: [
        { classify: "radio", label: "单选", value: "radio" },
        { classify: "checkbox", label: "多选", value: "checkbox" },
        { classify: "date", label: "日期", value: "date" }
      ],
      ydocA: new Y.Doc(),
      providerA: null
    };
  },
  methods: {
    getInitial(name: string) {
      return (name || "协").slice(0, 1).toUpperCase();
    },
    toggleCollaboration() {
      this.isCollaborating = !this.isCollaborating;

      if (this.isCollaborating) {
        this.shareCode = Math.random().toString(36).substring(2, 15);
        const color = this.currentUser.color;
        const username = this.currentUser.name;
        axios.post("http://127.0.0.1:5000/api/start-collaboration", { shareCode: this.shareCode, username, color });
        // 创建 TiptapCollabProvider 实例
        this.ydocA = new Y.Doc();
        this.providerA = new TiptapCollabProvider({
          appId: "JKV0ED9X",
          name: this.shareCode,
          document: this.ydocA
        });
      } else {
        axios.post("http://127.0.0.1:5000/api/close-collaboration", { shareCode: this.shareCode });
        if (this.providerA) {
          this.providerA.destroy();
          this.providerA = null;
          this.ydocA = null;
        }
        this.shareCode = "";
      }
    },
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    joinCollaboration() {
      const shareCode = this.inputShareCode.trim();
      if (!shareCode) return;
      if (this.providerA) {
        this.providerA.destroy();
        this.providerA = null;
        this.ydocA = null;
      }
      const username = this.currentUser.name;
      const color = this.currentUser.color;
      axios.post("http://127.0.0.1:5000/api/join-collaboration", { shareCode, username, color });
      this.shareCode = shareCode;
      this.isCollaborating = true;
      this.showModal = false;
      this.ydocA = new Y.Doc();
      this.providerA = new TiptapCollabProvider({
        appId: "JKV0ED9X",
        name: shareCode,
        document: this.ydocA
      });
    },

    quitCollaboration() {
      if (this.providerA) {
        this.providerA.destroy();
        this.providerA = null;
        this.ydocA = null;
      }
      this.isCollaborating = false;
      this.shareCode = "";
      this.showModal = false;
    },
    onUpdate(output, editor) {},
    onStatus(data, editor) {},
    onCreate(option) {
      console.log(option);
    },
    onAwarenessChange(data) {
      console.log(this.shareCode);
      axios
        .get("http://127.0.0.1:5000/api/get-users", {
          params: {
            shareCode: this.shareCode
          }
        })
        .then((response) => {
          const users = response.data?.user || (response as any).user || [];
          this.userLenth = Array.isArray(users) ? users.flat() : [];
          this.user = this.userLenth.map((item) => {
            return { name: item.username, color: item.color };
          });
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }
};
</script>
<style scoped>
.collab-shell {
  min-height: calc(100vh - 4rem);
  background: rgb(var(--wx-workspace-bg));
}

.collab-bar {
  position: sticky;
  top: 4rem;
  z-index: 55;
  display: grid;
  grid-template-columns: auto minmax(120px, 1fr) auto;
  align-items: center;
  gap: 18px;
  padding: 12px 28px;
  border-bottom: 1px solid rgba(var(--wx-workspace-border), 0.72);
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 16px 36px -34px rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(18px);
}

.collab-summary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.collab-summary div {
  display: grid;
  gap: 2px;
}

.collab-summary strong {
  color: rgb(var(--wx-ink));
  font-size: 14px;
  font-weight: 760;
}

.collab-summary small,
.collab-empty {
  color: rgb(var(--wx-ink-subtle));
  font-size: 12px;
  font-weight: 650;
}

.collab-status {
  width: 9px;
  height: 9px;
  border-radius: 999px;
  background: rgb(var(--wx-ink-faint));
}

.collab-status.active {
  background: rgb(var(--wx-brand-emerald));
  box-shadow: 0 0 0 5px rgba(var(--wx-brand-emerald), 0.12);
}

.collab-avatars {
  display: flex;
  min-width: 0;
  align-items: center;
}

.collab-avatar {
  display: grid;
  width: 30px;
  height: 30px;
  place-items: center;
  margin-left: -6px;
  border: 2px solid rgba(255, 255, 255, 0.94);
  border-radius: 999px;
  background: var(--collab-color);
  color: #ffffff;
  box-shadow: 0 12px 22px -18px rgba(15, 23, 42, 0.8);
  font-size: 12px;
  font-weight: 760;
}

.collab-avatar:first-child {
  margin-left: 0;
}

.collab-actions {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.share-code {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid rgba(var(--wx-workspace-border), 0.72);
  border-radius: 999px;
  background: rgba(var(--wx-workspace-surface), 0.78);
  color: rgb(var(--wx-ink-muted));
  font-size: 12px;
  font-weight: 700;
}

.shell-button,
.join-panel button {
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid rgba(var(--wx-workspace-border), 0.78);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.72);
  color: rgb(var(--wx-ink));
  cursor: pointer;
  font-size: 13px;
  font-weight: 720;
  transition: background 160ms ease, border-color 160ms ease, color 160ms ease;
}

.shell-button:hover,
.join-panel button:hover {
  border-color: rgba(var(--wx-brand-indigo), 0.28);
  background: rgba(var(--wx-brand-indigo-soft), 0.66);
  color: rgb(var(--wx-brand-indigo));
}

.shell-button.primary {
  border-color: rgb(var(--wx-brand-indigo));
  background: rgb(var(--wx-brand-indigo));
  color: #ffffff;
}

.join-panel {
  position: absolute;
  right: 28px;
  top: calc(100% + 8px);
  display: flex;
  gap: 8px;
  padding: 8px;
  border: 1px solid rgba(var(--wx-workspace-border), 0.72);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 18px 42px -30px rgba(15, 23, 42, 0.48);
  backdrop-filter: blur(16px);
}

.join-panel input {
  min-height: 34px;
  width: 180px;
  padding: 0 10px;
  border: 1px solid rgba(var(--wx-workspace-border), 0.88);
  border-radius: 8px;
  color: rgb(var(--wx-ink));
  font-size: 13px;
  outline: none;
}

.join-panel input:focus {
  border-color: rgba(var(--wx-brand-indigo), 0.55);
  box-shadow: 0 0 0 3px rgba(var(--wx-brand-indigo), 0.14);
}

@media (max-width: 920px) {
  .collab-bar {
    grid-template-columns: 1fr;
    gap: 10px;
    padding: 12px 16px;
  }

  .collab-actions {
    flex-wrap: wrap;
  }

  .join-panel {
    position: static;
    flex-wrap: wrap;
  }
}
</style>
