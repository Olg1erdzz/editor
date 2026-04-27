<template>
  <div>
    <quill-editor theme="snow"> </quill-editor>

    <div>222</div>
  </div>
</template>

<script>
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import { quillEditor } from "vue-quill-editor";

export default {
  components: {
    quillEditor
  }
};
</script>

<style scoped lang="less">
/* Your custom styles go here */
</style>
