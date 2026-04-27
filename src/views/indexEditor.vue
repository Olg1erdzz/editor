<template>
  <div class="editor-shell">
    <aside class="workspace-sidebar" aria-label="编辑器导航">
      <div class="brand-block">
        <span class="brand-mark">文</span>
        <div>
          <p class="eyebrow">WenXing Editor</p>
          <h1>文星编辑器</h1>
        </div>
      </div>

      <div class="primary-actions">
        <button class="action-button primary" type="button" @click="dialogVisible = true">
          <el-icon><Plus /></el-icon>
          <span>新建文档</span>
        </button>
        <button class="action-button" type="button" @click="triggerFileInput">
          <el-icon><Upload /></el-icon>
          <span>上传本地文件</span>
        </button>
        <input ref="fileInput" class="visually-hidden" type="file" @change="handleFileChange" />
      </div>

      <nav class="sidebar-nav" aria-label="常用编辑功能">
        <button v-for="item in quickTools" :key="item.path" type="button" @click="openTool(item)">
          <el-icon>
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.title }}</span>
        </button>
      </nav>
    </aside>

    <main class="workspace-main">
      <header class="workspace-header">
        <div>
          <p class="eyebrow">Document Workspace</p>
          <h2>我的文档</h2>
        </div>
        <label class="search-box" for="document-search">
          <el-icon><Search /></el-icon>
          <input
            id="document-search"
            ref="searchInput"
            v-model="searchQuery"
            type="search"
            placeholder="搜索文档名称"
            @keydown.enter="handleSearch"
            @focus="openSearchDialog"
          />
        </label>
      </header>

      <section class="filter-bar" aria-label="文档筛选">
        <button
          v-for="option in filterOptions"
          :key="option.value"
          type="button"
          :class="{ active: filterType === option.value }"
          @click="handleCommand(option.value)"
        >
          {{ option.label }}
        </button>
      </section>

      <section class="document-panel" aria-label="文档列表">
        <div class="table-header">
          <span>名称</span>
          <span>路径</span>
          <span>作者</span>
          <span>更新时间</span>
          <span>大小</span>
          <span>操作</span>
        </div>

        <div v-if="filteredDocuments.length === 0" class="empty-state">
          <el-icon><Files /></el-icon>
          <h3>暂无文档</h3>
          <p>新建或上传文件后，文档会显示在这里。</p>
          <button type="button" @click="dialogVisible = true">新建文档</button>
        </div>

        <ul v-else class="document-list">
          <li v-for="doc in filteredDocuments" :key="doc.id" @click="navigateToFile(doc)">
            <div class="document-name">
              <el-icon><Document /></el-icon>
              <div>
                <strong :title="doc.name">{{ doc.name }}</strong>
                <small>{{ doc.star ? "已收藏" : "普通文档" }}</small>
              </div>
            </div>
            <span :title="doc.file_path">{{ doc.file_path || "-" }}</span>
            <span>{{ doc.creator || "我" }}</span>
            <span>{{ doc.last_modified_time || "-" }}</span>
            <span>{{ doc.size || "-" }}</span>
            <div class="row-actions">
              <button type="button" :aria-label="doc.star ? '取消收藏' : '收藏'" @click.stop="toggleStar(doc)">
                <el-icon :class="{ starred: doc.star }"><Star /></el-icon>
              </button>
              <button type="button" aria-label="分享" @click.stop="shareDocument(doc)">
                <el-icon><Share /></el-icon>
              </button>
              <button type="button" aria-label="删除" @click.stop="confirmDelete(doc)">
                <el-icon><Delete /></el-icon>
              </button>
            </div>
          </li>
        </ul>
      </section>
    </main>

    <aside class="inspector-panel" aria-label="编辑器状态">
      <section class="status-card">
        <div class="status-title">
          <el-icon><Calendar /></el-icon>
          <span>{{ newDate }}</span>
        </div>
        <el-calendar ref="calendar" v-model="currentDate" class="compact-calendar" />
      </section>

      <section class="status-card">
        <div class="status-title">
          <el-icon><Memo /></el-icon>
          <span>工作区概览</span>
        </div>
        <dl class="workspace-stats">
          <div>
            <dt>全部文档</dt>
            <dd>{{ documents.length }}</dd>
          </div>
          <div>
            <dt>收藏</dt>
            <dd>{{ starredCount }}</dd>
          </div>
          <div>
            <dt>当前筛选</dt>
            <dd>{{ dropdownLabel }}</dd>
          </div>
        </dl>
      </section>
    </aside>

    <el-dialog v-model="searchDialogVisible" title="搜索结果" width="760px" custom-class="clean-dialog">
      <label class="dialog-search" for="dialog-search-input">
        <el-icon><Search /></el-icon>
        <input id="dialog-search-input" v-model="searchQuery" type="search" placeholder="输入文档名称" @keydown.enter="handleSearch" />
      </label>
      <ul class="search-results">
        <li v-if="searchResults.length === 0" class="search-empty">没有匹配的文档</li>
        <li v-for="doc in searchResults" v-else :key="doc.id" @click="navigateToFile(doc)">
          <span>{{ doc.name }}</span>
          <small>{{ doc.file_path || "-" }}</small>
          <button type="button" @click.stop="shareDocument(doc)">分享</button>
          <button type="button" @click.stop="confirmDelete(doc)">删除</button>
        </li>
      </ul>
    </el-dialog>

    <el-dialog v-model="dialogVisible" title="选择编辑任务" width="720px" :before-close="handleClose" custom-class="clean-dialog">
      <div class="task-grid">
        <button type="button" @click="navigateToNewPage">
          <el-icon><Edit /></el-icon>
          <strong>智能文档</strong>
          <span>从空白页面开始编辑</span>
        </button>
        <button v-for="item in creationTools" :key="item.path" type="button" @click="openTool(item)">
          <el-icon>
            <component :is="item.icon" />
          </el-icon>
          <strong>{{ item.title }}</strong>
          <span>{{ item.description }}</span>
        </button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import {
  Calendar,
  ChatDotRound,
  Connection,
  Delete,
  Document,
  Edit,
  Files,
  Memo,
  Plus,
  Search,
  Share,
  Star,
  Upload,
  View
} from "@element-plus/icons-vue";

