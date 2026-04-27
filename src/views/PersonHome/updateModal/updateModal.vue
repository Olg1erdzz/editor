<template>
  <div class="update-modal">
    <el-dialog title="修改用户信息" v-model:visible="centerDialogVisible" width="45%" center>
      <div class="data-div">
        <el-input class="nickname-input" v-model="nickName" placeholder="请输入昵称"></el-input>
        <el-avatar v-if="!isUpload" shape="square" :size="200" :src="avatarAddr" @click.native="isUpload = true"></el-avatar>
        <image-upload v-else ref="image-upload" :nickName="nickName"></image-upload>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitUpload">保 存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import imageUpload from "./imageUpload.vue";
import userApi from "../../../api/userApi.js";
export default {
  components: { imageUpload },
  props: {
    // 控制是否打开dialog
    isShowUpdateModal: Boolean
  },
  model: {
    prop: "isShowUpdateModal",
    event: "changeModalStatus"
  },
  watch: {
    // 监听centerDialogVisible, 对应修改isShowUpdateModal, 并传值给父组件
    centerDialogVisible: {
      immediate: true,
      handler(newValue) {
        this.$emit("changeModalStatus", newValue);
      }
    },
    isHaveFile: {
      immediate: true,
      handler(newValue) {
        console.log("是否上传了文件", newValue);
      }
    }
  },
  data() {
    return {
      // 控制显示当前头像还是上传新的头像
      isUpload: false,
      // 控制当前上传组件是否上传了文件
      isHaveFile: false,
      // 子组件不能修改props下的变量，所以定义一个对应的临时变量
      centerDialogVisible: this.isShowUpdateModal,
      // 用户昵称
      nickName: "",
      // 用户头像
      avatarAddr: ""
    };
  },
  created() {
    // 添加默认当前昵称
    this.nickName = localStorage.getItem("nickName");
    // 设置默认显示的头像
    this.avatarAddr = this.$store.state.baseUrl.remoteUrl + localStorage.getItem("avatarAddr");
  },
  methods: {
    submitUpload() {
      // 如果用户没有上传头像文件，则使用更新用户昵称的请求
      if (!this.isHaveFile) {
        if (!this.nickName) {
          this.$message.warning("请填写用户昵称");
          return;
        }
        userApi
          .updateInfo(this.nickName)
          .then((res) => {
            this.centerDialogVisible = false;
            this.$message.success("保存成功");
          })
          .catch((err) => {
            console.log("更新用户信息（用户昵称）失败", err);
          });
      } else {
        // 如果需要更新用户昵称和头像，则用el的上传组件去发送请求
        // 上传更新的用户信息
        this.$refs["image-upload"].submitUpload();
      }
    }
  }
};
</script>

<style>
.update-modal .data-div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.update-modal .nickname-input {
  width: 70%;
}
</style>
