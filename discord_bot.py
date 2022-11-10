import json
import os
import time
from datetime import datetime

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from get_splatoon_schedule import Splatoon

load_dotenv()
CHANNEL_ID=os.getenv('CHANNEL_ID')
EMOJI_HOKO=os.getenv('EMOJI_HOKO')
EMOJI_ASARI=os.getenv('EMOJI_ASARI')
EMOJI_AREA=os.getenv('EMOJI_AREA')
EMOJI_YAGURA=os.getenv('EMOJI_YAGURA')
if __name__=="__main__":
    while(1):
        now = datetime.now()
        # if 1:
        if now.minute==0 or now.minute == 30:
            Intents = discord.Intents.all()
            Intents.members = True
            client = discord.Client(intents=Intents)
            break
        time.sleep(5)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    alert_hoko_schedule.start()
    get_splatoon_schedule_with_timer.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "get_hoko":
        with open('./hoko.json', 'r') as f:
            hoko_schedules = json.load(f).values()
        message_hoko_time =""
        for hoko_schedule in hoko_schedules:
            message_hoko_time+= f"{hoko_schedule['type']}:{hoko_schedule['start_time']}:00～{hoko_schedule['end_time']}:00\n{hoko_schedule['stages'][0]['name']} {hoko_schedule['stages'][1]['name']}\n\n"
        await message.channel.send(f"{message_hoko_time}".strip('\n\n'))
    elif message.content == "get_now":
        now = datetime.now()
        now_schedule = Splatoon.get_now_schedule(datetime.now().hour)
        emoji_transition_dict={"ガチホコ":EMOJI_HOKO,"ガチアサリ":EMOJI_ASARI,"ガチエリア":EMOJI_AREA,"ガチヤグラ":EMOJI_YAGURA,"ナワバリバトル":""}
        message_now_schedule=f"スケジュール更新まで{1 if now.hour%2==1 else 0}:{60-now.minute}\n\n"
        for key,value in now_schedule.items():
            message_now_schedule+=f"{key}\n{value['rule']['name']} {emoji_transition_dict[value['rule']['name']]} \nステージ:{value['stages'][0]['name']} {value['stages'][1]['name']}\n\n"
        await message.channel.send(f"{message_now_schedule}".strip('\n\n'))




@tasks.loop(seconds=60*30)
async def alert_hoko_schedule():
    now = datetime.now()
    with open('./hoko.json', 'r') as f:
        hoko_schedule = json.load(f)
    if str(now.hour+1) in hoko_schedule.keys() and now.minute == 30:
        hold_hoko_schedule = hoko_schedule[str(now.hour+1)]
        channel = client.get_channel(int(CHANNEL_ID))
        await channel.send(f"ガチホコが30分後に始まります。\n{hold_hoko_schedule['type']}\n開催時刻:{hold_hoko_schedule['start_time']}:00~{hold_hoko_schedule['end_time']}:00\nステージ:{hold_hoko_schedule['stages'][0]['name']} {hold_hoko_schedule['stages'][1]['name']}")
        await channel.send(f"{hold_hoko_schedule['stages'][0]['image']}")
        await channel.send(f"{hold_hoko_schedule['stages'][1]['image']}")
    if str(now.hour) in hoko_schedule.keys() and now.minute == 00:
        hold_hoko_schedule = hoko_schedule[str(now.hour)]
        channel = client.get_channel(int(CHANNEL_ID))
        await channel.send(f"ガチホコが始まります。\n{hold_hoko_schedule['type']}\n開催時刻:{hold_hoko_schedule['start_time']}:00~{hold_hoko_schedule['end_time']}:00\nステージ:{hold_hoko_schedule['stages'][0]['name']} {hold_hoko_schedule['stages'][1]['name']}")
        await channel.send(f"{hold_hoko_schedule['stages'][0]['image']}")
        await channel.send(f"{hold_hoko_schedule['stages'][1]['image']}")
    if str(now.hour-1) in hoko_schedule.keys() and now.minute == 30:
        hold_hoko_schedule = hoko_schedule[str(now.hour-1)]
        channel = client.get_channel(int(CHANNEL_ID))
        await channel.send(f"ガチホコが30分後に終了します。")

@tasks.loop(seconds=60*60*24)
async def get_splatoon_schedule_with_timer():
    Splatoon.get_splatoon_schedule()
client.run(os.getenv('TOKEN'))
