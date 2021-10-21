import json

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from botController import BotController
from bot_utils import BotUtils


class CidadeController:
    __bot_util__ = BotUtils.get_instance()
    __bot_controller__ = BotController.get_instance()

    def buscar_cidade(self, cidade_id):
        request = self.__bot_util__.send_get(path=f'/cidade/{cidade_id}/')
        cidade = json.loads(request.content)

        return cidade

    def buscar_cidades(self):
        request = self.__bot_util__.send_get(path='/cidade/')

        a_json_object = json.loads(request.content)
        list_from_json = a_json_object["results"]
        return list_from_json

    def escolher_cidade_info(self, chat_id):
        cidades = self.get_botoes_cidade()
        message = self.__bot_controller__.bot.send_message(text='Deseja ver informações de qual cidade?',
                                                           chat_id=chat_id, reply_markup=cidades)
        self.__bot_controller__.bot.register_callback_query_handler(func=lambda call: message.id == call.message.id,
                                                                    callback=self.__show_info_cidade__)

    def get_botoes_cidade(self):
        cidades = self.buscar_cidades()

        markup = InlineKeyboardMarkup()
        markup.row_width = 2

        for cidade in cidades:
            data = json.dumps({'id': cidade['pk'], 'nome': cidade['nome']})
            label = f'{cidade["nome"]}'
            markup.add(InlineKeyboardButton(text=label, callback_data=data))

        return markup

    def __info_detalhada_cidade__(self, cidade):
        info = f'*::::::::::  {cidade["nome"]} ::::::::::*\n' \
               f'Governante: {cidade["governante"]["nome"]}\n' \
               f'Tesouro: {cidade["tesouro"]} peças de ouro'

        info = self.__bot_util__.escape_chars(info)
        return info

    def __show_info_cidade__(self, call):
        chat_id = call.message.chat.id

        dados = json.loads(call.data)
        id_cidade = dados['id']

        cidade = self.buscar_cidade(cidade_id=id_cidade)
        info_cidade = self.__info_detalhada_cidade__(cidade=cidade)
        self.__bot_controller__.bot.send_message(text=info_cidade, chat_id=chat_id, parse_mode='MarkdownV2')
