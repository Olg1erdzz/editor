<!-- headerComponent.vue -->
<template>
  <div>
    <el-dialog title="上传模版" v-model="dialogTableVisible" width="60%" height="50%">
      <div v-if="dialogTableVisible">
        <project-file-upload ref="uploadProjectFileModal" @showButton="isOpenUploadButton = true" @mergeUploadProjectSuccess="mergeUploadProjectSuccess" @removeFile="isOpenUploadButton = false" :documents="documents" :document="document" :editor="editor"></project-file-upload>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button v-if="isOpenCompleteButton" @click="closeUploadModal">完成</el-button>
          <el-button type="primary" v-if="isOpenUploadButton" @click="computeMD5ProjectFile">开始上传</el-button>
        </span>
      </template>
    </el-dialog>
    <div class="box-card" body-style="padding: 8px">
      <div class="button-container">
        <el-button type="danger" @click="dialogTableVisible = true">上传模版</el-button>
        <el-button type="primary">全部</el-button>

      </div>
    </div>
  </div>
</template>

<script>
import projectFileUpload from "./videoUpload/projectFileUpload.vue";
import { Editor } from "@tiptap/vue-3"; // 大文件上传组件
import { defineComponent } from "vue";
export default {
  name: "headerComponent",
  props: {
    documents: Array,
    document: {
      type: Object,
      required: true
    },
    editor: {
      type: Editor,
      required: true
    }
  },
  components: { projectFileUpload },
  data() {
    return {
      adminPermission: "system:admin:list",
      permissions: [],
      dialogTableVisible: false,
      isOpenCompleteButton: false,
      isOpenUploadButton: false,
      searchInput: "",
      avatarAddr: ""
    };
  },
  created() {
    this.permissions = localStorage.getItem("permissions");
    this.avatarAddr = this.$store.state.baseUrl.remoteUrl + localStorage.avatarAddr;
  },
  methods: {
    // 上传项目文件成功
    mergeUploadProjectSuccess() {
      this.isOpenCompleteButton = true;
      this.isOpenUploadButton = false;
    },
    // 对选择的文件进行切片计算
    computeMD5ProjectFile() {
      this.$refs.uploadProjectFileModal.computeMD5ProjectFile();
    },
    // 关闭上传项目文件的Modal
    closeUploadModal() {
      this.dialogTableVisible = false;
      this.isOpenCompleteButton = false;
      this.$router.go(0);
    },
    toMessagePage() {
      this.$router.push("/messagePage");
    },
    toVideoClassifyPage() {
      this.$router.push("/videoClassify");
    }
  }
};
</script>

<style scoped>
/*.button-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 10px;
}

.el-button {
  flex: 1;
  min-width: 100px;
  margin-bottom: 10px;
}*/
.titlestyle {
  font-weight: bold;
  font-size: 15px;
  font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
}
</style>
