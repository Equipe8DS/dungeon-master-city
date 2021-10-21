import json

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_utils import BotUtils


class PersonagemController:
    __bot_util__ = BotUtils.get_instance()

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

    def get_botoes(self):
        personagens = self.buscar_personagens()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2

        for personagem in personagens:
            data = json.dumps({'id': personagem['pk'], 'nome': personagem['nome']})
            markup.add(InlineKeyboardButton(personagem['nome'], callback_data=data))

        return markup
