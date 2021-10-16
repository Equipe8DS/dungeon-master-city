import os

import requests
from dotenv import load_dotenv


class BotUtils:
    def send_get(self, path):
        load_dotenv()
        return requests.get(self.URL_API() + path, auth=(self.LOGIN_AUTH(), self.PASSW_AUTH()))

    def send_post(self, path, data):
        load_dotenv()
        return requests.post(self.URL_API() + path, data=data, auth=(self.LOGIN_AUTH(), self.PASSW_AUTH()))

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