export default {
  components: {
    Calendar,
    ChatDotRound,
    Connection,
    Delete,
    Document,
    Edit,
    Files,
    Memo,
    Plus,
    Search,
    Share,
    Star,
    Upload,
    View
  },
  data() {
    return {
      dialogVisible: false,
      searchDialogVisible: false,
      filterType: "all",
      documents: [],
      searchResults: [],
      searchQuery: "",
      currentDate: new Date(),
      filterOptions: [
        { label: "全部", value: "all" },
        { label: "最近", value: "recent" },
        { label: "收藏", value: "starred" },
        { label: "Word", value: "word" },
        { label: "PDF", value: "pdf" }
      ],
      quickTools: [
        { id: 4, title: "评论批注", path: "/commenteditor", icon: "ChatDotRound" },
        { id: 3, title: "协作编辑", path: "/collaborativeeditor", icon: "Connection" },
        { id: 9, title: "页面模板", path: "/layout", icon: "View" }
      ],
      creationTools: [
        { id: 3, title: "协作编辑", description: "多人同步编辑与演示", path: "/collaborativeeditor", icon: "Connection" },
        { id: 4, title: "评论批注", description: "审阅、标注和讨论内容", path: "/commenteditor", icon: "ChatDotRound" },
        { id: 5, title: "操作记录", description: "查看文档变更历史", path: "/changeseteditor", icon: "Memo" },
        { id: 6, title: "版本比较", description: "对比不同版本差异", path: "/diff", icon: "Files" }
      ]
    };
  },
  computed: {
    dropdownLabel() {
      const option = this.filterOptions.find((item) => item.value === this.filterType);
      return option ? option.label : "全部";
    },
    filteredDocuments() {
      const today = new Date();
      const sevenDaysAgo = new Date(today);
      sevenDaysAgo.setDate(today.getDate() - 7);

      return this.documents.filter((doc) => {
        const name = doc.name || "";
        const modifiedTime = doc.last_modified_time ? new Date(doc.last_modified_time) : null;

        switch (this.filterType) {
          case "recent":
            return modifiedTime ? modifiedTime >= sevenDaysAgo : false;
          case "starred":
            return doc.star;
          case "word":
            return name.endsWith(".doc") || name.endsWith(".docx");
          case "pdf":
            return name.endsWith(".pdf");
          default:
            return true;
        }
      });
    },
    newDate() {
      return this.formatDate(this.currentDate);
    },
    starredCount() {
      return this.documents.filter((doc) => doc.star).length;
    }
  },
  async mounted() {
    await this.fetchDocuments();
  },
  methods: {
    addDocument(document) {
      this.$emit("add-document", document);
    },
    openTool(item) {
      this.dialogVisible = false;
      this.addDocument({ id: item.id, title: item.title, path: item.path });
      this.$router.push(item.path);
    },
    async fetchDocuments() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/get_documents", {
          params: {
            username: localStorage.getItem("userName")
          }
        });
        const payload = response.data || response;
        const items = payload.documents || payload.data || [];

        this.documents = items.map((doc) => ({
          ...doc,
          creator: doc.creator || "我",
          star: doc.star === true || doc.star === "true",
          isOpen: false
        }));
      } catch (error) {
        console.error("Error fetching documents:", error);
        this.documents = [];
      }
    },
    async navigateToFile(doc) {
      try {
        const username = localStorage.getItem("userName") || "unknown_user";
        const response = await axios.get("http://127.0.0.1:5000/api/open_document", {
          params: {
            username,
            file_name: doc.name
          },
          headers: {
            "Content-Type": "application/json"
          }
        });
        const documentContent = response.data || response || "";
        this.openDocument(doc, documentContent);
      } catch (error) {
        this.$message.error("打开文档时发生错误");
        console.error("Error navigating to document:", error);
        this.openDocument(doc, "");
      }
    },
    openDocument(doc, content) {
      const newDocument = {
        id: doc.id,
        title: doc.name,
        path: `/documents/${doc.file_path || doc.id}`,
        isOpen: true,
        content
      };

      doc.isOpen = true;
      this.$emit("add-document", newDocument);
      this.$router.push({
        path: newDocument.path,
        query: {
          name: doc.name,
          content
        }
      });
    },
    async confirmDelete(doc) {
      if (doc.isOpen) {
        this.$message.warning("文档正在打开，请先关闭后再删除。");
        return;
      }

      try {
        await this.$confirm("删除后无法恢复，是否继续？", "删除文档", {
          confirmButtonText: "删除",
          cancelButtonText: "取消",
          type: "warning"
        });
        await this.deleteDocument(doc);
      } catch (error) {
        if (error !== "cancel") {
          console.error("Delete cancelled or failed:", error);
        }
      }
    },
    async deleteDocument(doc) {
      try {
        const formData = new FormData();
        formData.append("username", localStorage.getItem("userName") || "unknown_user");
        formData.append("file_name", doc.name);

        const response = await axios.post("http://127.0.0.1:5000/api/delete", formData);
        const success = response.data === true || response.data === "true" || response === "true";

        if (success) {
          this.$message.success("文档已删除");
          this.documents = this.documents.filter((item) => item.id !== doc.id);
          this.searchResults = this.searchResults.filter((item) => item.id !== doc.id);
          await this.fetchDocuments();
        } else {
          this.$message.error("删除文档失败");
        }
      } catch (error) {
        this.$message.error("删除文档时发生错误");
        console.error("Error deleting document:", error);
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    async handleFileChange(event) {
      const file = event.target.files[0];
      if (!file) {
        return;
      }

      const username = localStorage.getItem("userName") || "unknown_user";
      const formData = new FormData();
      formData.append("file", file);
      formData.append("username", username);
      formData.append("file_name", file.name);

      const reader = new FileReader();
      reader.readAsText(file);
      reader.onload = async (e) => {
        const fileContent = e.target.result;
        if (!fileContent) {
          this.$message.error("读取文件内容失败，请重试。");
          return;
        }

        try {
          const uploadResponse = await axios.post("http://127.0.0.1:5000/api/upload", formData);
          if (uploadResponse) {
            const newDocument = {
              id: Date.now().toString(),
              title: file.name,
              path: `/documents/${Date.now()}`,
              isOpen: true,
              username,
              content: fileContent
            };

            this.documents.push({
              id: newDocument.id,
              name: file.name,
              file_path: newDocument.id,
              creator: "我",
              last_modified_time: new Date().toLocaleString(),
              size: `${Math.ceil(file.size / 1024)} KB`,
              star: false,
              isOpen: true
            });
            this.$emit("add-document", newDocument);
            this.$router.push({
              path: newDocument.path,
              query: {
                document: JSON.stringify(newDocument),
                content: fileContent
              }
            });

            this.$message.success("文件上传成功");
          } else {
            this.$message.error("文件上传失败，请稍后重试。");
          }
        } catch (error) {
          console.error("Error uploading file:", error);
          this.$message.error("文件上传时发生错误，请稍后重试。");
        } finally {
          event.target.value = "";
        }
      };
      reader.onerror = (error) => {
        console.error("Error reading file:", error);
        this.$message.error("读取文件内容时发生错误，请重试。");
      };
    },
    async toggleStar(doc) {
      const previousValue = doc.star;
      doc.star = !doc.star;

      try {
        const response = await axios.post("http://127.0.0.1:5000/api/update_star", {
          doc_id: doc.id,
          new_star: doc.star
        });
        const success = response.data === true || response.data === "true" || response === "true";
        if (!success) {
          throw new Error("Failed to update star status");
        }
      } catch (error) {
        console.error("Error updating star status:", error);
        doc.star = previousValue;
      }
    },
    handleCommand(command) {
      this.filterType = command;
    },
    handleClose(done) {
      done();
    },
    formatDate(value) {
      return new Intl.DateTimeFormat("zh-CN", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit"
      }).format(new Date(value));
    },
    navigateToNewPage() {
      this.dialogVisible = false;
      this.$router.push("/new-document-page");
    },
    shareDocument(doc) {
      this.$message.success(`已准备分享：${doc.name}`);
    },
    handleSearch() {
      const query = this.searchQuery.trim().toLowerCase();
      this.searchResults = query ? this.documents.filter((doc) => (doc.name || "").toLowerCase().includes(query)) : [];
      this.searchDialogVisible = true;
    },
    openSearchDialog() {
      this.handleSearch();
    }
  }
};
</script>

