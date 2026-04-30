import { ApiHeader } from '@/enums/api-header.enum'
import { http } from '@/http'

const USER_BASE_URL = '/system/user'

const UserAPI = {
  /**
   * 个人中心用户信息
   *
   * @returns 登录用户昵称、头像信息，包括角色和权限
   */
  getCurrentUserInfo(): Promise<UserInfo> {
    return http.Get(`${USER_BASE_URL}/current/info`)
  },

  /**
   * 当前用户头像上传
   *
   * @param body
   * @returns 上传后的文件路径
   */
  uploadCurrentUserAvatar(body: any): Promise<UploadFileResult> {
    return http.Post(`${USER_BASE_URL}/current/avatar/upload`, body, {
      headers: {
        [ApiHeader.KEY]: ApiHeader.MULTIPART,
      },
    })
  },

  /**
   * 修改个人中心用户信息
   *
   * @param body
   * @returns 修改后的用户信息
   */
  updateCurrentUserInfo(body: UserProfileForm): Promise<UserInfo> {
    return http.Put(`${USER_BASE_URL}/current/info/update`, body)
  },

  /**
   * 修改个人中心用户密码
   *
   * @param body
   * @returns 修改后的用户信息
   */
  changeCurrentUserPassword(body: PasswordChangeForm): Promise<ApiResponse> {
    return http.Put(`${USER_BASE_URL}/current/password/change`, body)
  },

  /**
   * 注册用户
   *
   * @param body
   * @returns 忘记密码结果
   */
  registerUser(body: RegisterForm): Promise<ApiResponse> {
    return http.Post(`${USER_BASE_URL}/register`, body)
  },

  /**
   * 忘记密码
   *
   * @param body
   * @returns 忘记密码结果
   */
  forgetPassword(body: ForgetPasswordForm): Promise<ApiResponse> {
    return http.Post(`${USER_BASE_URL}/forget/password`, body)
  },

  /**
   * 获取用户分页列表
   *POST
   * @param queryParams 查询参数
   */
  getUserPage(queryParams: UserPageQuery): Promise<PageResult<UserInfo[]>> {
    return http.Get(`${USER_BASE_URL}/list`, queryParams)
  },

  /**
   * 获取用户表单详情
   *
   * @param userId 用户ID
   * @returns 用户表单详情
   */
  getUserDetail(userId: number): Promise<UserForm> {
    return http.Get(`${USER_BASE_URL}/detail/${userId}`)
  },

  /**
   * 添加用户
   *
   * @param body 用户表单数据
   */
  addUser(body: UserForm): Promise<ApiResponse> {
    return http.Post(`${USER_BASE_URL}/create`, body)
  },

  /**
   * 修改用户
   *
   * @param body 用户表单数据
   */
  updateUser(body: UserForm): Promise<ApiResponse> {
    return http.Put(`${USER_BASE_URL}/update`, body)
  },

  /**
   * 删除用户
   *
   * @param ids 用户ID数组
   */
  deleteUser(ids: number[]): Promise<ApiResponse> {
    return http.Delete(`${USER_BASE_URL}/delete`, ids)
  },
}

export default UserAPI

/* 忘记密码表单 */
export interface ForgetPasswordForm {
  username: string
  new_password: string
  confirmPassword: string
}

/* 注册表单 */
export interface RegisterForm {
  username: string
  password: string
  confirmPassword: string
}

/* 分页查询表单 */
export interface UserPageQuery extends PageQuery {
  username?: string
  name?: string
  status?: boolean
  dept_id?: number
  start_time?: string
  end_time?: string
}

/* 搜索选择器数据类型 */
export interface searchSelectDataType {
  name?: string
  status?: string
}

/* 用户表单 */
export interface UserForm {
  id?: number
  username?: string
  name?: string
  dept_id?: number
  dept_name?: string
  role_ids?: number[]
  roleNames?: string[]
  position_ids?: number[]
  positionNames?: string[]
  password?: string
  gender?: number
  email?: string
  mobile?: string
  is_superuser?: boolean
  status?: boolean
  description?: string
}

/* 登录用户信息 */
export interface UserInfo {
  index?: number
  id?: number
  username?: string
  name?: string
  avatar?: string
  email?: string
  mobile?: string
  gender?: string
  password?: string
  menus?: MenuTable[]
  dept?: deptTreeType
  dept_id?: deptTreeType['id']
  dept_name?: deptTreeType['name']
  roles?: roleSelectorType[]
  roleNames?: roleSelectorType['name'][]
  role_ids?: roleSelectorType['id'][]
  positions?: positionSelectorType[]
  positionNames?: positionSelectorType['name'][]
  position_ids?: positionSelectorType['id'][]
  is_superuser?: boolean
  status?: boolean
  description?: string
  last_login?: string
  created_at?: string
  updated_at?: string
  creator?: creatorType
}

/* 菜单表 */
export interface MenuTable {
  index?: number
  id?: number
  name?: string
  type?: number
  icon?: string
  order?: number
  permission?: string
  route_name?: string
  route_path?: string
  component_path?: string
  redirect?: string
  parent_id?: number
  parent_name?: string
  keep_alive?: boolean
  hidden?: boolean
  always_show?: boolean
  title?: string
  params?: { key: string, value: string }[]
  affix?: boolean
  status?: boolean
  description?: string
  created_at?: string
  updated_at?: string
  children?: MenuTable[]
}

/* 部门树 */
export interface deptTreeType {
  id?: number
  name?: string
  parent_id?: number
  children?: deptTreeType[]
}

/* 角色选择器 */
export interface roleSelectorType {
  id?: number
  name?: string
  status?: boolean
  description?: string
}

/* 职位选择器 */
export interface positionSelectorType {
  id?: number
  name?: string
  status?: boolean
  description?: string
}

/* 个人中心用户信息表单 */
export interface UserProfileForm {
  id?: number
  name?: string
  gender?: string
  mobile?: string
  email?: string
  username?: string
  dept_name?: string
  positions?: positionSelectorType[]
  roles?: roleSelectorType[]
  avatar?: string
  created_at?: string
}

/* 修改密码表单 */
export interface PasswordChangeForm {
  old_password: string
  new_password: string
  confirm_password: string
}

/* 重置密码表单 */
export interface ResetPasswordForm {
  id: number
  password: string
}
