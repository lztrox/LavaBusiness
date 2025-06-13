import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    INVOICE_ID = ""
    invoice = await api.invoice_status(INVOICE_ID)

    if invoice.status == 'success':
        print('Invoice paid')
    elif invoice.status == 'expired':
        print('Invoice expired')
    else:
        print('Waiting for payment')
    
asyncio.run(main())