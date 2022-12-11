import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    payoff_tarrifs = await api.payoff_tarrifs()
    for tarrif in payoff_tarrifs:
        print(tarrif)

asyncio.run(main())