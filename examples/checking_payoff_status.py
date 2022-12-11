import asyncio
from LavaBusiness import AioLava

SECRET_KEY = ""
PROJECT_ID = ""

api = AioLava(SECRET_KEY, PROJECT_ID)

async def main():
    PAYOFF_ID = ""
    status = await api.payoff_status(PAYOFF_ID)

    if status == 'success':
        print('Вывод успешно завершен')
    elif status == 'rejected':
        print('Вывод отменен')
    else:
        print('Вывод в очереди')

asyncio.run(main())