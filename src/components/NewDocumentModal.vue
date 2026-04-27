<template>
  <div class="modal" v-if="visible">
    <div class="modal-content">
      <div class="modal-header">
        <span class="close" @click="close">&times;</span>
        <h2>新建</h2>
      </div>
      <div class="modal-body">
        <div class="categories">
          <h3>Office文档</h3>
          <div class="icons">
            <div class="icon"><img src="word-icon.png" alt="Word" />文字</div>
            <div class="icon"><img src="ppt-icon.png" alt="PPT" />演示</div>
            <div class="icon"><img src="excel-icon.png" alt="Excel" />表格</div>
            <div class="icon"><img src="pdf-icon.png" alt="PDF" />PDF</div>
          </div>
          <h3>在线文档</h3>
          <div class="icons">
            <div class="icon"><img src="smart-doc-icon.png" alt="Smart Doc" />智能文档</div>
            <div class="icon"><img src="smart-excel-icon.png" alt="Smart Excel" />智能表格</div>
            <div class="icon"><img src="smart-form-icon.png" alt="Smart Form" />智能表单</div>
          </div>
          <h3>应用服务</h3>
          <div class="icons">
            <div class="icon"><img src="multi-sheet-icon.png" alt="Multi Sheet" />多维表格</div>
            <div class="icon"><img src="mind-map-icon.png" alt="Mind Map" />思维导图</div>
            <div class="icon"><img src="flowchart-icon.png" alt="Flowchart" />流程图</div>
            <div class="icon"><img src="design-icon.png" alt="Design" />设计</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    close() {
      this.$emit("close");
    }
  }
};
</script>

<style scoped>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: #fff;
  width: 50%;
  height: 50%;
  margin: auto;
  padding: 20px;
  border-radius: 8px;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close {
  color: #aaa;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.categories {
  margin-top: 20px;
}

.icons {
  display: flex;
  justify-content: space-around;
  margin: 10px 0;
}

.icon {
  text-align: center;
}

.icon img {
  width: 50px;
  height: 50px;
  display: block;
  margin: 0 auto 5px;
}
</style>
