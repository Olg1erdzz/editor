import axios from "axios";
import Element from "element-plus";
import store from "../store";
import router from "../router";

// 设置基础URL，确保与后端API一致
axios.defaults.baseURL = "http://127.0.0.1:5000/api/"; // 这里设置为你的后端地址

// 前置拦截器
axios.interceptors.request.use(
  (config) => {
    // 排除登录和注册请求，其他请求都添加token
    const publicUrls = ["/entportal/v1/login", "/entportal/v1/register"];
    if (config.url && !publicUrls.includes(config.url)) {
      const token = localStorage.getItem("token");
      if (token) {
        if (config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        } else {
          config.headers = { Authorization: `Bearer ${token}` };
        }
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 后置拦截器
axios.interceptors.response.use(
  (response) => {
    const res = response.data;
    if (res.hwcode === 0) {
      // 返回成功响应
      return res.hwdata;
    } else if (res.code === 200) {
      return response;
    } else {
      return response;
      /* // 显示错误信息
      Element.Message.error(res.hwmsg, { duration: 1000 });
      return Promise.reject(res.hwmsg);*/
    }
  },
  (error) => {
    console.log("axios.js后置拦截错误", error);
    if (error.response) {
      if (error.response.data) {
        error.message = error.response.data.hwmsg;
      }
      if (error.response.status === 401) {
        store.commit("REMOVE_INFO");
        router.push("/login");
      }
      Element.Message.error(error.message, { duration: 1000 });
    } else {
      Element.Message.error("网络连接失败，请检查您的网络", { duration: 1000 });
    }
    return Promise.reject(error.message);
  }
);

export default axios;
