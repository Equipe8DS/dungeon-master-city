import json

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from botController import BotController
from bot_utils import BotUtils
from item.item_controller import ItemController


class PersonagemController:
    __bot_util__ = BotUtils.get_instance()
    __bot_controller__ = BotController.get_instance()
    __item_controller__ = ItemController()

    def buscar_personagens(self):
        request = self.__bot_util__.send_get('/personagem/')
        content = json.loads(request.content)
        personagens = content["results"]
        return personagens

    def buscar_personagem_nome(self, personagem_nome):
        request = self.__bot_util__.send_get(f'/personagem/?nome={personagem_nome}')
        content = json.loads(request.content)
        personagem = content["results"][0]
        return personagem

    def info_detalhada_personagem(self, personagem):
        info = f'Nome: {personagem["nome"]} \n' \
               f'Raça: {personagem["raca"]} \n' \
               f'Classe: {personagem["classe"]} \n' \
               f'Tipo: {personagem["tipo"]} \n'

        return info

    def iniciar_interacao_inventario(self, chat_id):
        botoes = self.get_botoes()
        message = self.__bot_controller__.bot.send_message(text='Deseja ver o inventário de qual personagem?',
                                                           chat_id=chat_id, reply_markup=botoes)
        self.__bot_controller__.bot.register_callback_query_handler(func=lambda call: message.id == call.message.id,
                                                                    callback=self.show_inventario)

    def get_inventario_personagem(self, personagem_id):
        request = self.__bot_util__.send_get(f'/inventario/?personagem_id={personagem_id}')
        content = json.loads(request.content)
        itens = content["results"]

        inventario = ''
        for item in itens:
            item_info = self.__item_controller__.info_detalhada_item(item=item['item'], show_preco=False)
            inventario += f'{item_info}' \
                          f'Quantidade: {item["quantidade"]}\n\n'

        inventario = self.__bot_util__.escape_chars(inventario)
        return inventario

    def get_botoes(self):
        personagens = self.buscar_personagens()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2

        for personagem in personagens:
            data = json.dumps({'id': personagem['pk'], 'nome': personagem['nome']})
            markup.add(InlineKeyboardButton(personagem['nome'], callback_data=data))

        return markup

    def show_inventario(self, call):
        chat_id = call.message.chat.id

        dados = json.loads(call.data)
        personagem_id = dados['id']
        nome_personagem = dados['nome']

        itens = self.get_inventario_personagem(personagem_id=personagem_id)
        inventario = f'*__Inventário do {nome_personagem}__*\n\n' \
                     f'{itens}'
        self.__bot_controller__.bot.send_message(text=inventario, chat_id=chat_id, parse_mode='MarkdownV2')
