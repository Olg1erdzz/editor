<template>
  <div class="new-document-page">
    <header class="page-header">
      <div>
        <p class="eyebrow">Create</p>
        <h1>新建文档</h1>
      </div>
      <label class="search-box" for="template-search">
        <el-icon><Search /></el-icon>
        <input id="template-search" v-model="templateQuery" type="search" placeholder="搜索模板" />
      </label>
    </header>

    <main class="page-content">
      <section class="create-panel">
        <button class="blank-document" type="button" @click="dialogVisible = true">
          <span class="blank-icon">
            <el-icon><Plus /></el-icon>
          </span>
          <strong>空白文档</strong>
          <small>从一个干净的编辑页面开始</small>
        </button>
      </section>

      <section class="template-section">
        <div class="section-title">
          <h2>模板推荐</h2>
          <span>{{ filteredTemplates.length }} 个模板</span>
        </div>

        <div v-if="filteredTemplates.length === 0" class="empty-state">
          <el-icon><Files /></el-icon>
          <p>暂无匹配的模板</p>
        </div>

        <div v-else class="template-grid">
          <button v-for="template in filteredTemplates" :key="template.id" class="template-card" type="button">
            <div class="template-preview">
              <el-icon><Document /></el-icon>
            </div>
            <div>
              <strong>{{ template.name }}</strong>
              <span>{{ template.likes }} 次点赞</span>
            </div>
          </button>
        </div>
      </section>
    </main>

    <el-dialog v-model="dialogVisible" title="新建空白文档" width="420px">
      <el-input v-model="newDocumentName" placeholder="请输入文档名称" @keydown.enter="createNewDocument" />
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="isCreating" @click="createNewDocument">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import { Document, Files, Plus, Search } from "@element-plus/icons-vue";

export default {
  components: {
    Document,
    Files,
    Plus,
    Search
  },
  data() {
    return {
      dialogVisible: false,
      isCreating: false,
      newDocumentName: "",
      templateQuery: "",
      templates: [
        { id: 1, name: "会议纪要", likes: 100 },
        { id: 2, name: "课程笔记", likes: 86 },
        { id: 3, name: "项目说明", likes: 72 }
      ]
    };
  },
  computed: {
    filteredTemplates() {
      const query = this.templateQuery.trim().toLowerCase();
      if (!query) {
        return this.templates;
      }
      return this.templates.filter((template) => template.name.toLowerCase().includes(query));
    }
  },
  mounted() {
    this.fetchTemplates();
  },
  methods: {
    async createNewDocument() {
      const documentName = this.newDocumentName.trim();
      if (!documentName) {
        this.$message.error("文档名称不能为空。");
        return;
      }

      this.isCreating = true;
      const username = localStorage.getItem("userName") || "unknown_user";

      try {
        const existingDocumentsResponse = await axios.get("http://127.0.0.1:5000/api/check_documents", {
          params: {
            username,
            file_name: documentName
          }
        });

        if (existingDocumentsResponse.data?.hwdata === "true") {
          this.$message.error("文档名称已存在，请换一个名称。");
          return;
        }

        const uploadResponse = await axios.post("http://127.0.0.1:5000/api/upload", {
          username,
          file_name: documentName,
          file_type: "doc"
        });

        if (uploadResponse.data?.hwdata !== "true") {
          this.$message.error("创建文档失败，请稍后重试。");
          return;
        }

        const newDocument = {
          id: Date.now().toString(),
          title: documentName,
          path: `/documents/${Date.now()}`,
          isOpen: true,
          username
        };

        this.dialogVisible = false;
        this.newDocumentName = "";
        this.$emit("add-document", newDocument);
        this.$router.push({
          path: newDocument.path,
          query: {
            document: JSON.stringify(newDocument),
            name: documentName,
            content: ""
          }
        });
        this.$message.success("文档已创建。");
      } catch (error) {
        console.error("Error creating document:", error);
        this.$message.error("无法创建文档，请确认后端和数据库已启动。");
      } finally {
        this.isCreating = false;
      }
    },
    async fetchTemplates() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/get_all_stencil");
        const templates = response.data?.templates;
        if (Array.isArray(templates) && templates.length > 0) {
          this.templates = templates.map((template, index) => ({
            id: template.id || index + 1,
            name: template.name || `模板 ${index + 1}`,
            likes: template.likes || 0
          }));
        }
      } catch (error) {
        console.error("Failed to fetch templates:", error);
      }
    }
  }
};
</script>

<style scoped>
.new-document-page {
  min-height: calc(100vh - 4rem);
  padding: 24px;
  background: #f6f7f9;
  color: #1f2937;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

.eyebrow {
  margin: 0;
  color: #64748b;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

h1,
h2 {
  margin: 0;
  letter-spacing: 0;
}

h1 {
  font-size: 24px;
}

h2 {
  font-size: 18px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  width: min(360px, 100%);
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: #ffffff;
}

.search-box input {
  width: 100%;
  border: 0;
  outline: 0;
  background: transparent;
  color: #111827;
  font: inherit;
}

.page-content {
  display: grid;
  gap: 20px;
}

.create-panel,
.template-section {
  border: 1px solid #d8dee8;
  border-radius: 8px;
  background: #ffffff;
}

.create-panel {
  padding: 18px;
}

.blank-document,
.template-card {
  border: 1px solid #d8dee8;
  border-radius: 6px;
  background: #ffffff;
  color: #334155;
  cursor: pointer;
  font: inherit;
  text-align: left;
}

.blank-document {
  display: grid;
  width: 190px;
  min-height: 150px;
  align-content: center;
  justify-items: center;
  gap: 8px;
  text-align: center;
}

.blank-document:hover,
.template-card:hover {
  border-color: #2563eb;
  background: #f8fafc;
}

.blank-icon {
  display: grid;
  width: 52px;
  height: 52px;
  place-items: center;
  border-radius: 8px;
  background: #eff6ff;
  color: #2563eb;
  font-size: 24px;
}

.blank-document small,
.template-card span,
.section-title span {
  color: #64748b;
  font-size: 13px;
}

.template-section {
  padding: 18px;
}

.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.template-card {
  display: grid;
  grid-template-columns: 54px minmax(0, 1fr);
  gap: 12px;
  align-items: center;
  min-height: 84px;
  padding: 14px;
}

.template-card strong,
.template-card span {
  display: block;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.template-preview {
  display: grid;
  width: 54px;
  height: 54px;
  place-items: center;
  border-radius: 6px;
  background: #f1f5f9;
  color: #475569;
  font-size: 24px;
}

.empty-state {
  display: grid;
  min-height: 180px;
  place-items: center;
  align-content: center;
  gap: 8px;
  color: #64748b;
}

.empty-state .el-icon {
  font-size: 30px;
}

@media (max-width: 720px) {
  .page-header {
    align-items: stretch;
    flex-direction: column;
  }

  .blank-document {
    width: 100%;
  }
}
</style>
