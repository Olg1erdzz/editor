import axios from "./axios";

const managerApi = {
  getVideoInfoList(content, currentPage, pageSize) {
    return axios.get("/manager/getVideoInfoList?content=" + (content || "") + "&currentPage=" + (currentPage || 1) + "&pageSize=" + (pageSize || 5));
  },
  checkVideo(videoId, action) {
    return axios.get("/manager/checkVideo?videoId=" + (videoId || 0) + "&action=" + (action || ""));
  }
};

export default managerApi;
