import json

from telebot.types import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup

from botController import BotController
from loja.loja_controller import LojaController
from personagem.personagem_controller import PersonagemController


class CompraController:
    __bot_controller__ = BotController.get_instance()
    __loja_controller__ = LojaController()
    __personagem_controller__ = PersonagemController()

    __loja_selecionada__ = {}
    __item_selecionado__ = {}
    __personagem_selecionado__ = {}
    __quantidade_selecionada__ = {}

    def iniciar_interacao(self, chat_id):
        personagens = self.__personagem_controller__.get_botoes()
        message = self.__bot_controller__.bot.send_message(chat_id=chat_id, reply_markup=personagens,
                                                           text='Para qual personagem deseja comprar?')
        self.__bot_controller__.bot.register_callback_query_handler(func=lambda call: message.id == call.message.id,
                                                                    callback=self.selecionar_loja)

    def selecionar_loja(self, call):
        chat_id = call.message.chat.id
        self.__personagem_selecionado__ = json.loads(call.data)

        lojas = self.__loja_controller__.get_botoes_loja()
        message = self.__bot_controller__.bot.send_message(chat_id=chat_id, reply_markup=lojas,
                                                           text='Em qual loja deseja comprar?')

        self.__bot_controller__.bot.delete_message(message_id=call.message.id, chat_id=chat_id)
        self.__bot_controller__.bot.register_callback_query_handler(func=lambda call: message.id == call.message.id,
                                                                    callback=self.selecionar_item)

    def selecionar_item(self, call):
        chat_id = call.message.chat.id
        self.__loja_selecionada__ = json.loads(call.data)

        itens = self.__loja_controller__.get_botoes_estoque(self.__loja_selecionada__['id'])
        message = self.__bot_controller__.bot.send_message(chat_id=chat_id, reply_markup=itens,
                                                           text='Qual item deseja comprar?')

        self.__bot_controller__.bot.delete_message(message_id=call.message.id, chat_id=chat_id)
        self.__bot_controller__.bot.register_callback_query_handler(func=lambda call: message.id == call.message.id,
                                                                    callback=self.selecionar_quantidade)

    def selecionar_quantidade(self, call):
        chat_id = call.message.chat.id
        self.__item_selecionado__ = json.loads(call.data)

        reply = self.__bot_controller__.bot.send_message(chat_id=chat_id, text='Quantos itens?',
                                                         reply_markup=ForceReply())

        self.__bot_controller__.bot.delete_message(message_id=call.message.id, chat_id=chat_id)
        self.__bot_controller__.bot.register_for_reply_by_message_id(message_id=reply.message_id,
                                                                     callback=self.confirmar_compra)

    def confirmar_compra(self, message):
        chat_id = message.chat.id
        self.quantidade_selecionada = message.text

        text_confirmacao = f'Confirma compra de *{self.quantidade_selecionada} {self.__item_selecionado__["nome"]}\(s\)*' \
                           f' em *{self.__loja_selecionada__["nome"]}* para *{self.__personagem_selecionado__["nome"]}*?'

        opcao_sim = InlineKeyboardButton(text='Sim', callback_data='sim')
        opcao_nao = InlineKeyboardButton(text='Não', callback_data='nao')

        markup = InlineKeyboardMarkup(row_width=2, keyboard=[[opcao_sim, opcao_nao]])
        message = self.__bot_controller__.bot.send_message(chat_id=chat_id, text=text_confirmacao,
                                                           reply_markup=markup, parse_mode='MarkdownV2')

        self.__bot_controller__.bot.register_callback_query_handler(func=lambda call: message.id == call.message.id,
                                                                    callback=self.efetuar_compra)

    def efetuar_compra(self, call):
        opcao = call.data
        chat_id = call.message.chat.id

        if opcao == 'sim':
            loja_id = self.__loja_selecionada__['id']
            item_id = self.__item_selecionado__['id']
            personagem_id = self.__personagem_selecionado__['id']

            response = self.__loja_controller__.comprar_item(quantidade=self.quantidade_selecionada, id_item=item_id,
                                                             id_loja=loja_id, id_personagem=personagem_id)
            self.__bot_controller__.bot.send_message(chat_id=chat_id, text=response)
            self.__bot_controller__.bot.delete_message(message_id=call.message.id, chat_id=chat_id)
        else:
            self.__bot_controller__.bot.send_message(chat_id=chat_id, text='Compra cancelada.')
