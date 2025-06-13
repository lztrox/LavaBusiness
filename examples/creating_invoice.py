import asyncio
from LavaBusiness import AioLava

SECRET_KEY = "wasdfwefw"
PROJECT_ID = "wefwefwefwef"

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    invoice = await api.create_invoice(100)
    print(f'Ссылка на оплату: {invoice.url}')
    print(f'Идентификатор счета: {invoice.invoice_id}')

asyncio.run(main())