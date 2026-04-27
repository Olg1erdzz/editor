<template>
  <div>
    <header class="header">
      <input type="text" ref="searchInput" v-model="searchQuery" @keydown.enter="handleSearch" placeholder="搜索文档、模板、文库、应用、技巧..." @focus="openSearchDialog" />
    </header>
    <div style="margin-top: 15px; padding: 0">
      <!-- 首页8个图片 -->
      <div>
        <el-row :gutter="20" class="space-y-3">
          <el-col v-for="(item, index) in cardData" :key="index" :span="6" class="bg-opacity-100" >
            <div class="grid-content bg-opacity-100 rounded-xl">
              <el-card class="card">
                <div class="image-container">
                  <el-image :src="item.imageAddr" @click="toVideoPage(index)" style="width: 100%; height: 220px; border-radius: 10px"></el-image>
                  <div class="overlay">
                    <el-button @click="openTemplate(item)" size="mini" type="primary">打开模版</el-button>
                    <el-button @click="triggerFileInput(item.id)" size="mini" type="warning">更换图片</el-button>
                    <el-button @click="downloadTemplate(item)" size="mini" type="success">下载模版</el-button>
                    <input type="file" :ref="'fileInput' + item.id" style="display: none" @change="handleFileChange($event, item.id)" />
                  </div>
                </div>
                <div style="height: 20%; width: 100%">
                  <p class="titlestyle">{{ item.title }}</p>
                  <p style="color: #606266">{{ item.username }} {{ item.update_time }}</p>
                </div>
              </el-card>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import { Editor } from "@tiptap/vue-3";
import axios from "axios";

