import axios, { AxiosInstance, AxiosError, AxiosResponse, InternalAxiosRequestConfig } from "axios";
import { ElMessage } from "element-plus";

/** 返回数据格式 */
interface ResponseData {
  hwcode: number;
  hwmsg: string;
  hwdata: {
    token: string;
    user: {
      name: string;
      role: string;
    };
  };
}

// 创建一个 axios 实例
const instance: AxiosInstance = axios.create({
  baseURL: "http://127.0.0.1:5000/api", // 确保这里的 baseURL 是 '/api' 以便通过代理转发请求
  timeout: 1000000000 // 请求超时时间
});

// 添加请求拦截器
instance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    config.headers["Content-Type"] = "application/json;charset=UTF-8";
    const authToken = localStorage.getItem("token");
    if (authToken) {
      config.headers["Authorization"] = `Bearer ${authToken}`;
    }
    return config;
  },
  (error: AxiosError) => {
    // 对请求错误进行处理
    return Promise.reject(error);
  }
);

// 添加响应拦截器
instance.interceptors.response.use(
  (response: AxiosResponse<ResponseData>) => {
    const responseData = response.data;
    if (responseData.hwcode === 0) {
      return {
        ...response,
        data: responseData.hwdata
      };
    } else {
      ElMessage.error(responseData.hwmsg);
      return Promise.reject(responseData);
    }
  },
  (error: AxiosError) => {
    if (error && error.response) {
      switch (error.response.status) {
        case 401:
          ElMessage.warning("登录已过期，请重新登录");
          localStorage.removeItem("token");
          setTimeout(() => {
            window.location.href = "/login";
          }, 1500);
          break;
        case 404:
          ElMessage.error("请求的资源不存在");
          break;
        case 500:
          ElMessage.error("服务器正在维护，请稍后重试");
          break;
        default:
          ElMessage.error(`网络错误(${error.response.status})`);
          break;
      }
    } else {
      ElMessage.error("网络连接失败，请检查您的网络");
    }
    return Promise.reject(error);
  }
);

export default instance;
