import axios from "./axios";

const blogCommentApi = {
  publishBlogComment(blogCommentDto) {
    return axios.post("/blogComment/publishBlogComment", blogCommentDto);
  },

  deleteBlogComment(blogCommentId) {
    return axios.get("/blogComment/deleteBlogComment?blogCommentId=" + blogCommentId);
  }
};

export default blogCommentApi;
