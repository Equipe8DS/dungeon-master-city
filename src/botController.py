import json

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from item.item_controller import ItemController
from loja.loja_controller import LojaController
from personagem.personagem_controller import PersonagemController


class BotController:
    __instance__ = None

    bot = telebot.TeleBot(token='')
    loja_controller = LojaController()
    personagem_controller = PersonagemController()
    item_controller = ItemController()

    loja_selecionada = {}
    item_selecionado = {}
    personagem_selecionado = {}
    quantidade_selecionada = {}

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

    def selecionar_item_loja(self, loja_id, chat_id):
        estoques_loja = self.loja_controller.buscar_estoque(loja_id=loja_id)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2

        for estoque in estoques_loja:
            item_json = {'id': estoque['item_id']}

            data = json.dumps({'acao': 'comprar', 'next': 'qtd', 'item': item_json})

            label = f'{estoque["item"]["nome"]} ({estoque["preco_item"]}G)'
            markup.add(InlineKeyboardButton(text=label, callback_data=data))

        self.bot.send_message(chat_id=chat_id, text='Qual item deseja comprar?', reply_markup=markup)

    def selecionar_loja(self, chat_id):
        lojas = self.loja_controller.buscar_loja()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2

        for loja in lojas:
            data = json.dumps({'acao': 'comprar', 'next': 'item', 'id': loja['pk'], 'nome': loja['nome']})
            markup.add(InlineKeyboardButton(loja['nome'], callback_data=data))

        self.bot.send_message(chat_id=chat_id, text='Em qual loja deseja comprar?', reply_markup=markup)

    def selecionar_personagem(self, chat_id):
        personagens = self.personagem_controller.buscar_personagens()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2

        for personagem in personagens:
            data = json.dumps({'acao': 'comprar', 'next': 'loja', 'id': personagem['pk'], 'nome': personagem['nome']})
            markup.add(InlineKeyboardButton(personagem['nome'], callback_data=data))

        self.bot.send_message(chat_id=chat_id, text='Para qual personagem deseja comprar?', reply_markup=markup)

    def selecionar_quantidade(self, chat_id):
        reply = self.bot.send_message(chat_id=chat_id, text='Quantos itens?', reply_markup=ForceReply())
        callback = lambda message: self.confirmar_compra(quantidade=message.text, chat_id=chat_id)
        self.bot.register_for_reply_by_message_id(message_id=reply.message_id, callback=callback)

    def confirmar_compra(self, quantidade, chat_id):
        self.quantidade_selecionada = quantidade

        text_confirmacao = f'Confirma compra de {self.quantidade_selecionada} {self.item_selecionado["nome"]} em ' \
                           f'{self.loja_selecionada["nome"]} para {self.personagem_selecionado["nome"]}?'

        opcao_sim = InlineKeyboardButton(text='Sim', callback_data=json.dumps({'acao': 'comprar', 'next': 'efetuar_compra',
                                                                               'opcao': 'sim'}))
        opcao_nao = InlineKeyboardButton(text='Não',
                                         callback_data=json.dumps({'acao': 'comprar', 'next': 'efetuar_compra',
                                                                   'opcao': 'nao'}))

        markup = InlineKeyboardMarkup(row_width=2, keyboard=[[opcao_sim, opcao_nao]])
        self.bot.send_message(chat_id=chat_id, text=text_confirmacao, reply_markup=markup)

    def efetuar_compra(self, opcao, chat_id):
        if opcao == 'sim':
            loja_id = self.loja_selecionada['id']
            item_id = self.item_selecionado['id']
            personagem_id = self.personagem_selecionado['id']

            response = self.loja_controller.comprar_item(quantidade=self.quantidade_selecionada, id_item=item_id,
                                                         id_loja=loja_id, id_personagem=personagem_id)
            self.bot.send_message(chat_id=chat_id, text=response)
        else:
            self.bot.send_message(chat_id=chat_id, text='Compra cancelada.')

    def processa_compra(self, dados):
        data = json.loads(dados.data)
        next = data['next']
        chat_id = dados.message.chat.id

        self.bot.delete_message(chat_id=chat_id, message_id=dados.message.id)

        if next == 'loja':
            self.personagem_selecionado['id'] = data['id']
            self.personagem_selecionado['nome'] = data['nome']
            self.selecionar_loja(chat_id=chat_id)
        elif next == 'item':
            self.loja_selecionada['id'] = data['id']
            self.loja_selecionada['nome'] = data['nome']
            self.selecionar_item_loja(loja_id=data['id'], chat_id=chat_id)
        elif next == 'qtd':
            self.item_selecionado['id'] = data['item']['id']
            self.item_selecionado['nome'] = self.item_controller.buscar_item_id(data['item']['id'])['nome']
            self.selecionar_quantidade(chat_id=chat_id)
        elif next == 'efetuar_compra':
            self.efetuar_compra(opcao=data['opcao'], chat_id=chat_id)
