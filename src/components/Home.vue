<template>
  <header class="editor-topbar" ref="navbar">
    <router-link class="topbar-brand" to="/">
      <span>文</span>
      <strong>文星编辑器</strong>
    </router-link>

    <nav class="document-tabs" aria-label="打开的文档">
      <router-link class="home-tab" to="/">文件</router-link>
      <div v-for="(doc, index) in documents" :key="doc.id" class="document-tab">
        <router-link :to="doc.path" :title="doc.title">{{ doc.title }}</router-link>
        <button type="button" aria-label="关闭文档" @click="showConfirmDialog(doc, index)">×</button>
      </div>
    </nav>

    <div class="topbar-user">
      <router-link v-if="!isLoggedIn" class="login-link" to="/login">登录</router-link>
      <el-dropdown v-else @command="handleCommand">
        <button class="user-menu" type="button">
          <img v-if="userAvatar" :src="userAvatar" alt="" />
          <span v-else class="avatar-fallback">{{ username.slice(0, 1).toUpperCase() }}</span>
          <span>{{ username }}</span>
        </button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="update_avatar">更换头像</el-dropdown-item>
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <input ref="fileInput" class="hidden-input" type="file" @change="onFileChange" />
    </div>

    <el-dialog title="关闭文档" v-model="dialogVisible" width="360px" :before-close="handleDialogClose">
      <span>是否关闭当前文档？</span>
      <template #footer>
        <el-button @click="handleClose(false)">取消</el-button>
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
  methods: {
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
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr) auto;
  align-items: center;
  min-height: 4rem;
  padding: 0 16px;
  border-bottom: 1px solid #d8dee8;
  background: rgba(255, 255, 255, 0.96);
  color: #1f2937;
}

.topbar-brand,
.home-tab,
.document-tab a,
.login-link {
  color: inherit;
  text-decoration: none;
}

.topbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.topbar-brand span,
.avatar-fallback {
  display: grid;
  width: 32px;
  height: 32px;
  place-items: center;
  border-radius: 8px;
  background: #1f2937;
  color: #ffffff;
  font-weight: 700;
}

.document-tabs {
  display: flex;
  min-width: 0;
  gap: 8px;
  overflow-x: auto;
}

.home-tab,
.document-tab {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  border: 1px solid #d8dee8;
  border-radius: 6px;
  background: #f8fafc;
}

.home-tab {
  padding: 0 12px;
}

.document-tab a {
  max-width: 180px;
  overflow: hidden;
  padding: 0 8px 0 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-tab button {
  width: 28px;
  height: 28px;
  margin-right: 3px;
  border: 0;
  border-radius: 4px;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  font-size: 18px;
  line-height: 1;
}

.document-tab button:hover {
  background: #e5e7eb;
  color: #111827;
}

.topbar-user {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-left: 12px;
}

.login-link,
.user-menu {
  min-height: 36px;
  border: 1px solid #d8dee8;
  border-radius: 6px;
  background: #ffffff;
}

.login-link {
  display: inline-flex;
  align-items: center;
  padding: 0 14px;
}

.user-menu {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0 10px;
  color: #1f2937;
  cursor: pointer;
  font: inherit;
}

.user-menu img {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-fallback {
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.hidden-input {
  display: none;
}

@media (max-width: 760px) {
  .editor-topbar {
    grid-template-columns: 1fr auto;
    gap: 8px;
  }

  .document-tabs {
    grid-column: 1 / -1;
    order: 3;
    padding-bottom: 8px;
  }
}
</style>
