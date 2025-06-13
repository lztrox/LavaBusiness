import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    INVOICE_ID = ""
    invoice = await api.invoice_status(INVOICE_ID)

    if invoice.status == 'success':
        print('Счет оплачен')
    elif invoice.status == 'expired':
        print('Счет просрочен')
    else:
        print('Счет ожидает оплаты')
    
asyncio.run(main())