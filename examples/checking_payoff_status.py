import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    PAYOFF_ID = ""
    payoff = await api.payoff_status(PAYOFF_ID)

    if payoff.status == 'success':
        print('Payoff completed')
    elif payoff.status == 'rejected':
        print('Payoff canceled')
    else:
        print('Payoff in queue')

asyncio.run(main())