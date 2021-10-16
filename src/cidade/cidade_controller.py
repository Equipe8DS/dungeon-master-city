import json

from bot_utils import BotUtils


class CidadeController:
    __bot_util__ = BotUtils()

    def buscar_cidade(self):
        request = self.__bot_util__.send_get(path='/cidade/')

        a_json_object = json.loads(request.content)
        list_from_json = a_json_object["results"]
        return list_from_json

    def info_detalhada_cidade(self, cidade):
        info = f'Nome: {cidade["nome"]} \n' \
               f'Tesouro: {cidade["tesouro"]} peças de ouro'
        return info
