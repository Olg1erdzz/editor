// src/api/user.ts
import instance from "../request/http";

/** 注册新用户 */
export async function register(params: { username: string; email: string; password: string; role: string }) {
  return await instance({
    url: "/entportal/v1/register",
    method: "post",
    data: { ...params }
  });
}

/** 用户登录 */
export async function login(params: { username: string; password: string }) {
  return await instance({
    url: "/entportal/v1/login",
    method: "post",
    data: { ...params }
  });
}
/** 确认账户是否存在 */
export async function confirmAccount(params: { email: string }) {
  return await instance({
    url: "/entportal/v1/confirmAccount",
    method: "post",
    data: { ...params }
  });
}

/** 发送验证码 */
export async function sendSms(params: { email: string }) {
  return await instance({
    url: "/entportal/v1/sendSms",
    method: "post",
    data: { ...params }
  });
}

/** 重置密码 */
export async function resetPassword(params: { email: string; newPassword: string; code: string }) {
  return await instance({
    url: "/entportal/v1/user/password",
    method: "put",
    data: { ...params }
  });
}