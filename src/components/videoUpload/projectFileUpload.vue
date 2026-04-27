<template>
  <div>
    <el-form v-loading="loading" ref="form" v-if="isOpenVideoForm" :model="submitVideoData" :rules="rules" label-width="80px">
      <el-form-item label="标题" prop="title">
        <el-input v-model="submitVideoData.title"></el-input>
      </el-form-item>
      <el-form-item label="简介" prop="desc">
        <el-input type="textarea" v-model="submitVideoData.desc"></el-input>
      </el-form-item>
      <el-form-item label="标签" prop="label">
        <el-select v-model="submitVideoData.label" placeholder="模版类别">
          <el-option label="简历模版" value="简历模版"></el-option>
          <el-option label="实习证明" value="实习证明"></el-option>
          <!-- 添加更多选项 -->
        </el-select>
      </el-form-item>
      <el-form-item label="用户名" prop="title">
        <el-input v-model="submitVideoData.username"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即创建</el-button>
        <el-button @click="isOpenVideoForm = false">取消</el-button>
      </el-form-item>
    </el-form>
    <uploadFile ref="uploadFile" v-loading="loading" v-if="isOpenUploadModal" @checkFileSuccess="checkFileSuccess" @computeMD5FileSuccess="computeMD5FileSuccess" @removeFile="removeFile"></uploadFile>
  </div>
</template>

<script>
import uploadFile from "./uploadFile.vue";
import videoApi from "../../api/videoApi";
import { Editor } from "@tiptap/vue-3";

export default {
  name: "projectFileUpload",
  props: {
    documents: {
      type: Object,
      required: true
    },
    document: {
      type: Object,
      required: true
    },
    editor: {
      type: Editor,
      required: true
    }
  },
  components: { uploadFile },
  data() {
    const username = localStorage.getItem("userName") || "unknown_user";
    return {
      loading: false,
      isOpenVideoForm: true,
      isOpenUploadModal: false,
      submitVideoData: {
        title: "",
        desc: "",
        label: "",
        username
      },
      rules: {
        title: [
          { required: true, message: "请输入文件名称", trigger: "blur" },
          {
            min: 3,
            max: 20,
            message: "长度在 3 到 20 个字符",
            trigger: "blur"
          }
        ],
        desc: [
          { required: true, message: "请输入文件简介", trigger: "blur" },
          {
            min: 3,
            max: 200,
            message: "长度在 3 到 200 个字符",
            trigger: "blur"
          }
        ],
        label: [{ required: true, message: "请选择文件标签", trigger: "change" }],
        username: [{ required: true, message: "请输入用户名", trigger: "blur" }]
      },
      file: null, // 用于接收uploadFile.vue中onFileAdded方法中传来的已经验证过重名的file信息（在uploadProjectFile方法中传入用于切片上传）(原始文件)
      fileInfo: "" // 用于接收uploadFile.vue中onFileSuccess方法传来的已经切片计算过的文件信息（切片后的文件信息）
    };
  },
  methods: {
    onSubmit() {
      this.loading = true;
      this.$refs["form"].validate((valid) => {
        if (valid) {
          videoApi
            .checkVideoName(this.submitVideoData.title)
            .then((response) => {
              if (response.data && response.data.code === 200) {
                this.isOpenVideoForm = false;
                this.isOpenUploadModal = true;
                this.$message.success("文件名称验证成功！");
              } else {
                this.$message.error("文件名称已存在！");
              }
            })
            .catch((error) => {
              console.error("文件名称验证失败：", error);
              this.$message.error("文件名称验证失败！");
            })
            .finally(() => {
              this.loading = false;
            });
        } else {
          this.$message.error("请完善文件信息！");
          this.loading = false;
        }
      });
    },
    checkFileSuccess(file) {
      this.file = file;
      this.$emit("showButton");
    },
    computeMD5ProjectFile() {
      this.$refs.uploadFile.computeMD5(this.file);
      console.log("开始执行computeMD5方法");
    },
    computeMD5FileSuccess(fileInfo) {
      this.fileInfo = fileInfo;
      this.mergeProjectFile();
    },
    mergeProjectFile() {
      console.log("开始合并上传");
      const username = localStorage.getItem("userName") || "unknown_user";
      console.log(username);
      this.loading = true;
      let videoInfo = {
        title: this.submitVideoData.title,
        description: this.submitVideoData.desc,
        label: this.submitVideoData.label,
        userName: username
      };
      console.log("videoInfo: ", videoInfo);
      console.log("fileInfo: ", this.fileInfo);
      videoApi
        .mergeVideo(this.fileInfo, videoInfo)
        .then((response) => {
          console.log("Received response:", response); // 打印完整响应，确保其结构
          if (response && response.data) {
            if (response.data.code === 200) {
              this.$message.success("文件上传成功：" + response.data.msg);
              this.$emit("mergeUploadProjectSuccess");
            } else {
              this.$message.error("错误信息：" + response.data.msg + ", 错误码：" + response.data.code);
            }
          } else {
            // 如果 response 或 response.data 不存在
            this.$message.success("文件上传成功：" + response.data.msg);
            this.loading = false;
          }
        })
        .catch((error) => {
          console.error("合并后捕获的异常：", error);
          this.$message.error("文件上传失败：" + error.message);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    removeFile() {
      this.$emit("removeFile");
    }
  }
};
</script>
