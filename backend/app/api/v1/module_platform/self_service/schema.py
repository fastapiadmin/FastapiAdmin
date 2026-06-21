from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.common.enums import OrderTypeEnum

OrderType = OrderTypeEnum  # 兼容旧代码的类型别名
PackageAction = Literal["buy", "renew", "upgrade", "downgrade"]
PayMethod = Literal["alipay", "wxpay", "free"]


class PackageAvailableItem(BaseModel):
    """
    可选套餐项
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="套餐ID")
    name: str = Field(..., description="套餐名称")
    price: int = Field(..., ge=0, description="价格(分)")
    period: str = Field(..., description="计费周期(month/year)")
    trial_days: int = Field(default=0, ge=0, description="试用天数")
    max_users: int = Field(default=0, ge=0, description="最大用户数")
    max_roles: int = Field(default=0, ge=0, description="最大角色数")
    max_depts: int = Field(default=0, ge=0, description="最大部门数")
    max_storage_mb: int = Field(default=0, ge=0, description="最大存储(MB)")
    description: str | None = Field(default=None, description="套餐描述")
    is_current: bool = Field(default=False, description="是否为当前套餐")
    available_actions: list[PackageAction] = Field(default_factory=list, description="可执行操作列表")


class PackageAvailableOut(BaseModel):
    """
    可选套餐列表
    """

    model_config = ConfigDict(from_attributes=True)

    current_package_id: int | None = Field(default=None, description="当前套餐ID")
    packages: list[PackageAvailableItem] = Field(default_factory=list, description="可选套餐列表")


class PackagePreviewOut(BaseModel):
    """
    套餐变更预览结果
    """

    model_config = ConfigDict(from_attributes=True)

    current_package: str = Field(default="", description="当前套餐名称")
    target_package: str = Field(default="", description="目标套餐名称")
    action: PackageAction = Field(default="buy", description="操作类型")
    amount: int = Field(default=0, ge=0, description="金额(分)")
    period: str = Field(default="", description="计费周期")
    gained_menus: list[dict] = Field(default_factory=list, description="新增菜单清单")
    lost_menus: list[dict] = Field(default_factory=list, description="移除菜单清单")
    affected_roles: list[str] = Field(default_factory=list, description="受影响的角色名")
    affected_users: int = Field(default=0, ge=0, description="受影响用户数")


class SelfOrderCreate(BaseModel):
    """
    自助订单创建
    """

    package_id: int = Field(..., ge=1, description="套餐ID")
    order_type: PackageAction = Field(..., description="订单类型(buy/renew/upgrade/downgrade)")


class PluginPurchaseCreate(BaseModel):
    """
    插件购买
    """

    plugin_id: int = Field(..., ge=1, description="插件ID")
    pay_method: PayMethod | None = Field(default=None, description="支付方式(alipay/wxpay/free)")


class SelfOrderOut(BaseModel):
    """
    自助订单创建结果
    """

    model_config = ConfigDict(from_attributes=True)

    order_id: int = Field(..., description="订单ID")
    order_no: str = Field(..., description="订单号")
    amount: int = Field(..., ge=0, description="订单金额(分)")
    need_pay: bool = Field(..., description="是否需要支付")


class SelfOrderListItem(BaseModel):
    """
    我的订单列表项
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="订单ID")
    order_no: str = Field(..., description="订单号")
    package_name: str = Field(default="", description="套餐名称")
    order_type: OrderType = Field(..., description="订单类型")
    amount: int = Field(..., ge=0, description="订单金额(分)")
    status: int = Field(..., description="订单状态(0:待支付 1:已支付 2:已取消 3:已退款)")
    pay_method: str | None = Field(default=None, description="支付方式")
    pay_time: str | None = Field(default=None, description="支付时间")
    created_at: str | None = Field(default=None, description="创建时间")


