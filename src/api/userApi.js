import axios from "./axios";

const userApi = {
  updateInfo(nickName) {
    return axios.get("/user/updateNickName?nickName=" + (nickName || ""));
  }
};

export default userApi;
