<template>
  <header class="editor-topbar" ref="navbar">
    <div class="topbar-left">
      <router-link class="topbar-brand" to="/" aria-label="文星协作编辑器">
        <span class="brand-icon">文</span>
        <span class="brand-copy">
          <strong>文星</strong>
          <small>Workspace</small>
        </span>
      </router-link>

      <nav class="breadcrumb-nav" aria-label="文档位置">
        <ol role="list">
          <li>
            <router-link to="/" class="breadcrumb-link">文档库</router-link>
          </li>
          <li v-if="$route.path !== '/'" class="breadcrumb-current">
            <svg aria-hidden="true" class="breadcrumb-arrow" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
            <el-dropdown trigger="click" @command="switchDocument">
              <button
                :key="activeDocumentTitle"
                class="document-switch"
                type="button"
                v-motion
                :initial="{ opacity: 0, y: -6, filter: 'blur(4px)' }"
                :enter="{ opacity: 1, y: 0, filter: 'blur(0px)' }"
              >
                <span>{{ activeDocumentTitle }}</span>
                <svg aria-hidden="true" class="switch-chevron" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <template #dropdown>
                <el-dropdown-menu class="workspace-dropdown">
                  <el-dropdown-item v-for="(doc, index) in documents" :key="doc.id" :command="doc.path">
                    <span class="document-option" :class="{ active: doc.path === $route.path }">
                      <span class="document-dot"></span>
                      <span class="document-name">{{ doc.title }}</span>
                      <button type="button" class="document-close" aria-label="关闭文档" @click.stop.prevent="showConfirmDialog(doc, index)">×</button>
                    </span>
                  </el-dropdown-item>
                  <el-dropdown-item v-if="documents.length === 0" disabled>无打开的文档</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </li>
        </ol>
      </nav>
    </div>

    <div class="topbar-right">
      <div class="status-strip" aria-label="文档状态">
        <span class="status-dot"></span>
        <span>就绪</span>
        <em>{{ openedDocumentCount }} 个打开文档</em>
      </div>
      <router-link v-if="!isLoggedIn" class="login-link" to="/login">登录</router-link>
      <el-dropdown v-else @command="handleCommand">
        <button class="user-menu" type="button" :title="username">
          <img v-if="userAvatar" :src="userAvatar" alt="" />
          <span v-else class="avatar-fallback bg-brand-indigo">{{ username.slice(0, 1).toUpperCase() }}</span>
          <span class="user-name">{{ username }}</span>
        </button>
        <template #dropdown>
          <el-dropdown-menu class="workspace-dropdown">
            <el-dropdown-item command="update_avatar">更换头像</el-dropdown-item>
            <el-dropdown-item command="logout" class="text-red-600">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <input ref="fileInput" class="hidden-input" type="file" @change="onFileChange" />
    </div>

    <el-dialog title="关闭文档" v-model="dialogVisible" width="360px" :before-close="handleDialogClose">
      <span class="dialog-copy">是否关闭当前文档？</span>
      <template #footer>
        <el-button @click="handleClose(false)" plain>取消</el-button>
        <el-button type="primary" @click="handleClose(true)">关闭</el-button>
      </template>
    </el-dialog>
  </header>
</template>

<script>
import { defineComponent } from "vue";
import axios from "axios";
import imageCompression from "browser-image-compression";
import { ElDropdown, ElDropdownMenu, ElDropdownItem } from "element-plus";

