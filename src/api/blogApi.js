import axios from "./axios";

const blogApi = {
  publishBlog(blogDto) {
    return axios.post("/blog/publishBlog", blogDto);
  },

  searchBlogs(pageNum, pageSize, blogDto) {
    return axios.post("/blog/searchBlogs?pageNum=" + (pageNum || 1) + "&pageSize=" + (pageSize || 10), blogDto);
  },

  getBlogsByUser(pageNum, pageSize, userId) {
    return axios.get("/blog/getBlogsByUser?pageNum=" + (pageNum || 1) + "&pageSize=" + (pageSize || 10) + "&userId=" + userId);
  },

  getBlogInfoAndComment(blogId) {
    return axios.get("/blog/getBlogInfoAndComment?blogId=" + blogId);
  },

  deleteBlog(blogId) {
    return axios.get("/blog/deleteBlog?blogId=" + blogId);
  }
};

export default blogApi;
