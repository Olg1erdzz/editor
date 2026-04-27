<template>
  <div>
    <div class="videoShoe" v-if="isShowVideo">
      <!--            :before-close="handleClose"-->
      <el-dialog v-model:visible="isShowVideo" title="视频审核" width="60%" style="text-align: center">
        <video-check :videoUrl="videoAddr"></video-check>
        <el-divider></el-divider>
        审核内容：<el-input v-model="videoCheckText" placeholder="请输入审核内容" style="width: 60%"></el-input>
        <span class="dialog-footer" slot="footer">
          <el-button @click="isShowVideo = false">取 消</el-button>
          <el-button @click="isShowVideo = false" type="primary">确 定</el-button>
        </span>
      </el-dialog>
    </div>
    <div class="video_header">
      <el-row>
        <el-col :span="2">
          <!--                    管理员页面暂时不需要添加功能-->
          <!--                    <el-button plain type="primary">添加</el-button>-->
        </el-col>
        <el-col :offset="10" :span="14">
          <div style="display: flex; justify-content: right; align-items: center">
            <el-input placeholder="请输入内容" style="width: 60%" v-model="searchText"></el-input>
            <el-button icon="el-icon-search" style="margin-left: 10px" type="primary" @click="search">搜索</el-button>
          </div>
        </el-col>
      </el-row>
    </div>
    <el-divider></el-divider>
    <div class="video_content">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column label="更新日期" prop="updateTime" width="180"> </el-table-column>
        <el-table-column label="视频名称" prop="title" width="180"> </el-table-column>
        <el-table-column label="标签" prop="label"> </el-table-column>
        <el-table-column label="发布作者" prop="username"> </el-table-column>
        <el-table-column label="视频">
          <template v-slot="scope">
            <el-image :src="baseUrl + scope.row.imageAddr" @click="showVideo(scope.row.videoAddr)" style="width: 100px; height: 100px"> </el-image>
          </template>
        </el-table-column>
        <el-table-column
          :filter-method="filterTag"
          :filters="[
            { text: '已通过', value: 0 },
            { text: '待审核', value: 1 },
            { text: '未通过', value: 2 }
          ]"
          filter-placement="bottom-end"
          label="审核状态"
          prop="status"
          width="100"
        >
          <template v-slot="scope">
            <el-tag :type="scope.row.status === 0 ? 'success' : scope.row.status === 1 ? 'warning' : 'danger'" disable-transitions>
              <span v-if="scope.row.status === 0">已通过</span>
              <span v-else-if="scope.row.status === 1">待审核</span>
              <span v-else>未通过</span>
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template v-slot="scope">
            <el-button @click="checkVideo(scope.$index, scope.row, 'pass')" size="mini">通过 </el-button>
            <el-button @click="checkVideo(scope.$index, scope.row, 'forbid')" size="mini" type="danger">禁止 </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="text-align: right">
        <el-pagination :page-size="pageSize" :total="total" @current-change="pageChange" background layout="prev, pager, next"> </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import VideoCheck from "./VideoCheck.vue";
import managerApi from "../../api/managerApi";
export default {
  name: "VideoManagerPage",
  components: {
    VideoCheck
  },
  data() {
    return {
      baseUrl: "",
      isShowVideo: false,
      searchText: "",
      videoCheckText: "",
      pageSize: 5,
      total: 5,
      currentPage: 1,
      videoAddr: "",
      tableData: []
    };
  },
  created() {
    this.baseUrl = this.$store.state.baseUrl.remoteUrl;
    console.log("基础地址：", this.baseUrl);
  },
  mounted() {
    this.getList(1);
  },
  methods: {
    showVideo(videoAddr) {
      this.videoAddr = videoAddr;
      console.log("传入的视频地址：", this.videoAddr);
      this.isShowVideo = true;
    },
    filterTag(value, row) {
      console.log("行数据：", value, row);
      return row.status === value;
    },
    checkVideo(index, row, action) {
      console.log("审核视频操作：", index, row, action);
      managerApi
        .checkVideo(row.id, action)
        .then((response) => {
          this.$message.success(response.data.msg);
          console.log("现在的页：", this.currentPage);
          this.getList(this.currentPage);
        })
        .catch((error) => {
          this.$message.error("审核视频错误内容为：" + error);
        });
    },
    pageChange(currentPage) {
      console.log("当前页数：", currentPage);
      this.currentPage = currentPage;
      this.getList(currentPage);
    },
    getList(currentPage) {
      managerApi
        .getVideoInfoList(this.searchText, currentPage, this.pageSize)
        .then((response) => {
          console.log("视频审理信息", response.data);
          this.pageSize = response.data.data.pageSize;
          this.total = response.data.data.total;
          this.tableData = [];
          response.data.data.videoInfo.forEach((video) => {
            let videoObject = new Object();
            videoObject.id = video.id;
            videoObject.updateTime = video.updateTime;
            videoObject.title = video.title;
            videoObject.label = video.label;
            videoObject.username = video.username;
            videoObject.status = video.status;
            videoObject.videoAddr = video.videoAddr;
            videoObject.imageAddr = video.videoAddr.substr(0, video.videoAddr.indexOf(".mp4")) + ".jpg";
            this.tableData.push(videoObject);
          });
          // console.log("视频审核信息处理后的数据：", this.tableData)
        })
        .catch((error) => {
          console.log("获取视频审核信息失败,错误为：", error);
          this.$message.error("获取视频审核信息失败,错误为：" + error);
        });
    },
    search() {
      this.getList(1);
    }
  }
};
</script>

<style scoped></style>
