import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    payoff_tarrifs = await api.payoff_tarrifs()
    for tarrif in payoff_tarrifs.tariffs:
        print(f'Название платежного сервиса: {tarrif.title}')
        print(f'Внутренний идентификатор сервиса: {tarrif.service}')
        print(f'Валюта: {tarrif.currency}')
        print(f'Минимальная сумма вывода: {tarrif.min_sum}')

asyncio.run(main())