export default {
  name: "PublicPage",
  props: {
    documents: {
      type: Object,
      required: true
    },
    document: {
      type: Object,
      required: true
    },
    editor: {
      type: Editor,
      required: true
    }
  },
  data() {
    return {
      baseUrl: "",
      loading: true,
      carouselData: {},
      cardData: [],
      labelData: []
    };
  },
  created() {
    this.baseUrl = this.$store.state.baseUrl.remoteUrl || ""; // 如果不需要后端，可以留空
  },
  mounted() {
    this.init(); // 初始化数据
  },
  methods: {
    init() {
      this.$axios
        .get("http://127.0.0.1:5000/api/get_all_stencil")
        .then((response) => {
          console.log("response", response);
          if (response) {
            this.cardData = response;
            console.log(this.cardData);
            let videoLabelSet = new Set();
            for (let i = 0, len = this.cardData.length; i < len; i++) {
              let videoAddr = this.cardData[i]["videoAddr"];
              console.error(videoAddr);

              if (videoAddr && typeof videoAddr === "string") {
                let imageAddr = videoAddr.substring(0, videoAddr.lastIndexOf(".")) + ".jpg";
                this.cardData[i]["imageAddr"] = this.baseUrl + imageAddr;
                console.log(`生成的图片地址: ${this.cardData[i]["imageAddr"]}`);
                console.log(this.cardData);
                console.log(response);
                videoLabelSet.add(this.cardData[i].label);
              } else {
                console.error(`视频地址缺失或无效，ID: ${this.cardData[i].id}`);
                this.cardData[i]["imageAddr"] = "src/assets/images/10.png"; // 默认图片
              }
            }
            this.labelData = videoLabelSet;
            console.log("图片标签：", this.labelData);
            this.$message.success("刷新图片");
          } else {
            console.log("获取图片列表失败 response不为200");
            this.$message.error("获取图片列表失败 response不为200");
          }
        })
        .catch((error) => {
          console.log("获取图片列表失败原因：", error);
          this.$message.error("获取图片列表失败");
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async toVideoPage(index) {
      // const cardData = await axios.get("http://127.0.0.1:5000/api/get_all_stencil")
      // console.log(cardData);
      let videoData = cardData[index];
      console.log(videoData);
      console.log("公共页-图片页-传递数据-图片ID：", videoData.id);
      console.log("公共页-图片页-传递数据-用户ID：", videoData.username); // 输出用户ID
      this.$router.push({
        path: "/videoPage",
        query: {
          videoDataId: videoData.id,
          videoDataAddr: videoData.videoAddr,
          username: videoData.username // 传递用户ID
        }
      });
    },
    async openTemplate(item) {
      console.log("打开模版", item);
      const username = localStorage.getItem("userName") || "unknown_user";
      console.log(item.username);
      console.log(item.title);
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/open_stencil", {
          params: {
            username: item.username,
            name: item.title,
          },
          headers: {
            "Content-Type": "application/json"
          }
        });

        // if (response.data.code === 200) {
        //   const filePath = response.data.file_path;
        //   const fileResponse = await axios.get(`http://localhost:5000/${filePath}`, {
        //     responseType: 'blob'  // 确保接收的是二进制数据
        //   });

          // 将文件内容读取为文本
          // reader.onload = (e) => {
          //   const documentContent = e.target.result;
            const documentContent = response
            console.log(documentContent)
            // 更新导航栏信息
            // const newDocument = {
            //   id: Date.now().toString(),
            //   title: item.name,
            //   path: `/documents/${Date.now()}`,//有可能造成冲突，后可以采用uuid随机编码
            //   isOpen: true,
            //   content: documentContent // 包含从后端获取的模版内容
            // };
            const newDocument = {
                id: Date.now().toString(),
                title: item.title,
                path: `/documents/${Date.now()}`,
                isOpen: true,
                username: username,
                content:documentContent
              };
            console.log(newDocument)
            item.isOpen = true; // 更新当前模版的 isOpen 状态
            this.$emit("add-document", newDocument);
            this.$router.push({
              path: newDocument.path,
              query: {
                title: item.title,
                content: documentContent // 将内容作为查询参数传递
              }
            });
          // };
          // reader.readAsText(fileResponse.data);
        // } else {
        //   this.$message.error(response.data.msg);
        // }
      } catch (error) {
        this.$message.error("打开模版时发生错误");
        console.error("Error opening template:", error);

        // 无论是否发生错误，都继续跳转
        const newDocument = {
          id: item.id,
          title: item.title,
          path: `/documents/${item.id}`,
          isOpen: true,
          content: "" // 由于发生错误，内容为空
        };
        item.isOpen = true; // 更新当前模版的 isOpen 状态
        this.$emit("add-document", newDocument);
        this.$router.push({
          path: newDocument.path,
          query: {
            title: item.title,
            content: "" // 内容为空
          }
        });
      }
    },
    triggerFileInput(itemId) {
      this.$refs[`fileInput${itemId}`][0].click();
    },
    handleFileChange(event, itemId) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const imageDataUrl = e.target.result;
          const item = this.cardData.find((item) => item.id === itemId);
          if (item) {
            item.imageAddr = imageDataUrl;
          }
        };
        reader.readAsDataURL(file);
      }
    },
    async downloadTemplate(item) {
      console.log("免费下载模版", item);
      const username = localStorage.getItem("userName") || "unknown_user";
      console.log(item.username);
      console.log(item.name);
      try{
        const response = await axios.get("http://127.0.0.1:5000/api/open_stencil", {
          params: {
            username: item.username,
            name: item.title,
          },
          headers: {
            "Content-Type": "application/json"
          }
        });

        const response1 = await axios.post("http://127.0.0.1:5000/api/save", 
        {
            username: username,
            file_name: item.title + '（新）',
            text: response,
        },
        {  headers: {
            "Content-Type": "application/json"
          }
        });
      }catch(error)
      {
        console.log('failed to download')
      }
    }
  }
};
</script>

<style scoped>
.card {
  max-height: 350px;
}
/* 图片标题 */
.titlestyle {
  font-weight: bold;
}

.el-row {
  margin-bottom: 20px;
}

.el-col {
  border-radius: 4px;
}

.bg-purple {
  background: #d3dce6;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}

/* 图片悬浮效果 */
.image-container {
  position: relative;
}

.image-container .overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 10px;
}

.image-container:hover .overlay {
  opacity: 1;
}

.overlay .el-button {
  margin: 0 5px;
}
</style>
