import json

from botController import BotController
from botController import BotController


class ItemController:
    __bot_controller__ = BotController()
    __bot_util__ = BotController()

    QUALIDADE = {
        'ruim': 'Ruim',
        'pobre': 'Pobre',
        'medio': 'Médio',
        'bom': 'Bom',
        'excelente': 'Excelente',
    }
    CATEGORIA = {
        'alimentos': 'Alimentos',
        'transporte': 'Transporte',
        'academico': 'Acadêmico',
        'agricultura': 'Agricultura',
        'casa': 'Casa',
        'equipamento': 'Equipamento',
        'luxo': 'Luxo',
    }

    def buscar_item_nome(self, item_nome):
        request = self.__bot_util__.send_get(path=f'/item/?nome={item_nome}')

        content = json.loads(request.content)
        item = content["results"][0]
        return item

    def buscar_itens(self):
        request = self.__bot_util__.send_get(path='/item/')

        content = json.loads(request.content)
        itens = content["results"]
        return itens

    def imprime_categoria(self, categoria):
        return self.CATEGORIA[categoria]

    def imprime_qualidade(self, qualidade):
        return self.QUALIDADE[qualidade]

    def info_detalhada_item(self, item, show_preco=True):
        if show_preco:
            info = f'Nome: {item["nome"]} \n' \
                   f'Preço Sugerido: {item["preco_sugerido"]} peças de ouro \n' \
                   f'Qualidade: {self.imprime_qualidade(qualidade=item["qualidade"])} \n' \
                   f'Categoria: {self.imprime_categoria(item["categoria"])} \n' \
                   f'Descrição: {item["descricao"]} \n'
        else:
            info = f'Nome: {item["nome"]} \n' \
                   f'Qualidade: {self.imprime_qualidade(qualidade=item["qualidade"])} \n' \
                   f'Categoria: {self.imprime_categoria(item["categoria"])} \n' \
                   f'Descrição: {item["descricao"]} \n'

        return info
