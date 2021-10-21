import json

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_utils import BotUtils
from item.item_controller import ItemController
from personagem.personagem_controller import PersonagemController


class LojaController:
    __bot_util__ = BotUtils.get_instance()
    personagem_controller = PersonagemController()
    item_controller = ItemController()

    def buscar_estoque(self, loja_id):
        request = self.__bot_util__.send_get(path=f'/estoque/?loja_id={loja_id}')
        a_json_object = json.loads(request.content)
        list_from_json = a_json_object["results"]
        return list_from_json

    def buscar_loja(self):
        request = self.__bot_util__.send_get(path='/loja/')
        content = json.loads(request.content)
        lojas = content["results"]
        return lojas

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
        info = f'Nome: {loja["nome"]} \n' \
               f'Cidade: {loja["cidade"]} \n' \
               f'Responsável: {loja["responsavel"]} \n' \
               f'Ativo: {loja["ativo"]}'

        return info

    def get_botoes_loja(self):
        lojas = self.buscar_loja()
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
