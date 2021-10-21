import telebot
from telebot.types import ForceReply

from item.item_controller import ItemController
from jogador.jogador_controller import JogadorController
from loja.loja_controller import LojaController
from personagem.personagem_controller import PersonagemController


class BotController:
    __instance__ = None

    bot = telebot.TeleBot(token='')
    loja_controller = LojaController()
    personagem_controller = PersonagemController()
    item_controller = ItemController()
    jogador_controller = JogadorController()

    def __init__(self):
        if BotController.__instance__ is None:
            BotController.__instance__ = self
        else:
            raise Exception("This class is a singleton!")

    @staticmethod
    def get_instance():
        if BotController.__instance__ is None:
            BotController.__instance__ = BotController()

        return BotController.__instance__

    def gerar_lista_por_nomes(self, list):
        i = 1
        response = ""
        for object in list:
            response = response + str(i) + " - " + object["nome"] + "\n"
            i = i + 1
        return response

    def gerar_dicionario_lista_por_nome(self, list):
        list_dict = {object['nome']: object for object in list}
        return list_dict

    def confirmar_username(self, message):
        self.bot.send_chat_action(message.chat.id, 'typing')
        username = message.text
        self.jogador_controller.criar_jogador(username=username)
        self.bot.reply_to(message, f'Seja bem-vindo {username} ! A grande Redzay te espera.')

    def inserir_username(self, chat_id):
        reply = self.bot.send_message(chat_id=chat_id, text='Digite seu nome de usuário', reply_markup=ForceReply())
        self.bot.register_for_reply_by_message_id(message_id=reply.message_id, callback=self.confirmar_username)
