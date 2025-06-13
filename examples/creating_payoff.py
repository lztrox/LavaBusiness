import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    payoff = await api.create_payoff(100)
    print(f'Payoff ID: {payoff.payoff_id}')

asyncio.run(main())