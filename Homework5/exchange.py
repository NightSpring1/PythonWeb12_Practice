import asyncio
import sys
import time
import aiohttp
import logging
from datetime import datetime, timedelta
import platform

pb_url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

empty_dict = {"date": "None", "exchangeRate": [
    {"currency": "EUR", "saleRate": 0, "purchaseRate": 0},
    {"currency": "USD", "saleRate": 0, "purchaseRate": 0}]}


class PBCollector:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get_currency(self, days: int):
        async with self.session as session:
            tasks = []
            today = datetime.today()
            for i in range(days):
                day = (today - timedelta(days=i)).strftime('%d.%m.%Y')
                tasks.append(self.get_currency_rate(session, day))
            results = await asyncio.gather(*tasks)
            return results

    @staticmethod
    async def get_currency_rate(session: aiohttp.ClientSession, day: str):
        logging.debug('Started!')
        start = time.time()
        try:
            async with session.get(pb_url + day) as response:
                if response.status == 200:
                    result = await response.json()
                else:
                    result = empty_dict
                finish = time.time()
                logging.debug(f'done in {finish - start:.4f} sec.')
                return result
        except aiohttp.ClientConnectorError:
            pass


async def main():
    if not len(sys.argv) > 1:
        arg = 1
    elif not sys.argv[1].isdigit():
        arg = 1
    else:
        arg = int(sys.argv[1]) if int(sys.argv[1]) <= 10 else 10

    pb = PBCollector()
    print(f"Getting currency rate for {arg} days.")
    result = await pb.get_currency(int(arg))
    logging.debug("Results:")
    for i in result:
        for j in i.get('exchangeRate'):
            if j['currency'] in ("EUR", "USD"):
                print(f"{i['date']} {j['currency']} -> Sale: {j['saleRate']:.2f}, Purchase: {j['purchaseRate']:.2f}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(funcName)s %(message)s')
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
