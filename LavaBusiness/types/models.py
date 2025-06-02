import hmac
import hashlib
import json
from pydantic import BaseModel
from typing import Optional, List

class Invoice(BaseModel):
    """
    Информация о выставленном счете.

    :var str order_id: Идентификатор платежа в системе мерчанта.
    :var str invoice_id: Идентификатор счета в системе Lava.ru.
    :var float amount: Сумма выставленного счета.
    :var str expire_date: Дата и время истечения срока действия счета (формат: YYYY-MM-DD HH:MM:SS).
    :var str url: Ссылка для оплаты счета.
    :var str comment: Комментарий к выставленному счету.
    """
    order_id: str
    invoice_id: str
    amount: float
    expire_date: str
    url: str
    comment: Optional[str] = None

class InvoiceStatus(BaseModel):
    """
    Информация о статусе счета.

    :var str order_id: Идентификатор платежа в системе мерчанта.
    :var str invoice_id: Идентификатор счета в системе Lava.ru.
    :var str status: Статус счета (created - ожидает оплаты, expired - просрочен, success - оплачен).
    :var int amount: Сумма выставленного счета.
    :var str expire_date: Дата и время истечения срока действия счета (формат: YYYY-MM-DD HH:MM:SS).
    :var dict full_response: Полный ответ API с информацией о счете.
    """
    order_id: str
    invoice_id: str
    status: str
    amount: float
    expire_date: str
    full_response: dict

class Payoff(BaseModel):
    """
    Информация о выводе.

    :var str order_id: Идентификатор вывода в системе мерчанта.
    :var str payoff_id: Идентификатор вывода в системе Lava.ru.
    """
    order_id: str
    payoff_id: str

class PayoffStatus(BaseModel):
    """
    Информация о статусе вывода.

    :var str order_id: Идентификатор вывода в системе мерчанта.
    :var str payoff_id: Идентификатор вывода в системе Lava.ru.
    :var str status: Статус вывода (created - в очереди, rejected - отменен, success - успешно завершен).
    :var float amount: Сумма вывода.
    :var float fee: Комиссия.
    :var float amount_recieve: Сумма вывода с учетом комиссии.
    :var str service: Сервис вывода.
    :var str wallet: Реквизиты для вывода средств.
    """
    order_id: str
    payoff_id: str
    status: str
    amount: float
    fee: float
    amount_recieve: float
    service: str
    wallet: str

class Balance(BaseModel):
    """
    Информация о балансе магазина.

    :var float balance: Доступный баланс магазина.
    :var float freeze_balance: Замороженные средства.
    """
    balance: float
    freeze_balance: float

class PayMethod(BaseModel):
    """
    Информация о методе оплаты.

    :var str service_name: Название платежного сервиса.
    :var str service_id: Внутренний идентификатор сервиса.
    :var float percent: Комиссия за операцию.
    :var float user_percent: Комиссия пользователя.
    :var float shop_percent: Комиссия магазина.
    """
    service_name: str
    service_id: str
    percent: float
    user_percent: float
    shop_percent: float

class PayMethods(BaseModel):
    """
    Доступные методы оплаты.

    :var List[PayMethod] methods: Список методов оплаты.
    """
    tariffs: List[PayMethod]

class PayoffTariff(BaseModel):
    """
    Информация о тарифе на вывод.

    :var str title: Название платежного сервиса.
    :var str service: Внутренний дентификатор сервиса.
    :var str currency: Валюта.
    :var float min_sum: Минимальная сумма вывода.
    :var float max_sum: Максимальная сумма вывода.
    :var float percent: Комиссия.
    :var float fix: Фиксированная сумма комиссии.
    """
    title: str
    service: str
    currency: str
    min_sum: float
    max_sum: float
    fee: float
    fix_fee: float

class PayoffTariffs(BaseModel):
    """
    Тарифы на вывод.

    :var List[PayoffTariff] tariffs: Список тарифов на вывод средств.
    """
    tariffs: List[PayoffTariff]

class BaseParams(BaseModel):
    shopId: str

    def build_request(self, secret_key: bytes) -> dict:
        json_data = self.model_dump_json()
        params_str = json.dumps(json_data).encode()
        signature = hmac.new(secret_key, params_str, hashlib.sha256).hexdigest()
        headers = {'Signature': signature, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        return json_data, headers

class CreateInvoiceParams(BaseParams):
    orderId: Optional[str] = None
    sum: float
    comment: Optional[str] = None
    expire: Optional[int] = None

class CreateInvoiceStatusParams(BaseParams):
    invoiceId: Optional[str] = None
    orderId: Optional[str] = None

class CreatePayoffParams(BaseParams):
    orderId: Optional[str] = None
    amount: float
    service: str
    walletTo: str
    substract: int

class CreatePayoffStatusParams(BaseParams):
    payoffId: Optional[str] = None
    orderId: Optional[str] = None