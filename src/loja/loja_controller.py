import json

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from botController import BotController
from bot_utils import BotUtils
from item.item_controller import ItemController
from personagem.personagem_controller import PersonagemController


class LojaController:
    __bot_util__ = BotUtils.get_instance()
    __bot_controller__ = BotController.get_instance()
    personagem_controller = PersonagemController()
    item_controller = ItemController()

    def buscar_estoque(self, loja_id):
        request = self.__bot_util__.send_get(path=f'/estoque/?loja_id={loja_id}')
        a_json_object = json.loads(request.content)
        list_from_json = a_json_object["results"]
        return list_from_json

    def buscar_lojas(self):
        request = self.__bot_util__.send_get(path='/loja/')
        content = json.loads(request.content)
        lojas = content["results"]
        return lojas

    def buscar_loja(self, loja_id):
        request = self.__bot_util__.send_get(path=f'/loja/{loja_id}/')
        loja = json.loads(request.content)
        return loja

    def buscar_loja_nome(self, loja_nome):
        request = self.__bot_util__.send_get(path=f'/loja/?nome={loja_nome}')
        content = json.loads(request.content)
        loja = content["results"][0]
        return loja

    def comprar_item(self, id_loja, id_personagem, id_item, quantidade):
        request = self.__bot_util__.send_post(path='/loja/comprar-item/',
                                              data={'idLoja': id_loja, 'idPersonagem': id_personagem, 'idItem': id_item,
                                                    'quantidade': quantidade})
        content = json.loads(request.content)
        response_message = content['message']
        if 'lojaHasEstoque' in content or 'personagemHasGold' in content:
            if not content['lojaHasEstoque']:
                response_message += ' Loja não possui estoque suficiente.'
            elif not content['personagemHasGold']:
                response_message += ' Personagem não possui ouro suficiente.'

        return response_message

    def escolher_loja_info(self, chat_id):
        lojas = self.get_botoes_loja()
        message = self.__bot_controller__.bot.send_message(text='Deseja ver informações de qual loja?',
                                                           chat_id=chat_id, reply_markup=lojas)
        self.__bot_controller__.bot.register_callback_query_handler(func=lambda call: message.id == call.message.id,
                                                                    callback=self.show_info_loja)

    def gerar_dicionario_lista_por_nome_itens_estoque(self, itens):
        list_dict = {item['item']['nome']: item for item in itens}
        return list_dict

    def info_detalhada_estoque(self, loja):
        estoque = self.buscar_estoque(loja['pk'])
        response_dict = self.gerar_dicionario_lista_por_nome_itens_estoque(estoque)

        info = ""

        for key in response_dict:
            elem = response_dict[key]
            item = elem['item']
            info_item = self.item_controller.info_detalhada_item(item=item, show_preco=False)

            info += f'{info_item}\n' \
                    f'Preço: {elem["preco_item"]} peças de ouro \n' \
                    f'Quantidade: {elem["quantidade_item"]} \n' \
                    f'==================== \n'

        return info

    def info_detalhada_loja(self, loja):
        info = f'*::::::::::  {loja["nome"]} ::::::::::*\n' \
               f'Cidade: {loja["cidade"]} \n' \
               f'Responsável: {loja["responsavel"]} \n'

        info = self.__bot_util__.escape_chars(info)
        return info

    def get_botoes_loja(self):
        lojas = self.buscar_lojas()
        markup = InlineKeyboardMarkup()
        markup.row_width = 2

        for loja in lojas:
            data = json.dumps({'id': loja['pk'], 'nome': loja['nome']})
            markup.add(InlineKeyboardButton(loja['nome'], callback_data=data))

        return markup

    def get_botoes_estoque(self, loja_id):
        estoques_loja = self.buscar_estoque(loja_id=loja_id)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2

        for estoque in estoques_loja:
            data = json.dumps({'id': estoque['item_id'], 'nome': estoque['item']['nome']})
            label = f'{estoque["item"]["nome"]} ({estoque["preco_item"]}G)'
            markup.add(InlineKeyboardButton(text=label, callback_data=data))

        return markup

    def show_info_loja(self, call):
        chat_id = call.message.chat.id

        dados = json.loads(call.data)
        id_loja = dados['id']

        loja = self.buscar_loja(loja_id=id_loja)
        info_loja = self.info_detalhada_loja(loja=loja)
        self.__bot_controller__.bot.send_message(text=info_loja, chat_id=chat_id, parse_mode='MarkdownV2')
