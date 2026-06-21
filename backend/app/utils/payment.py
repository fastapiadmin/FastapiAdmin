import base64
import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from urllib.parse import urlencode

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from app.config.setting import settings
from app.core.logger import logger

# ── dataclass ──


@dataclass
class PaymentInfo:
    pay_url: str | None = None
    qr_code_url: str | None = None
    trade_no: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class CallbackResult:
    verified: bool = False
    transaction_id: str | None = None
    order_id: int | None = None
    amount: int = 0
    raw: dict[str, Any] = field(default_factory=dict)


# ── 抽象基类 ──


class BasePaymentGateway(ABC):

    @abstractmethod
    async def create_payment(self, order_no: str, amount: int, subject: str, notify_url: str) -> PaymentInfo:
        ...

    @abstractmethod
    async def verify_callback(self, data: dict[str, Any]) -> CallbackResult:
        ...


# ── 支付宝 ──


class AlipayGateway(BasePaymentGateway):
    GATEWAY_URL = "https://openapi.alipay.com/gateway.do"
    DEV_GATEWAY_URL = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"

    def __init__(self) -> None:
        self.app_id = settings.PAYMENT_ALIPAY_APP_ID or ""
        self._private_key = (settings.PAYMENT_ALIPAY_PRIVATE_KEY or "").encode()
        self._alipay_public_key = (settings.PAYMENT_ALIPAY_PUBLIC_KEY or "").encode()
        self.is_sandbox = settings.PAYMENT_ALIPAY_SANDBOX
        self._gateway = self.DEV_GATEWAY_URL if self.is_sandbox else self.GATEWAY_URL

    def _sign(self, params: dict[str, Any]) -> str:
        sorted_params = sorted((k, v) for k, v in params.items() if v != "" and v is not None)
        sign_str = "&".join(f"{k}={v}" for k, v in sorted_params)
        private_key_obj = serialization.load_pem_private_key(self._private_key, password=None)
        if not isinstance(private_key_obj, rsa.RSAPrivateKey):
            raise TypeError("私钥类型不是 RSA")
        signature = private_key_obj.sign(sign_str.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256())
        return base64.b64encode(signature).decode("utf-8")

    def _verify(self, params: dict[str, Any], signature: str) -> bool:
        sorted_params = sorted(
            (k, v) for k, v in params.items()
            if k != "sign" and k != "sign_type" and v != "" and v is not None
        )
        sign_str = "&".join(f"{k}={v}" for k, v in sorted_params)
        try:
            public_key_obj = serialization.load_pem_public_key(self._alipay_public_key)
            if not isinstance(public_key_obj, rsa.RSAPublicKey):
                return False
            public_key_obj.verify(base64.b64decode(signature), sign_str.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256())
            return True
        except Exception:
            return False

    async def create_payment(self, order_no: str, amount: int, subject: str, notify_url: str) -> PaymentInfo:
        biz_content = json.dumps({
            "out_trade_no": order_no,
            "total_amount": f"{amount / 100:.2f}",
            "subject": subject,
            "product_code": "FAST_INSTANT_TRADE_PAY",
        }, ensure_ascii=False)
        params = {
            "app_id": self.app_id,
            "method": "alipay.trade.page.pay",
            "format": "JSON",
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "notify_url": notify_url,
            "biz_content": biz_content,
        }
        params["sign"] = self._sign(params)
        pay_url = f"{self._gateway}?{urlencode(params)}"
        return PaymentInfo(pay_url=pay_url, trade_no="", raw=params)

    async def verify_callback(self, data: dict[str, Any]) -> CallbackResult:
        sign = data.pop("sign", "")
        _ = data.pop("sign_type", "")
        verified = self._verify(data, sign) if sign else False
        if verified and data.get("trade_status") in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            return CallbackResult(
                verified=True,
                transaction_id=data.get("trade_no"),
                amount=int(float(data.get("total_amount", 0)) * 100),
                raw=data,
            )
        return CallbackResult(verified=False, raw=data)


# ── Mock ──


class MockPaymentGateway(BasePaymentGateway):

    def __init__(self) -> None:
        self._pending_orders: dict[str, dict] = {}

    async def create_payment(self, order_no: str, amount: int, subject: str, notify_url: str) -> PaymentInfo:
        trade_no = f"MOCK{uuid.uuid4().hex[:16].upper()}"
        self._pending_orders[order_no] = {"trade_no": trade_no, "amount": amount, "subject": subject}
        pay_url = f"/mock-pay?order_no={order_no}&amount={amount}"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={pay_url}"
        return PaymentInfo(pay_url=pay_url, qr_code_url=qr_url, trade_no=trade_no, raw={"order_no": order_no, "amount": amount, "is_mock": True})

    async def verify_callback(self, data: dict[str, Any]) -> CallbackResult:
        order_no = data.get("order_no", "")
        pending = self._pending_orders.pop(order_no, None)
        if pending:
            return CallbackResult(verified=True, transaction_id=pending["trade_no"], order_id=data.get("order_id"), amount=pending["amount"], raw={**data, **pending})
        return CallbackResult(verified=False, raw=data)

    def get_mock_callback_data(self, order_id: int, order_no: str) -> dict:
        pending = self._pending_orders.get(order_no, {})
        return {
            "order_id": order_id,
            "order_no": order_no,
            "trade_no": pending.get("trade_no", f"MOCK{uuid.uuid4().hex[:16].upper()}"),
            "total_amount": str(pending.get("amount", 0) / 100),
            "trade_status": "TRADE_SUCCESS",
        }


# ── 工厂 ──

_mock_gateway: MockPaymentGateway | None = None


def create_payment_gateway(method: str = "") -> BasePaymentGateway:
    if method == "alipay":
        logger.info("🔔 使用支付宝支付网关")
        return AlipayGateway()
    if method == "wxpay":
        logger.info("🔔 使用微信支付网关（未实现，回退 Mock）")
        return MockPaymentGateway()
    if settings.PAYMENT_ALIPAY_APP_ID and settings.PAYMENT_ALIPAY_PRIVATE_KEY:
        logger.info("🔔 自动选择支付宝支付网关")
        return AlipayGateway()
    logger.info("🔔 使用 Mock 支付网关（开发模式）")
    return MockPaymentGateway()


def get_mock_gateway() -> MockPaymentGateway:
    global _mock_gateway
    if _mock_gateway is None:
        _mock_gateway = MockPaymentGateway()
    return _mock_gateway


__all__ = [
    "BasePaymentGateway",
    "PaymentInfo",
    "CallbackResult",
    "create_payment_gateway",
    "get_mock_gateway",
]
