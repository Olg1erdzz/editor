<style></style>

<template>
  <div>
    <el-upload class="avatar-uploader" ref="upload" drag :action="targetUrl" :headers="headers" :data="userInfo" :auto-upload="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload" :before-remove="beforeRemove">
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将头像拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过2MB</div>
    </el-upload>
  </div>
</template>

<script>
export default {
  props: {
    // 用户名
    nickName: String
  },
  watch: {
    nickName(newValue) {
      this.userInfo.nickName = newValue;
    }
  },
  data() {
    return {
      targetUrl: this.$store.state.baseUrl.remoteUrl + "user/updateInfo",
      headers: {
        token: localStorage.getItem("token")
      },
      userInfo: {
        nickName: this.nickName
      }
    };
  },
  methods: {
    handleAvatarSuccess(res, file) {
      // this.imageUrl = URL.createObjectURL(file.raw);
      this.$parent.$parent.centerDialogVisible = false;
      this.$message.success("保存成功");
    },
    beforeAvatarUpload(file) {
      // const isJPG = file.type === 'image/jpeg' || file.type === 'image/png';
      const isJPG = file.type === "image/png";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error("上传头像图片只能是 jpg 或 png 格式!");
      }
      if (!isLt2M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
      }

      // 设置已经上传了文件
      this.$parent.$parent.isHaveFile = true;

      return isJPG && isLt2M;
    },
    beforeRemove() {
      // 设置还没有上传文件
      this.$parent.$parent.isHaveFile = false;
    },
    submitUpload() {
      this.$refs.upload.submit();
    }
  }
};
</script>
