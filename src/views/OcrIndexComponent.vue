<template>
  <div class="ocr-container">
    <el-upload action="http://localhost:8090/upload" :on-success="handleUploadSuccess" :on-error="handleUploadError" :before-upload="handleBeforeUpload" list-type="picture-card">
      <i class="el-icon-plus"></i>
    </el-upload>
    <el-button @click="recognizeImage" style="margin-left: 50px">识别图片</el-button>
    <el-button @click="closeResults" style="margin-left: 50px">关闭图像结果</el-button>
    <el-dropdown>
      <el-button style="margin-left: 50px"> 保存图片<i class="el-icon-arrow-down el-icon--right"></i> </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="saveAsPDF">保存为 PDF</el-dropdown-item>
          <el-dropdown-item @click="saveAsWord">保存为 Word</el-dropdown-item>
          <el-dropdown-item @click="saveAsImage">保存为图片</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <el-button @click="clearResults" style="margin-left: 50px">重置</el-button>

    <el-row :gutter="20" style="margin-top: 20px; padding: 0px 50px 0 50px">
      <el-col :span="12">
        <el-card style="height: 1000px">
          <h3 style="text-align: center">古籍图片展示</h3>
          <el-image v-if="uploadedImageUrl" :src="uploadedImageUrl" style="width: 600px; height: 800px"></el-image>
          <div v-if="uploading" class="text-center">
            <el-progress type="circle" :percentage="uploadProgress"></el-progress>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card style="height: 1000px; width: 800px">
          <h3 style="text-align: center">识别结果</h3>
          <div class="quill">
            <quill-editor ref="quillEditor" theme="snow" v-model:content="recognizedText" p> </quill-editor>
          </div>
          <div v-if="loading" class="text-center"></div>
          <div v-if="error" class="error-message">{{ errorMessage }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import "@vueup/vue-quill/dist/vue-quill.bubble.css";
import { Document, Packer, Paragraph } from "docx";
import { jsPDF } from "jspdf";
import html2canvas from "html2canvas";
import { QuillEditor } from "@vueup/vue-quill";
import { saveAs } from "file-saver";

export default {
  name: "OcrIndexComponent",
  data() {
    return {
      uploadedImageUrl: null,
      recognizedText: "",
      loading: false,
      uploading: false,
      uploadProgress: 0,
      error: false,
      errorMessage: ""
    };
  },
  methods: {
    handleBeforeUpload() {
      this.uploading = true;
    },
    handleUploadSuccess(response) {
      this.uploadedImageUrl = response.url;
      this.error = false;
      this.uploading = false;
      this.uploadProgress = 100;
      this.$message.success("图片上传成功");
    },
    handleUploadError(err) {
      this.error = true;
      this.uploading = false;
      this.errorMessage = "上传失败: " + err.message;
      this.$message.error("图片上传失败");
    },
    confirmUpload() {
      this.$emit("close");
    },
    recognizeImage() {
      if (!this.uploadedImageUrl) {
        this.error = true;
        this.errorMessage = "请先上传图片";
        return;
      }
      this.loading = true;
      fetch(`http://localhost:8090/recognize?url=${this.uploadedImageUrl}`)
        .then((response) => response.json())
        .then((data) => {
          this.recognizedText = data.text;
          this.loading = false;
          this.error = false;
        })
        .catch((error) => {
          this.error = true;
          this.errorMessage = "识别失败: " + error.message;
          this.loading = false;
        });
    },
    closeResults() {
      this.recognizedText = "";
    },
    async saveAsPDF() {
      const content = this.$refs.quillEditor.$el.querySelector(".ql-editor");
      const canvas = await html2canvas(content);
      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF({
        orientation: "portrait",
        unit: "px",
        format: [canvas.width, canvas.height]
      });
      pdf.addImage(imgData, "PNG", 0, 0);
      pdf.save("download.pdf");
    },
    async saveAsWord() {
      const contentHtml = this.$refs.quillEditor.$el.querySelector(".ql-editor").innerHTML;
      const doc = new Document();
      const paragraphs = contentHtml.split("<p>").map((p) => new Paragraph(p.replace("</p>", "")));
      doc.addSection({ children: paragraphs });

      const blob = await Packer.toBlob(doc);
      saveAs(blob, "download.docx");
    },
    saveAsImage() {
      const content = this.$refs.quillEditor.$el.querySelector(".ql-editor");
      html2canvas(content).then((canvas) => {
        const img = canvas.toDataURL("image/png");
        const link = document.createElement("a");
        link.href = img;
        link.download = "download.png";
        link.click();
      });
    },
    clearResults() {
      this.uploadedImageUrl = null;
      this.recognizedText = "";
      this.error = false;
    }
  },
  components: {
    quillEditor: QuillEditor
  }
};
</script>

<style>
.ocr-container {
  width: 100%;
  height: 100%;
  overflow-y: auto;
}

.quill {
  width: 720px;
  height: 1000px;
  font-size: 50px;
}

.ql-editor p {
  font-size: 20px;
  height: 666px;
}

.ql-toolbar.ql-snow {
  height: 150px;
}
</style>
