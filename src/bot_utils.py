import os

import requests
from dotenv import load_dotenv


class BotUtils:
    __instance__ = None
    uid_telegram = ""
    username = ""
    password = ""

    def __init__(self):
        if BotUtils.__instance__ is None:
            BotUtils.__instance__ = self
        else:
            raise Exception("This class is a singleton!")

    @staticmethod
    def get_instance():
        if BotUtils.__instance__ is None:
            BotUtils.__instance__ = BotUtils()

        return BotUtils.__instance__

    def escape_chars(self, string):
        escape_chars = ['[', ']', '(', ')', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in escape_chars:
            string = string.replace(char, f'/{char}')

        return string

    def send_get(self, path):
        load_dotenv()
        payload = {"uid_telegram": self.uid_telegram}
        return requests.get(self.URL_API() + path, data=payload)

    def send_post(self, path, data):
        load_dotenv()
        data['uid_telegram'] = self.uid_telegram
        return requests.post(self.URL_API() + path, data=data)

    def URL_API(self):
        load_dotenv()
        return os.getenv('URL_API')

    def LOGIN_AUTH(self):
        load_dotenv()
        return os.getenv('LOGIN')

    def PASSW_AUTH(self):
        load_dotenv()
        return os.getenv('PASSW')

    def BOT_TOKEN(self):
        load_dotenv()
        return os.getenv('BOT_TOKEN')

    def set_uid_telegram(self, uid_telegram):
        self.uid_telegram = uid_telegram
