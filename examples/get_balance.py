import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    balances = await api.balance()
    print(balances['balance'])
    print(balances['freeze_balance'])

asyncio.run(main())