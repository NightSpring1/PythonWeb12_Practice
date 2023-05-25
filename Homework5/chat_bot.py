import asyncio
import logging
import time
from datetime import datetime, timedelta
from aiofile import async_open
import aiohttp
import websockets

logging.basicConfig(level=logging.INFO)

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
        o_str = []
        for i in results:
            for j in i['exchangeRate']:
                if j['currency'] in ("EUR", "USD"):
                    msg = f"{i['date']} {j['currency']} -> S: {j['saleRate']:.2f}, P: {j['purchaseRate']:.2f}| "
                    o_str.append(msg)

        await asyncio.sleep(1)
        return ''.join(o_str)

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
                logging.info(f'done in {finish - start:.4f} sec.')
                return result
        except aiohttp.ClientConnectorError:
            pass


async def get_currency_message(days: int) -> str:
    pb = PBCollector()
    result = await pb.get_currency(days)
    del pb
    return result


async def message_handler(message: str) -> str | None:
    if message not in COMMAND:
        return None
    else:
        async with async_open("exchange.log", 'a') as afp:
            await afp.write(f"{str(datetime.now())}: -exchange called.\n")
        return await COMMAND[message](1)


async def polling(hostname: str, port: int):
    ws_resource_url = f"ws://{hostname}:{port}"
    async with websockets.connect(ws_resource_url) as ws:
        async for message in ws:
            logging.info(f"Message: {message}")
            respond = await message_handler(message)
            if respond is not None:
                await ws.send(respond)

COMMAND = {'-exchange': get_currency_message}


if __name__ == '__main__':
    asyncio.run(polling('localhost', 8080))