<style scoped>
.editor-shell {
  display: grid;
  grid-template-columns: 248px minmax(0, 1fr) 300px;
  min-height: calc(100vh - 4rem);
  background: #f6f7f9;
  color: #1f2937;
}

.workspace-sidebar,
.inspector-panel {
  border-color: #d8dee8;
  background: #ffffff;
}

.workspace-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px 18px;
  border-right: 1px solid #d8dee8;
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-mark {
  display: grid;
  width: 40px;
  height: 40px;
  place-items: center;
  border-radius: 8px;
  background: #1f2937;
  color: #ffffff;
  font-weight: 700;
}

.eyebrow {
  margin: 0;
  color: #64748b;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

h1,
h2,
h3 {
  margin: 0;
  letter-spacing: 0;
}

h1 {
  font-size: 19px;
}

h2 {
  font-size: 24px;
}

.primary-actions,
.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-button,
.sidebar-nav button,
.filter-bar button,
.row-actions button,
.empty-state button,
.task-grid button,
.search-results button {
  border: 1px solid #d8dee8;
  border-radius: 6px;
  background: #ffffff;
  color: #334155;
  cursor: pointer;
  font: inherit;
}

.action-button,
.sidebar-nav button {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 40px;
  padding: 0 12px;
  text-align: left;
}

.action-button.primary {
  border-color: #2563eb;
  background: #2563eb;
  color: #ffffff;
}

.sidebar-nav button:hover,
.filter-bar button:hover,
.row-actions button:hover,
.search-results button:hover {
  border-color: #94a3b8;
  background: #f8fafc;
}

.workspace-main {
  min-width: 0;
  padding: 24px;
}

.workspace-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 18px;
}

