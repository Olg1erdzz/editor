<template>
  <div>
    <el-menu :collapse="isCollapse" default-active="1" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
      <h2 v-if="!isCollapse">管理中心</h2>
      <el-menu-item index="1" @click="toPage('video')">
        <i class="el-icon-setting"></i>
        <span slot="title">视频管理</span>
      </el-menu-item>
      <el-menu-item index="2" @click="toPage('ocr')">
        <i class="el-icon-setting"></i>
        <span slot="title">识别管理</span>
      </el-menu-item>
      <el-menu-item index="3" @click="toPage('Ocrhistory')">
        <i class="el-icon-setting"></i>
        <span slot="title">识别历史管理</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "SideComponent",
  data() {
    return {
      isCollapse: false
    };
  },
  methods: {
    toPage(type) {
      if (type === "video") {
        if (this.$route.name !== "VideoManagerPage") {
          this.$router.push("/videoManagerPage");
        }
      } else if (type === "ocr") {
        if (this.$route.name !== "Ocr") {
          this.$router.push("/ocr");
        }
      } else if (type === "Ocrhistory") {
        if (this.$route.name !== "Ocrhistory") {
          this.$router.push("/ocrhistory");
        }
      }
    }
  }
};
</script>

<style lang="less" scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 100%;
  min-height: 1000px;
}
.el-menu {
  height: 100%;
  border: none;
  h2 {
    color: #fff;
    text-align: center;
    line-height: 48px;
  }
}
</style>
