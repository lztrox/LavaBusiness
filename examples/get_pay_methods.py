import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    pay_methods = await api.pay_methods()
    for method in pay_methods.methods:
        print(f'Service name: {method.service_name}')
        print(f'Internal service ID: {method.service_id}')
        print(f'Service fee: {method.percent} %')

asyncio.run(main())