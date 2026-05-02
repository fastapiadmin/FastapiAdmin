/**
 * 认证相关便捷接口（示例页等使用 `@/api/auth` 路径导入）
 * 实现委托至 `@/api/module_system/auth` / `user`
 */
import AuthAPI, { type LoginFormData } from "@/api/module_system/auth";
import UserAPI, { type UserInfo } from "@/api/module_system/user";
import { ResultEnum } from "@/enums/api/result.enum";

export interface FetchLoginParams {
  userName: string;
  password: string;
}

export async function fetchLogin(params: FetchLoginParams): Promise<{
  token: string;
  refreshToken: string;
}> {
  const captchaRes = await AuthAPI.getCaptcha();
  const captchaInfo = captchaRes.data?.data;

  const loginForm: LoginFormData = {
    username: params.userName,
    password: params.password,
    captcha_key: captchaInfo?.key ?? "",
    captcha: "",
    remember: false,
    login_type: "PC端",
  };

  const response = await AuthAPI.login(loginForm);
  if (response.data.code !== ResultEnum.SUCCESS || !response.data.data) {
    throw new Error(response.data.msg || "登录失败");
  }

  const data = response.data.data;
  return {
    token: data.access_token,
    refreshToken: data.refresh_token,
  };
}

/** 使用当前请求上下文中的 token 拉取用户信息（与 store.getUserInfo 数据来源一致） */
export async function fetchGetUserInfo(): Promise<UserInfo> {
  const response = await UserAPI.getCurrentUserInfo();
  if (response.data.code !== ResultEnum.SUCCESS || response.data.data == null) {
    throw new Error(response.data.msg || "获取用户信息失败");
  }

  const raw = response.data.data;
  const next = { ...raw };
  delete next.menus;
  return next as UserInfo;
}
