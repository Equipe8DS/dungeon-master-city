import json

from telebot.types import ForceReply

from botController import BotController
from bot_utils import BotUtils


class JogadorController:
    __bot_util__ = BotUtils.get_instance()
    __bot_controller__ = BotController.get_instance()

    def criar_jogador(self, username):
        data = {'username': username, 'nome': username, 'uid_telegram': self.__bot_util__.uid_telegram, 'password': self.__bot_util__.uid_telegram}
        request = self.__bot_util__.send_post(path='/jogador/', data=data)
        return "Jogador criado com sucesso"

    def confirmar_username(self, message):
        self.__bot_controller__.bot.send_chat_action(message.chat.id, 'typing')
        username = message.text
        self.criar_jogador(username=username)
        self.__bot_controller__.bot.reply_to(message, f'Seja bem-vindo {username} ! A grande Redzay te espera.')

    def inserir_username(self, chat_id):
        reply = self.__bot_controller__.bot.send_message(chat_id=chat_id, text='Digite seu nome de usuário',
                                                         reply_markup=ForceReply())
        self.__bot_controller__.bot.register_for_reply_by_message_id(message_id=reply.message_id,
                                                                     callback=self.confirmar_username)

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
