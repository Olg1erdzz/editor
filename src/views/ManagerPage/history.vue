<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="关键字" prop="content">
        <el-input v-model="queryParams.content" placeholder="请输入关键字" clearable size="small" style="width: 240px" @keyup.enter.native="handleQuery" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>
    <el-row :gutter="10" class="mb8">
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>
    <el-table v-loading="loading" :data="list">
      <el-table-column label="图片名称" align="center" prop="pictureName" width="320" />
      <el-table-column label="图片类型" align="center" prop="pictureType" width="80" />
      <el-table-column label="图片路径" align="center" prop="picturePath" :show-overflow-tooltip="true">
        <template v-slot="scope">
          <el-popover width="600" trigger="click">
            <el-image :src="baseUrl + scope.row.picturePath" :alt="scope.row.picturePath" />
            <el-link slot="reference" type="primary">{{ scope.row.picturePath }}</el-link>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="识别内容" align="center" prop="content" :show-overflow-tooltip="true">
        <template v-slot="scope">
          <el-link @click="showDetail(scope.row.wordsResult)" slot="reference" type="primary">{{ scope.row.content }} </el-link>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" prop="createTime" width="100">
        <template v-slot="scope">
          <span>{{ parseTime(scope.row.createTime, "{y}-{m}-{d}") }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="80" class-name="small-padding fixed-width">
        <template v-slot="scope">
          <el-button size="mini" type="text" icon="el-icon-delete" @click="handleDelete(scope.row)">删除 </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize" @pagination="getList" />
    <el-dialog title="PaddleOCR详情" v-model:visible="dialogVisible">
      <div style="margin: 0 1em; font-size: 14px">
        <div v-html="text"></div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" v-clipboard:copy="text" v-clipboard:success="clipboardSuccess">复 制</el-button>
        <el-button @click="dialogVisible = false">取 消</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { deleteRow, list } from "@/api/ocr/picture";

export default {
  name: "history",
  data() {
    return {
      dialogVisible: false,
      showSearch: true,
      // baseUrl: process.env.VUE_APP_BASE_API,
      // 遮罩层
      loading: true,
      // 总条数
      total: 0,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        content: undefined
      },
      // 表格数据
      list: [],
      text: ""
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询列表 */
    getList() {
      this.loading = true;
      list(this.queryParams).then((response) => {
        this.list = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    showDetail(content) {
      this.text = content.join("<br />");
      this.dialogVisible = !0;
    },
    handleDelete(row) {
      this.$modal
        .confirm('是否确认当前id为："' + row.id + '"的数据项？')
        .then(function () {
          return deleteRow(row.id);
        })
        .then(() => {
          this.getList();
          this.$modal.msgSuccess("删除成功");
        })
        .catch(() => {});
    },
    clipboardSuccess() {
      this.$modal.msgSuccess("复制成功");
    }
  }
};
</script>