export default defineComponent({
  props: {
    documents: {
      type: Array,
      default: () => []
    }
  },
  components: {
    ElDropdown,
    ElDropdownMenu,
    ElDropdownItem
  },
  data() {
    return {
      isLoggedIn: false,
      username: "",
      role: "",
      userAvatar: "",
      dialogVisible: false,
      currentDoc: null,
      currentIndex: null
    };
  },
  async mounted() {
    await this.$nextTick();
    this.checkLoginStatus();
  },
  computed: {
    activeDocumentTitle() {
      if (this.$route.path === "/") return "文档库";
      const doc = this.documents.find(d => d.path === this.$route.path);
      if (doc) return doc.title;
      if (typeof this.$route.query.name === "string") return this.$route.query.name;
      if (typeof this.$route.query.document === "string") {
        try {
          const routeDocument = JSON.parse(this.$route.query.document);
          if (routeDocument?.title) return routeDocument.title;
        } catch (error) {
          console.warn("Invalid document route payload:", error);
        }
      }
      return "未命名文档";
    },
    openedDocumentCount() {
      return this.documents.length;
    }
  },
  methods: {
    switchDocument(path) {
      if (path && this.$route.path !== path) {
        this.$router.push(path);
      }
    },
    handleClose() {
      this.removeDocument(this.currentDoc, this.currentIndex);
      this.dialogVisible = false;
    },
    handleDialogClose() {
      this.dialogVisible = false;
    },
    showConfirmDialog(doc, index) {
      this.currentDoc = doc;
      this.currentIndex = index;
      this.dialogVisible = true;
    },
    handleCommand(command) {
      if (command === "logout") {
        this.logout();
      } else if (command === "update_avatar") {
        this.$refs.fileInput.click();
      }
    },
    checkLoginStatus() {
      const storedUsername = localStorage.getItem("userName");
      const storedRole = localStorage.getItem("role");
      const storedAvatar = localStorage.getItem("avatar");
      if (storedUsername && storedRole) {
        this.isLoggedIn = true;
        this.username = storedUsername;
        this.role = storedRole;
        this.userAvatar = storedAvatar || "";
      }
    },
    logout() {
      localStorage.removeItem("userName");
      localStorage.removeItem("role");
      localStorage.removeItem("avatar");
      this.isLoggedIn = false;
      this.username = "";
      this.role = "";
      this.userAvatar = "";
      this.$router.push("/login");
    },
    removeDocument(doc, index) {
      if (!doc) {
        return;
      }
      this.$emit("remove-document", { id: doc.id, index });
    },
    async onFileChange(event) {
      const file = event.target.files[0];
      if (!file) {
        return;
      }

      const options = {
        maxSizeMB: 0.1,
        maxWidthOrHeight: 1920,
        useWebWorker: true
      };

      try {
        const compressedFile = await imageCompression(file, options);
        const reader = new FileReader();
        reader.onload = async (e) => {
          const avatar = e.target.result;
          const formData = new FormData();
          formData.append("username", this.username);
          formData.append("avatar", avatar);

          const response = await axios.post("http://127.0.0.1:5000/api/update_avatar", formData);
          const success = response.data === 0 || response === 0;
          if (success) {
            localStorage.setItem("avatar", avatar);
            this.userAvatar = avatar;
          }
        };
        reader.readAsDataURL(compressedFile);
      } catch (error) {
        console.error("Failed to update avatar:", error);
      } finally {
        event.target.value = "";
      }
    }
  }
});
</script>

<style scoped>
.editor-topbar {
  position: fixed;
  inset: 0 0 auto;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 4rem;
  padding: 0 28px;
  border-bottom: 1px solid rgba(var(--wx-workspace-border), 0.78);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.82)),
    rgba(var(--wx-workspace-shell), 0.82);
  color: rgb(var(--wx-ink));
  box-shadow: 0 14px 36px -34px rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(18px) saturate(1.12);
  -webkit-backdrop-filter: blur(18px) saturate(1.12);
}

.topbar-left {
  display: flex;
  align-items: center;
  min-width: 0;
  gap: 26px;
}

.topbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 148px;
  text-decoration: none;
}

.brand-icon {
  display: grid;
  width: 34px;
  height: 34px;
  place-items: center;
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 8px;
  background: rgb(var(--wx-brand-indigo));
  color: #ffffff;
  box-shadow: inset 0 1px rgba(255, 255, 255, 0.16), 0 14px 24px -20px rgba(43, 55, 117, 0.85);
  font-family: var(--font-geist, "Geist"), "Microsoft YaHei", sans-serif;
  font-size: 15px;
  font-weight: 800;
}

.brand-copy {
  display: flex;
  flex-direction: column;
  gap: 1px;
  line-height: 1;
}

.brand-copy strong {
  color: rgb(var(--wx-ink));
  font-size: 14px;
  font-weight: 760;
}

.brand-copy small {
  color: rgb(var(--wx-ink-subtle));
  font-size: 10px;
  font-weight: 650;
  letter-spacing: 0;
  text-transform: uppercase;
}

.breadcrumb-nav {
  min-width: 0;
}

.breadcrumb-nav ol,
.breadcrumb-current {
  display: flex;
  align-items: center;
}

.breadcrumb-nav ol {
  gap: 6px;
  min-width: 0;
  padding: 0;
  margin: 0;
  list-style: none;
}

.breadcrumb-link,
.document-switch {
  min-height: 34px;
  color: rgb(var(--wx-ink-muted));
  font-size: 13px;
  font-weight: 650;
  text-decoration: none;
  transition: color 160ms ease, background 160ms ease, box-shadow 160ms ease;
}