.search-box,
.dialog-search {
  display: flex;
  align-items: center;
  gap: 8px;
  width: min(420px, 100%);
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: #ffffff;
}

.search-box input,
.dialog-search input {
  width: 100%;
  border: 0;
  outline: 0;
  background: transparent;
  color: #111827;
  font: inherit;
}

.filter-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
  overflow-x: auto;
}

.filter-bar button {
  min-height: 34px;
  padding: 0 14px;
  white-space: nowrap;
}

.filter-bar button.active {
  border-color: #0f766e;
  background: #ecfdf5;
  color: #0f766e;
}

.document-panel {
  overflow: hidden;
  border: 1px solid #d8dee8;
  border-radius: 8px;
  background: #ffffff;
}

.table-header,
.document-list li {
  display: grid;
  grid-template-columns: minmax(220px, 1.6fr) minmax(140px, 1fr) 90px 150px 80px 116px;
  gap: 12px;
  align-items: center;
}

.table-header {
  min-height: 42px;
  padding: 0 16px;
  border-bottom: 1px solid #e5e7eb;
  background: #f8fafc;
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
}

.document-list {
  max-height: calc(100vh - 235px);
  margin: 0;
  padding: 0;
  overflow: auto;
  list-style: none;
}

.document-list li {
  min-height: 64px;
  padding: 0 16px;
  border-bottom: 1px solid #eef2f7;
  cursor: pointer;
}

