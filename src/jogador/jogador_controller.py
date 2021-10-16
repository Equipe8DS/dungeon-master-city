import json

from bot_utils import BotUtils


class JogadorController:
    __bot_util__ = BotUtils()

    def buscar_jogador(self):
        request = self.__bot_util__.send_get('/jogador/')
        content = json.loads(request.content)

        lista_jogadores = content["results"]
        return lista_jogadores

    def info_detalhada_jogador(self, jogador):
        info = f'Nome: {jogador["nome"]} \n' \
               f'E-mail: {jogador["email"]} \n' \
               f'Username: {jogador["username"]}'
        return info
