import axios from "./axios";

const videoApi = {
  getVideo(videoId) {
    return axios.get("/video/getVideo?videoId=" + (videoId || 0));
  },

  checkVideoName(fileName) {
    return axios.post("/video/checkName", { title: fileName || "" });
  },

  mergeVideo(fileInfo, videoInfo) {
    return axios.post("/video/merge", { fileInfo: fileInfo, videoInfo: videoInfo });
  },

  getVideoListByLabel(label) {
    return axios.post("/video/getVideoListByLabel", { label: label });
  },

  getVideoList() {
    return axios.post("/video/getVideoList");
  },

  // 不去后端请求，而是把网址拼接好返回给调用这个的函数
  downloadVideo(videoUrl) {
    return axios.defaults.baseURL + "/video/downloadVideo?videoUrl=" + videoUrl;
  }
};

export default videoApi;
