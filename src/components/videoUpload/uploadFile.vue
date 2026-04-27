<template>
  <div>
    <!-- 上传器 -->
    <uploader
      ref="uploader"
      v-loading="loading"
      element-loading-text="正在上传模版，请稍等~"
      :options="options"
      :auto-start="false"
      :file-status-text="fileStatusText"
      @file-added="onFileAdded"
      @file-success="onFileSuccess"
      @file-progress="onFileProgress"
      @file-error="onFileError"
      @file-removed="fileRemoved"
      class="uploader-example"
    >
      <uploader-unsupport></uploader-unsupport>
      <uploader-drop>
        <div>
          <uploader-btn id="global-uploader-btn" ref="uploadBtn" v-show="!fileSuccess">
            选择文件
            <i class="el-icon-upload el-icon--right"></i>
          </uploader-btn>
        </div>
      </uploader-drop>
      <uploader-list></uploader-list>
    </uploader>
  </div>
</template>

<script>
import SparkMD5 from "spark-md5";

export default {
  name: "uploadFile",
  data() {
    return {
      loading: false,
      fileSuccess: false,
      options: {
        target: this.$store.state.baseUrl.remoteUrl + "api/video/upload/chunk",
        headers: {
          token: localStorage.getItem("token")
        },
        singleFile: true,
        chunkSize: "2048000",
        fileParameterName: "chunkFile",
        maxChunkRetries: 3,
        testChunks: false
      },
      fileStatusText: {
        success: "上传成功",
        error: "上传失败",
        uploading: "上传中",
        paused: "暂停",
        waiting: "等待上传"
      }
    };
  },
  methods: {
    onFileAdded(file) {
      this.loading = true;
      const supportedFileTypes = ["video/mp4", "video/ogg", "video/flv", "video/avi", "video/wmv", "video/rmvb", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
      if (supportedFileTypes.indexOf(file.fileType) === -1) {
        this.$message.error("不支持" + file.fileType + "格式，请上传支持的文件格式");
        file.ignored = true;
      } else {
        this.$message.success("文件格式验证成功！");
        this.$emit("checkFileSuccess", file);
      }
      this.loading = false;
    },
    computeMD5(file) {
      console.log("file=", file); // 获取用户选择上传的文件
      file.pause();
      let fileSizeLimit = 50 * 1024 * 1024 * 1024;
      if (file.size > fileSizeLimit) {
        this.$message({
          duration: 7,
          message: "文件大小不能超过50G",
          type: "warning"
        });
        file.cancel();
      }

      let fileReader = new FileReader();
      let time = new Date().getTime();
      let blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice;
      console.log("blobSlice=", blobSlice);
      let currentChunk = 0;
      const chunkSize = 10 * 1024 * 1000;
      let chunks = Math.ceil(file.size / chunkSize);
      console.log("chunks=", chunks);
      console.log("chunkSize=", chunkSize);
      let spark = new SparkMD5.ArrayBuffer();
      let chunkNumberMD5 = 1;

      loadNext();

      fileReader.onload = (e) => {
        spark.append(e.target.result);

        if (currentChunk < chunkNumberMD5) {
          loadNext();
        } else {
          let md5 = spark.end();
          file.uniqueIdentifier = md5;
          file.resume();
          console.log(`MD5计算完毕：${file.name} \nMD5：${md5} \n分片数量：${chunks} 文件大小:${file.size} 分片用时：${new Date().getTime() - time} ms`);
        }
      };

      fileReader.onerror = () => {
        this.$message.error(`文件${file.name}读取出错，请检查该文件`);
        file.cancel();
      };

      function loadNext() {
        let start = currentChunk * chunkSize;
        let end = start + chunkSize >= file.size ? file.size : start + chunkSize;
        fileReader.readAsArrayBuffer(blobSlice.call(file.file, start, end));
        currentChunk++;
        console.log("计算第" + currentChunk + "块");
      }
    },
    onFileSuccess(rootFile, file, response, chunk) {
      console.log({
        "success-rootFile: ": rootFile,
        "success-file: ": file,
        "success-response: ": response,
        "success-chunk: ": chunk
      });
      console.log("文件上传成功-success");
      let fileInfo = {};
      fileInfo.id = file.id;
      fileInfo.fileType = file.fileType;
      fileInfo.name = file.name;
      fileInfo.size = file.size;
      fileInfo.relativePath = file.relativePath;
      fileInfo.uniqueIdentifier = file.uniqueIdentifier;
      this.$emit("computeMD5FileSuccess", fileInfo);
    },
    onFileProgress(rootFile, file, chunk) {
      console.log(`上传中 ${file.name}，chunk：${chunk.startByte / 1024 / 1024} ~ ${chunk.endByte / 1024 / 1024}`);
    },
    onFileError(rootFile, file, response, chunk) {
      console.log("上传完成后异常信息：" + response);
      console.log({
        "error-rootFile: ": rootFile,
        "error-file: ": file,
        "error-response: ": response,
        "error-chunk: ": chunk
      });
    },
    fileRemoved() {
      this.$emit("removeFile");
    }
  }
};
</script>

<style>
.uploader-example {
  width: 880px;
  padding: 15px;
  margin: 40px auto 0;
  font-size: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
}
.uploader-example .uploader-btn {
  margin-right: 4px;
}
.uploader-example .uploader-list {
  max-height: 440px;
  overflow: auto;
  overflow-x: hidden;
  overflow-y: auto;
}
</style>