class SelfOrderListOut(BaseModel):
    """
    我的订单列表
    """

    model_config = ConfigDict(from_attributes=True)

    items: list[SelfOrderListItem] = Field(default_factory=list, description="订单列表")
    total: int = Field(..., ge=0, description="总记录数")
    page_no: int = Field(..., ge=1, description="页码")
    page_size: int = Field(..., ge=1, description="每页数量")


class SelfOrderDetailOut(BaseModel):
    """
    订单详情
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="订单ID")
    order_no: str = Field(..., description="订单号")
    package_id: int | None = Field(default=None, description="套餐ID")
    package_name: str = Field(default="", description="套餐名称")
    amount: int = Field(..., ge=0, description="订单金额(分)")
    order_type: OrderType = Field(..., description="订单类型")
    status: int = Field(..., description="订单状态(0:待支付 1:已支付 2:已取消 3:已退款)")
    pay_method: str | None = Field(default=None, description="支付方式")
    pay_time: str | None = Field(default=None, description="支付时间")
    created_at: str | None = Field(default=None, description="创建时间")


class WorkspaceTenantInfo(BaseModel):
    """
    工作台-租户信息
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="租户ID")
    name: str = Field(..., description="租户名称")
    code: str = Field(..., description="租户编码")
    status: int = Field(..., description="租户状态(0:正常 1:宽限期 2:已暂停 3:已冻结 4:已过期 5:已归档)")
    status_label: str = Field(..., description="租户状态描述")
    start_time: str | None = Field(default=None, description="开始时间")
    end_time: str | None = Field(default=None, description="结束时间")
    days_remaining: int = Field(default=0, description="剩余天数")


class WorkspacePackageInfo(BaseModel):
    """
    工作台-套餐信息
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="套餐ID")
    name: str = Field(..., description="套餐名称")
    price: int = Field(..., ge=0, description="价格(分)")
    period: str = Field(..., description="计费周期")
    max_users: int = Field(..., ge=0, description="最大用户数")
    max_roles: int = Field(..., ge=0, description="最大角色数")
    max_depts: int = Field(..., ge=0, description="最大部门数")


class WorkspaceUsagePercent(BaseModel):
    """
    工作台-用量百分比
    """

    model_config = ConfigDict(from_attributes=True)

    users: float = Field(default=0.0, ge=0, description="用户用量占比(%)")
    roles: float = Field(default=0.0, ge=0, description="角色用量占比(%)")
    depts: float = Field(default=0.0, ge=0, description="部门用量占比(%)")


class WorkspaceQuotaInfo(BaseModel):
    """
    工作台-配额用量
    """

    model_config = ConfigDict(from_attributes=True)

    max_users: int = Field(default=0, ge=0, description="最大用户数")
    max_roles: int = Field(default=0, ge=0, description="最大角色数")
    max_depts: int = Field(default=0, ge=0, description="最大部门数")
    current_users: int = Field(default=0, ge=0, description="当前用户数")
    current_roles: int = Field(default=0, ge=0, description="当前角色数")
    current_depts: int = Field(default=0, ge=0, description="当前部门数")
    usage_percent: WorkspaceUsagePercent = Field(default_factory=WorkspaceUsagePercent, description="用量占比")


class WorkspaceOrderItem(BaseModel):
    """
    工作台-近期订单项
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="订单ID")
    order_no: str = Field(..., description="订单号")
    amount: int = Field(..., ge=0, description="订单金额(分)")
    order_type: OrderType = Field(..., description="订单类型")
    status: int = Field(..., description="订单状态(0:待支付 1:已支付 2:已取消 3:已退款)")
    created_at: str | None = Field(default=None, description="创建时间")


class WorkspaceOut(BaseModel):
    """
    工作台概览
    """

    model_config = ConfigDict(from_attributes=True)

    tenant: WorkspaceTenantInfo = Field(..., description="租户信息")
    package: WorkspacePackageInfo | None = Field(default=None, description="当前套餐信息")
    quota: WorkspaceQuotaInfo = Field(..., description="配额用量")
    recent_orders: list[WorkspaceOrderItem] = Field(default_factory=list, description="近期订单(最多5条)")
