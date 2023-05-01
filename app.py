from telethon import TelegramClient, sync
from dateutil.parser import parse
import csv
import asyncio
from config import api_hash, api_id


data_file = open("data.csv", "r", encoding="utf-8-sig", newline="")
data_reader = csv.DictReader(data_file, delimiter=";")

result_file = open("result.csv", "w", encoding="windows-1251", newline="")
fieldnames = ["IMEI", "Последняя связь"]
result_writer = csv.DictWriter(result_file, fieldnames=fieldnames, delimiter=";")
result_writer.writeheader()


client = TelegramClient("test", api_id, api_hash)
client.start()


async def main():

    greeting_message = await client.send_message("https://t.me/Glonass2216_bot", "Здравствуйте")

    for data_line in data_reader:

        imei = data_line["IMEI"]

        await client.send_message("https://t.me/Glonass2216_bot", imei)
        await asyncio.sleep(0.1)

    middle_mes = await client.send_message("https://t.me/Glonass2216_bot", "Еще немного")

    async with asyncio.TaskGroup() as tg:
        async for message in client.iter_messages("https://t.me/Glonass2216_bot", min_id=greeting_message.id):
            if message.buttons:
                tg.create_task(message.click(0))
                await asyncio.sleep(1.5)

    async for message in client.iter_messages("https://t.me/Glonass2216_bot", min_id=middle_mes.id, search="IMEI:"):

        imei = message.message.split(" ")[1]

        try:
            word = message.message.split(" ")[4]
            last_con = parse(word).date()
        except:
            last_con = "n/d"

        res_line = {"IMEI": imei, "Последняя связь": last_con}
        result_writer.writerow(res_line)


if __name__ == "__main__":
    client.loop.run_until_complete(main())
