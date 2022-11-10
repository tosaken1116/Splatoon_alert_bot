import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv


class Splatoon:
    @classmethod
    def get_splatoon_schedule(cls):
        load_dotenv()
        USER_AGENT=os.getenv('USER_AGENT')
        BASE_URL = os.getenv('BASE_URL')
        headers={"user-agent": USER_AGENT}
        response = requests.get(f"{BASE_URL}schedule", headers=headers).json()
        with open('./response.json', 'w') as f:
            json.dump(response, f, ensure_ascii=False)
        cls.save_splatoon_schedule_hoko()
    def save_splatoon_schedule_hoko():
        with open('./response.json', 'r') as f:
            response = json.load(f)
        bankara_open_schedule_list = response["result"]["bankara_open"]
        bankara_charange_schedule_list= response["result"]["bankara_challenge"]
        gachihoko_dicts ={}
        for schedule in bankara_open_schedule_list:
            if schedule["rule"]["key"]=="GOAL":
                start_time = datetime.strptime(schedule["start_time"].split('T')[1].split('+')[0],"%H:%M:%S").hour
                schedule["start_time"] =start_time
                schedule["end_time"] =datetime.strptime(schedule["end_time"].split('T')[1].split('+')[0],"%H:%M:%S").hour
                schedule["type"]="オープン"
                gachihoko_dicts[start_time]=(schedule)
        for schedule in bankara_charange_schedule_list:
            if schedule["rule"]["key"]=="GOAL":
                start_time = datetime.strptime(schedule["start_time"].split('T')[1].split('+')[0],"%H:%M:%S").hour
                schedule["start_time"] =start_time
                schedule["end_time"] =datetime.strptime(schedule["end_time"].split('T')[1].split('+')[0],"%H:%M:%S").hour
                schedule["type"]="チャレンジ"
                gachihoko_dicts[start_time]=(schedule)
        with open('./hoko.json', 'w') as f:
            json.dump(gachihoko_dicts, f, ensure_ascii=False)
    @classmethod
    def get_now_schedule(cls,time:int) ->dict:
        with open('./response.json','r')as f:
            schedule = json.load(f)
        schedule_name_transition_dict ={"regular":"レギュラー","bankara_challenge":"チャレンジ","bankara_open":"オープン"}
        now_schedule = {}
        for schedule_key,schedule_value in schedule["result"].items():
            if schedule_key == "fest":
                continue
            for schedule_element in schedule_value:
                schedule_time = datetime.strptime(schedule_element["start_time"].split('T')[1].split('+')[0],"%H:%M:%S")
                if schedule_time.hour >=time and schedule_time.hour+2>time:
                    now_schedule[schedule_name_transition_dict[schedule_key]] = schedule_element
                    break
        return now_schedule
if __name__=="__main__":
    Splatoon.get_splatoon_schedule()