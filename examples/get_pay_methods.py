import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    pay_methods = await api.pay_methods()
    for method in pay_methods:
        print(method)

asyncio.run(main())