import axios from "./axios";

const noteApi = {
  getPublicNoteList(pageNum, pageSize, content) {
    return axios.get("/note/getPublicNoteList?content=" + (content || "") + "&pageNum=" + (pageNum || 1) + "&pageSize=" + (pageSize || 10));
  }
};

export default noteApi;
