import random
import time

from LavaBusiness.types.client import AsyncClient
from LavaBusiness.types.models import *
from LavaBusiness.processors.response_processors import ResponseProcessor

class AioLava:
    """
    Асинхронный клиент для работы с Бизнес API Lava.ru.

    :param secret_key: Секретный ключ проекта.
    :type secret_key: str
    :param project_id: ID проекта.
    :type project_id: str
    """
    secret_key: bytes
    project_id: str
    client: AsyncClient

    def __init__(self, secret_key: str, project_id: str):
        self._set_secret_key(secret_key)
        self.project_id = project_id
        self.client = AsyncClient()

    def _set_secret_key(self, secret_key: str) -> None:
        self.secret_key = bytes(secret_key, 'utf-8')

    @staticmethod
    def _build_order_id(order_id: str | None = None):
        return order_id or f'LavaBusiness-{int(time.time() * 100)}-{int(random.random() * 1000)}'

    @staticmethod
    def _build_expire(expire: int):
        if expire > 43200:
            expire = 43200
        elif expire < 1:
            expire = 1
        return expire

    @staticmethod
    def _build_payoff_service(service: str | None = None):
        return service + '_payoff'

    async def create_invoice(self, amount: float, comment: str | None = None, order_id: str | None = None, expire: int = 300) -> Invoice:
        """
        Выставление счета.

        :param amount: Сумма выставленного счета.
        :type amount: float
        :param comment: Комментарий к выставленному счету (необязательный).
        :type comment: str, optional
        :param order_id: Идентификатор платежа в системе мерчанта (необязательный).
        :type order_id: str, optional
        :param expire: Время жизни счета в минутах (от 1 до 43200, по умолчанию 300).
        :type expire: int, optional
        :return: Информация о выставленном счете.
        :rtype: Invoice
        """
        order_id = self._build_order_id(order_id=order_id)
        expire = self._build_expire(expire=expire)

        params = CreateInvoiceParams(shopId=self.project_id, orderId=order_id, sum=amount, comment=comment, expire=expire)
        json_data, headers = params.build_request(self.secret_key)
        response = await self.client.post(url='invoice/create', json=json_data, headers=headers)

        return ResponseProcessor.process(order_id=order_id, response=response, response_type='invoice_created')

    async def invoice_status(self, invoce_id: str | None = None, order_id: str | None = None) -> InvoiceStatus:
        """
        Статус счета.

        :param invoice_id: Идентификатор счета в системе Lava.ru (необязательный, если указан `order_id`).
        :type invoice_id: str, optional
        :param order_id: Идентификатор платежа в системе мерчанта (необязательный, если указан `invoice_id`).
        :type order_id: str, optional
        :return: Информация о статусе счета.
        :rtype: InvoiceStatus
        :raises ValueError: Если не указан `invoice_id` или `order_id`, либо указаны оба одновременно.
        """
        if invoce_id:
            params = CreateInvoiceStatusParams(shopId=self.project_id, invoiceId=invoce_id)
        elif order_id:
            params = CreateInvoiceStatusParams(shopId=self.project_id, orderId=order_id)
        else:
            raise ValueError('Должен быть указан один из параметров - invoice_id, либо order_id')

        json_data, headers = params.build_request(self.secret_key)
        response = await self.client.post(url='invoice/status', json=json_data, headers=headers)

        return ResponseProcessor.process(response=response, response_type='invoice_status')

    async def create_payoff(self, amount: float, order_id: str | None = None, service: str = 'lava', wallet_to: str | None = None, substract_fee: int = 0) -> Payoff:
        """
        Создание вывода.

        :param amount: Сумма вывода.
        :type amount: float
        :param order_id: Идентификатор платежа в системе мерчанта (необязательный).
        :type order_id: str, optional
        :param service: Сервис вывода (lava - Кошелек Lava, card - Банковская карта, qiwi - QIWI.com).
        :type service: str, optional
        :param wallet_to: Реквизиты для вывода.
        :type wallet_to: str
        :param substract_fee: С кого списывать комиссию (0 - с суммы, 1 - с магазина).
        :type substract_fee: int, optional
        :return: Информация о выводе.
        :rtype: Payoff
        """
        order_id = self._build_order_id(order_id=order_id)
        payoff_service = self._build_payoff_service(service=service)

        params = CreatePayoffParams(shopId=self.project_id, orderId=order_id, amount=amount, service=payoff_service, walletTo=wallet_to, substract=substract_fee)
        json_data, headers = params.build_request(self.secret_key)
        response = await self.client.post(url='payoff/create', json=json_data, headers=headers)

        return ResponseProcessor.process(order_id=order_id, response=response, response_type='payoff_created')

    async def payoff_status(self, payoff_id: str | None = None, order_id: str | None = None) -> PayoffStatus:
        """
        Статус вывода.

        :param payoff_id: Идентификатор вывода в системе Lava.ru (необязательный, если указан `order_id`).
        :type payoff_id: str, optional
        :param order_id: Идентификатор платежа в системе мерчанта (необязательный, если указан `payoff_id`).
        :type order_id: str, optional
        :return: Информация о статусе вывода.
        :rtype: PayoffStatus
        :raises ValueError: Если не указан `payoff_id` или `order_id`, либо указаны оба одновременно.
        """
        if payoff_id:
            params = CreatePayoffStatusParams(shopId=self.project_id, payoffId=payoff_id)
        elif order_id:
            params = CreatePayoffStatusParams(shopId=self.project_id, orderId=order_id)
        else:
            raise ValueError('Должен быть указан один из параметров - payoff_id, либо order_id')

        json_data, headers = params.build_request(self.secret_key)
        response = await self.client.post(url='payoff/info', json=json_data, headers=headers)

        return ResponseProcessor.process(response=response, response_type='payoff_status')

    async def balance(self) -> Balance:
        """
        Баланс магазина.

        :return: Информация о балансе магазина.
        :rtype: Balance
        """
        params = BaseParams(shopId=self.project_id)
        json_data, headers = params.build_request(self.secret_key)
        response = await self.client.post(url='shop/get-balance', json=json_data, headers=headers)

        return ResponseProcessor.process(response=response, response_type='balance')

    async def pay_methods(self) -> PayMethods:
        """
        Доступные методы оплаты.

        :return: Список методов оплаты.
        :rtype: PayMethods
        """
        params = BaseParams(shopId=self.project_id)
        json_data, headers = params.build_request(self.secret_key)
        response = await self.client.post(url='invoice/get-available-tariffs', json=json_data, headers=headers)

        return ResponseProcessor.process(response=response, response_type='pay_methods')

    async def payoff_tarrifs(self) -> PayoffTariffs:
        """
        Тарифы на вывод.

        :return: Список тарифов на вывод средств.
        :rtype: PayoffTariffs
        """
        params = BaseParams(shopId=self.project_id)
        json_data, headers = params.build_request(self.secret_key)
        response = await self.client.post(url='payoff/get-tariffs', json=json_data, headers=headers)

        return ResponseProcessor.process(response=response, response_type='payoff_tariffs')