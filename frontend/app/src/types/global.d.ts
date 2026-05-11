declare global {
  /**
   * 响应数据
   */
  interface ApiResponse<T = any> {
    code: number
    data: T
    msg: string
    status_code: number
  }

  /**
   * 分页查询参数
   */
  interface PageQuery {
    /** 当前页码 */
    page_no: number
    /** 每页条数 */
    page_size: number
  }

  /**
   * 分页响应对象
   */
  interface PageResult<T> {
    /** 数据列表 */
    items: T
    /** 总数 */
    total: number
    page_no: number
    page_size: number
    has_next: boolean
  }

  /**
   * 下拉选项数据类型
   */
  interface OptionType {
    /** 值 */
    value: string | number
    /** 文本 */
    label: string
    /** 子列表  */
    children?: OptionType[]
  }

  /**
   * 创建人
   */
  interface creatorType {
    id?: number
    name?: string
    username?: string
  }

  /**
   * 上传文件返回
   */
  interface UploadFileResult {
    file_path: string
    file_name: string
    origin_name: string
    file_url: string
  }
}
export {}
