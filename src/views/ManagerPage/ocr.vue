<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="80px" v-loading="loading">
      <el-form-item label="选择图片" prop="picturePath">
        <image-upload v-model="form.picturePathText" :limit="20" />
      </el-form-item>
      <template>
        <el-form-item v-for="(item, index) of content" :label="'识别结果' + (index + 1)" :key="'content' + index">
          <el-input type="textarea" :show-word-limit="true" :autosize="{ minRows: 3, maxRows: 20 }" v-model="content[index]" readonly />
        </el-form-item>
      </template>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="submitForm">执行OCR</el-button>
      <el-button @click="reset">重 置</el-button>
      <el-button @click="annotation">标注</el-button>
    </div>
  </div>
</template>

<script>
import { addPicture } from "@/api/ocr/picture";

export default {
  name: "ocr",
  data() {
    return {
      form: {},
      loading: !1,
      content: []
    };
  },
  created() {},
  methods: {
    submitForm: function () {
      this.loading = !0;
      addPicture(this.form).then((response) => {
        this.$modal.msgSuccess("识别成功");
        let data_ = response.data;
        data_.forEach((i) => {
          this.content.push(i["wordsResult"]?.join("\n"));
        });
        this.loading = !1;
      });
    },
    reset() {
      this.form = {
        picturePathText: undefined
      };
      this.content = [];
      this.resetForm("form");
    }
  }
};
</script>