.document-list li:hover {
  background: #f8fafc;
}

.document-list li > span,
.document-name strong {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-name {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.document-name small {
  display: block;
  margin-top: 2px;
  color: #64748b;
  font-size: 12px;
}

.row-actions {
  display: flex;
  gap: 6px;
}

.row-actions button {
  display: grid;
  width: 30px;
  height: 30px;
  place-items: center;
  padding: 0;
}

.starred {
  color: #d97706;
}

.empty-state {
  display: grid;
  min-height: 340px;
  place-items: center;
  align-content: center;
  gap: 10px;
  color: #64748b;
  text-align: center;
}

.empty-state .el-icon {
  color: #94a3b8;
  font-size: 34px;
}

.empty-state button {
  min-height: 36px;
  padding: 0 14px;
}

.inspector-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px 16px;
  border-left: 1px solid #d8dee8;
}

.status-card {
  border: 1px solid #d8dee8;
  border-radius: 8px;
  background: #ffffff;
}

.status-title {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px;
  border-bottom: 1px solid #eef2f7;
  font-weight: 700;
}

.compact-calendar {
  --el-calendar-cell-width: 34px;
  border: 0;
}

.compact-calendar :deep(.el-calendar__body) {
  padding: 8px 12px 12px;
}

.compact-calendar :deep(.el-calendar__header) {
  padding: 10px 12px;
}

.workspace-stats {
  margin: 0;
  padding: 12px 14px 14px;
}

.workspace-stats div {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  padding: 8px 0;
}

.workspace-stats dt {
  color: #64748b;
}

.workspace-stats dd {
  margin: 0;
  font-weight: 700;
}

.task-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.task-grid button {
  display: grid;
  gap: 8px;
  min-height: 112px;
  justify-items: start;
  padding: 16px;
  text-align: left;
}

.task-grid .el-icon {
  color: #2563eb;
  font-size: 22px;
}

.task-grid span {
  color: #64748b;
  font-size: 13px;
}

.dialog-search {
  width: 100%;
  margin-bottom: 12px;
}

.search-results {
  margin: 0;
  padding: 0;
  list-style: none;
}

.search-results li {
  display: grid;
  grid-template-columns: minmax(160px, 1fr) minmax(180px, 1fr) 64px 64px;
  gap: 10px;
  align-items: center;
  min-height: 44px;
  border-bottom: 1px solid #eef2f7;
}

.search-results small,
.search-results span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.search-empty {
  display: block !important;
  padding: 24px 0;
  color: #64748b;
  text-align: center;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
}

@media (max-width: 1180px) {
  .editor-shell {
    grid-template-columns: 220px minmax(0, 1fr);
  }

  .inspector-panel {
    display: none;
  }
}

@media (max-width: 820px) {
  .editor-shell {
    display: block;
  }

  .workspace-sidebar {
    border-right: 0;
    border-bottom: 1px solid #d8dee8;
  }

  .workspace-header {
    align-items: stretch;
    flex-direction: column;
  }

  .table-header {
    display: none;
  }

  .document-list {
    max-height: none;
  }

  .document-list li {
    grid-template-columns: 1fr;
    gap: 8px;
    padding: 14px;
  }

  .row-actions {
    justify-content: flex-start;
  }

  .task-grid,
  .search-results li {
    grid-template-columns: 1fr;
  }
}
</style>
