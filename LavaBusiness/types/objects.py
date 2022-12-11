from LavaBusiness.types import LavaError

class Invoice:
    """
    Объект выставленного счета

    **Атрибуты**\n
        • responce - ``dict`` - json ответ Lava.ru API\n
        • order_id - ``str`` - Идентификатор платежа в системе мерчанта\n
        • invoice_id - ``str`` - Идентификатор счета в системе Lava.ru\n
        • amount - ``int`` - Сумма выставленного счета\n
        • expire_date - ``str`` - Дата и время истечения\n
        • url - ``str`` - Ссылка на оплату\n
        • comment - ``str`` - Комментарий к выставленному счету\n
    """
    def __init__(self, response: dict, order_id: str):
        self.response: dict = response

        if 'error' in response:
            raise LavaError(response)

        self.order_id: str = order_id
        self.invoice_id: str = response['data']['id']
        self.amount: float = response['data']['amount']
        self.expire_date: str = response['data']['expired']
        self.url: str = response['data']['url']
        self.comment: str = response['data']['comment']