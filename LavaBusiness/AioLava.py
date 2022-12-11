import httpx
import time
import random
import hashlib
import hmac
import json

from LavaBusiness.types import Invoice, LavaError

client = httpx.AsyncClient()

class AioLava:
    """
    Асинхронный клиент для работы с Бизнес API Lava.ru

    **Параметры**\n
        • secret_key - Секретный ключ проекта\n
        • project_id - ID проекта
    """

    def __init__(self, secret_key: str, project_id: str):
        self.secret_key = secret_key
        self.project_id = project_id

    async def _create_sign_headers(self, params) -> json:
        secret_key = bytes(self.secret_key, 'utf-8')
        params_str = json.dumps(params).encode()
        signature = hmac.new(secret_key, params_str, hashlib.sha256).hexdigest()
        headers = {'Signature': signature, 'Accept': 'application/json', 'Content-Type': 'application/json'}

        return headers

    async def create_invoice(self, amount: float, comment: str = None, order_id: str = None, expire: int = 300) -> Invoice:
        """
        Выставление счета

        **Параметры**\n
            • amount - ``float`` - Сумма выставленного счета
                    Минимум: 1\n
            • comment - ``str`` (optional) - Комментарий к выставленному счету\n
            • order_id - ``str`` (optional) - Идентификатор платежа в системе мерчанта\n
            • expire - ``int`` (optional) - Время жизни счета в минутах
                    От 1 до 43200 (5 дней)
                    По умолчанию: 300 (5 часов)

        :return: ``Invoice`` - Объект выставленного счета
        """
        order_id = order_id or f'LavaBusiness-{int(time.time() * 100)}-{int(random.random() * 1000)}'

        if expire is not None:
            if expire > 43200:
                expire = 43200
            elif expire < 1:
                expire = 1

        params = {'shopId': self.project_id, 'orderId': order_id, 'sum': amount, 'comment': comment, 'expire': expire}
        headers = await self._create_sign_headers(params)
        request = await client.post(f'https://api.lava.ru/business/invoice/create', json=params, headers=headers)

        return Invoice(request.json(), order_id)

    async def invoice_status(self, invoce_id: str = None, order_id: str = None) -> str:
        """
        Статус счета

        **Параметры**\n
            • invoce_id - ``str`` (optional, если указан order_id) - Идентификатор счета в системе Lava.ru\n
            • order_id - ``str`` (optional, если указан invoce_id) - Идентификатор платежа в системе мерчанта

        :return: - ``str`` - Статус счета (``created`` - Ожидает оплаты, ``expired`` - Просрочен, ``success`` - Оплачен)
        """
        params = {'shopId': self.project_id}

        if invoce_id != None:
            params.update({'invoiceId': invoce_id})
        else:
            params.update({'orderId': order_id})

        headers = await self._create_sign_headers(params)
        request = await client.post(f'https://api.lava.ru/business/invoice/status', json=params, headers=headers)
        response = request.json()

        if 'error' in response:
            raise LavaError(response)

        return response['data']['status']

    async def pay_methods(self) -> list:
        """
        Доступные методы оплаты

        :return: ``dict``
        """
        params = {'shopId': self.project_id}
        headers = await self._create_sign_headers(params)
        request = await client.post('https://api.lava.ru/business/invoice/get-available-tariffs', json=params, headers=headers)
        response = request.json()

        if 'error' in response:
            raise LavaError(response)

        return response['data']

    async def balance(self) -> dict:
        """
        Баланс магазина

        :return: ``dict``
        """
        params = {'shopId': self.project_id}
        headers = await self._create_sign_headers(params)
        request = await client.post('https://api.lava.ru/business/shop/get-balance', json=params, headers=headers)
        response = request.json()

        if 'error' in response:
            raise LavaError(response)

        return response['data']

    async def create_payoff(self, amount: float, order_id: str = None, service: str = 'lava', wallet_to: str = None, substract_fee: int = 0) -> str:
        """
        Выставление счета

        **Параметры**\n
            • amount - ``float`` - Сумма вывода\n
            • order_id - ``str`` (optional) - Идентификатор платежа в системе мерчанта\n
            • service - ``str`` (optional) - Сервис вывода (``lava`` - Кошелек Lava, ``qiwi`` - QIWI.com, ``card`` - Банковская карта)
                    По умолчанию: ``lava``

        :return: ``str`` - Идентификатор вывода в системе Lava.ru (payoff_id)
        """
        order_id = order_id or f'LavaBusiness-{int(time.time() * 100)}-{int(random.random() * 1000)}'
        payoff_service = service + '_payoff'

        params = {'shopId': self.project_id, 'orderId': order_id, 'amount': amount, 'service': payoff_service, 'walletTo': wallet_to, 'subtract': substract_fee}
        headers = await self._create_sign_headers(params)
        request = await client.post(f'https://api.lava.ru/business/payoff/create', json=params, headers=headers)
        response = request.json()

        if 'error' in response:
            raise LavaError(response)

        return response['data']['payoff_id']

    async def payoff_status(self, payoff_id: str = None, order_id: str = None) -> str:
        """
        Статус вывода

        **Параметры**\n
            • payoff_id - ``str`` (optional, если указан order_id) - Идентификатор вывода в системе Lava.ru\n
            • order_id - ``str`` (optional, если указан payoff_id) - Идентификатор платежа в системе мерчанта

        :return: - ``str`` - Статус вывода (``created`` - В очереди, ``rejected`` - Отменен, ``success`` - Успешно завершен)
        """
        params = {'shopId': self.project_id}

        if payoff_id != None:
            params.update({'payoffId': payoff_id})
        else:
            params.update({'orderId': order_id})

        headers = await self._create_sign_headers(params)
        request = await client.post(f'https://api.lava.ru/business/payoff/info', json=params, headers=headers)
        response = request.json()

        if 'error' in response:
            raise LavaError(response)

        return response['data']['status']

    async def payoff_tarrifs(self) -> list:
        """
        Тарифы на вывод

        :return: ``dict``
        """
        params = {'shopId': self.project_id}
        headers = await self._create_sign_headers(params)
        request = await client.post('https://api.lava.ru/business/payoff/get-tariffs', json=params, headers=headers)
        response = request.json()

        if 'error' in response:
            raise LavaError(response)

        return response['data']['tariffs']