.breadcrumb-link {
  display: inline-flex;
  align-items: center;
  padding: 0 10px;
  border-radius: 8px;
}

.breadcrumb-link:hover {
  background: rgba(var(--wx-workspace-surface), 0.9);
  color: rgb(var(--wx-ink));
}

.breadcrumb-arrow {
  width: 15px;
  height: 15px;
  color: rgb(var(--wx-ink-faint));
}

.document-switch {
  display: inline-flex;
  align-items: center;
  max-width: min(42vw, 420px);
  gap: 6px;
  padding: 0 10px;
  border: 1px solid transparent;
  border-radius: 8px;
  background: transparent;
  color: rgb(var(--wx-ink));
  cursor: pointer;
}

.document-switch span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-switch:hover {
  border-color: rgba(var(--wx-workspace-border), 0.7);
  background: rgba(var(--wx-workspace-surface), 0.88);
  box-shadow: 0 8px 18px -18px rgba(15, 23, 42, 0.7);
}

.switch-chevron {
  width: 14px;
  height: 14px;
  flex: 0 0 auto;
  color: rgb(var(--wx-ink-subtle));
}

.topbar-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding-left: 16px;
}

.status-strip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid rgba(var(--wx-workspace-border), 0.68);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.66);
  color: rgb(var(--wx-ink-muted));
  font-size: 12px;
  font-weight: 650;
}

.status-strip em {
  color: rgb(var(--wx-ink-faint));
  font-style: normal;
  font-weight: 600;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 999px;
  background: rgb(var(--wx-brand-emerald));
  box-shadow: 0 0 0 4px rgba(var(--wx-brand-emerald), 0.12);
}

.login-link,
.user-menu {
  min-height: 36px;
  border-radius: 999px;
  background: transparent;
  border: 1px solid rgba(var(--wx-workspace-border), 0.74);
  transition: background 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
}

.login-link {
  display: inline-flex;
  align-items: center;
  padding: 0 14px;
  color: rgb(var(--wx-ink));
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
}

.login-link:hover,
.user-menu:hover {
  border-color: rgba(var(--wx-brand-indigo), 0.22);
  background: rgba(var(--wx-brand-indigo-soft), 0.52);
  box-shadow: 0 8px 18px -18px rgba(15, 23, 42, 0.7);
}

.user-menu {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  max-width: 180px;
  padding: 3px 10px 3px 4px;
  color: rgb(var(--wx-ink));
  cursor: pointer;
  font: inherit;
}

.user-menu img {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 0 0 1px rgba(var(--wx-workspace-border), 0.8);
}

.avatar-fallback {
  display: grid;
  place-items: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  color: white;
  font-weight: 600;
  font-size: 14px;
  background: rgb(var(--wx-brand-indigo));
}

.user-name {
  overflow: hidden;
  color: rgb(var(--wx-ink-muted));
  font-size: 13px;
  font-weight: 650;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hidden-input {
  display: none;
}

.workspace-dropdown {
  min-width: 220px;
}

.document-option {
  display: grid;
  grid-template-columns: 8px minmax(0, 1fr) 24px;
  align-items: center;
  width: 220px;
  gap: 8px;
}

.document-dot {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: rgb(var(--wx-ink-faint));
}

.document-option.active .document-dot {
  background: rgb(var(--wx-brand-emerald));
  box-shadow: 0 0 0 4px rgba(var(--wx-brand-emerald), 0.12);
}

.document-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-close {
  display: inline-grid;
  width: 22px;
  height: 22px;
  place-items: center;
  border-radius: 6px;
  color: rgb(var(--wx-ink-faint));
  font-size: 16px;
  line-height: 1;
}

.document-close:hover {
  background: rgba(220, 38, 38, 0.08);
  color: #b91c1c;
}

.dialog-copy {
  color: rgb(var(--wx-ink-muted));
  font-size: 14px;
}

@media (max-width: 760px) {
  .editor-topbar {
    flex-wrap: wrap;
    gap: 8px 12px;
    padding: 10px 14px;
  }

  .topbar-left,
  .topbar-right {
    width: 100%;
  }

  .topbar-right {
    justify-content: space-between;
    padding-left: 0;
  }

  .brand-copy,
  .status-strip em,
  .user-name {
    display: none;
  }

  .topbar-brand {
    min-width: auto;
  }

  .document-switch {
    max-width: calc(100vw - 132px);
  }
}
</style>
