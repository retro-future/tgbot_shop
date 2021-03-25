import logging
import json
from aiohttp import ClientSession, FormData
from tgbot.data import config

URL = "https://api.telegram.org/bot{0}/sendPhoto"

TOKEN = config.BOT_TOKEN


async def get_file_id(file_bytes: bytes):
    data = {
        "chat_id": "-402323826",
        "photo": file_bytes

    }
    async with ClientSession() as session:
        async with session.post(URL.format(TOKEN), data=data) as response:
            try:
                response_json = json.loads(await response.text())
                file_id = response_json['result']['photo'][-1]['file_id']
            except Exception as e:
                logging.error(e)

    return file_id


async def photo_link(photo_bytes: bytes):
    data = FormData()
    data.add_field(
        name="file",
        value=photo_bytes
    )
    async with ClientSession() as session:
        async with session.post("https://telegra.ph/upload", data=data) as response:
            try:
                response_json = json.loads(await response.text())
                link = "https://telegra.ph/" + response_json[0]["src"]
            except Exception as e:
                logging.error(e)
    return link
