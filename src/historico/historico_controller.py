import json

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from botController import BotController
from bot_utils import BotUtils
from loja.loja_controller import LojaController
from personagem.personagem_controller import PersonagemController


class HistoricoController:
    __ACAO__ = 'history'
    __bot_util__ = BotUtils.get_instance()
    __historico_escolhido__ = ''

    bot_controller = BotController.get_instance()

    def get_historico(self, params):
        resultado = self.__bot_util__.send_get(path=f'/historico/{params}')
        historico_json = json.loads(resultado.content)['results']
        return self.converte_historico_json_to_string(historico_json=historico_json)

    def converte_historico_json_to_string(self, historico_json):
        historico = ''

        if len(historico_json) > 0:
            for json in historico_json:
                historico += f'• {json["descricao"]}\n\n'

        else:
            historico = 'Não houveram transações.'

        historico = self.__bot_util__.escape_chars(historico)
        return historico

    def mostra_historico(self, call):
        params = ''
        chat_id = call.message.chat.id

        dados = json.loads(call.data)
        if self.__historico_escolhido__ == 'loja':
            loja_id = dados['id']
            params = f'?loja_id={loja_id}'
        else:
            personagem_id = dados['id']
            params = f'?personagem_id={personagem_id}'

        nome = dados['nome']
        historico = f'*Histórico de __{nome}__*\n'
        historico += self.get_historico(params=params)

        self.bot_controller.bot.delete_message(message_id=call.message.id, chat_id=chat_id)
        self.bot_controller.bot.send_message(chat_id=chat_id, text=historico, parse_mode='MarkdownV2')

    def inicia_interacao_historico(self, message):
        self.__bot_util__.set_uid_telegram(message.from_user.id)

        chat_id = message.chat.id
        text_confirmacao = 'Qual histórico deseja visualizar?'

        opcao_loja = InlineKeyboardButton(text='Loja', callback_data='loja')
        opcao_personagem = InlineKeyboardButton(text='Personagem', callback_data='personagem')

        markup = InlineKeyboardMarkup(row_width=2, keyboard=[[opcao_loja, opcao_personagem]])
        message = self.bot_controller.bot.send_message(chat_id=chat_id, text=text_confirmacao, reply_markup=markup)
        self.bot_controller.bot.register_callback_query_handler(func=lambda call: message.id == call.message.id,
                                                                callback=self.seleciona_historico)

    def seleciona_historico(self, call):
        opcao = call.data
        if opcao == 'loja':
            self.__historico_escolhido__ = 'loja'
            self.seleciona_loja(call=call)
        else:
            self.__historico_escolhido__ = 'personagem'
            self.seleciona_personagem(call=call)

    def seleciona_loja(self, call):
        loja_controller = LojaController()
        botoes = loja_controller.get_botoes_loja()
        chat_id = call.message.chat.id

        self.bot_controller.bot.delete_message(message_id=call.message.id, chat_id=chat_id)
        message = self.bot_controller.bot.send_message(chat_id=chat_id, text='Deseja ver o histórico de qual loja?',
                                                       reply_markup=botoes)
        self.bot_controller.bot.register_callback_query_handler(func=lambda call: message.id == call.message.id,
                                                                callback=self.mostra_historico)

    def seleciona_personagem(self, call):
        personagem_controller = PersonagemController()
        botoes = personagem_controller.get_botoes()
        chat_id = call.message.chat.id

        self.bot_controller.bot.delete_message(message_id=call.message.id, chat_id=chat_id)
        message = self.bot_controller.bot.send_message(chat_id=chat_id,
                                                       text='Deseja ver o histórico de qual personagem?',
                                                       reply_markup=botoes)
        self.bot_controller.bot.register_callback_query_handler(func=lambda call: message.id == call.message.id,
                                                                callback=self.mostra_historico)
