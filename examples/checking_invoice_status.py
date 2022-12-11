import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    INVOICE_ID = ""
    status = await api.invoice_status(INVOICE_ID)

    if status == 'success':
        print('Счет оплачен')
    elif status == 'expired':
        print('Счет просрочен')
    else:
        print('Счет ожидает оплаты')
    
asyncio.run(main())