import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    pay_methods = await api.pay_methods()
    for method in pay_methods.methods:
        print(f'Название платежного сервиса: {method.service_name}')
        print(f'Внутренний идентификатор сервиса: {method.service_id}')
        print(f'Комиссия за операцию: {method.percent} %')

asyncio.run(main())