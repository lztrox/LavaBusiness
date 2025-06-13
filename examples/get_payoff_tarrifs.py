import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    payoff_tarrifs = await api.payoff_tarrifs()
    for tarrif in payoff_tarrifs.tariffs:
        print(f'Service name: {tarrif.title}')
        print(f'Internal service ID: {tarrif.service}')
        print(f'Currency: {tarrif.currency}')
        print(f'Minimal amount: {tarrif.min_sum}')

asyncio.run(main())