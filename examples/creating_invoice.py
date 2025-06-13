import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    invoice = await api.create_invoice(100)
    print(f'Invoice url: {invoice.url}')
    print(f'Invoice ID: {invoice.invoice_id}')

asyncio.run(main())