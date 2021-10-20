import json

from bot_utils import BotUtils


class JogadorController:
    __bot_util__ = BotUtils.get_instance()

    def criar_jogador(self, username):
        data = {'username': username, 'nome': username, 'uid_telegram': self.__bot_util__.uid_telegram, 'password': self.__bot_util__.uid_telegram}
        request = self.__bot_util__.send_post(path='/jogador/', data=data)
        return "Jogador criado com sucesso"

    def buscar_jogadores(self):
        request = self.__bot_util__.send_get('/jogador/')
        content = json.loads(request.content)

        lista_jogadores = content["results"]
        return lista_jogadores

    def info_detalhada_jogador(self, jogador):
        info = f'Nome: {jogador["nome"]} \n' \
               f'E-mail: {jogador["email"]} \n' \
               f'Username: {jogador["username"]}'
        return info
