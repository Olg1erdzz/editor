<template>
  <!--  <Home v-if="$route.meta.showNavbar" :documents="documents" :document="document" @remove-document="removeDocument" :editor="editor" />-->
  <div class="main">
    <header-component class="header" :document="document" :editor="editor"></header-component>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import headerComponent from "../../components/headerComponent.vue";
import Home from "@/components/Home.vue";
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Layout",
  components: { headerComponent },
  data() {
    return {
      editor: {
        type: Object,
        required: true
      },
      document: [],
      documents: [], // 存储文档的数组
      currentDocument: null // 当前文档对象
    };
  },
  mounted() {
    // console.log('layout-router-params: ', this.$route.query.msg)
  }
};
</script>
<style lang="less" scoped>
.main {
  // display: flex;
  // background-color: aquamarine;
  width: 100%;
  height: auto;
}
.header {
  width: 100%;
  height: 13%;
}

.content {
  //background-color: bisque;
  width: 100%;
  height: 85%;
}
</style>
