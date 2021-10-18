import json

from bot_utils import BotUtils


class PersonagemController:
    __bot_util__ = BotUtils()

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

    def inventario_personagem(self, personagem_id):
        request = self.__bot_util__.send_get(f'/inventario/?personagem_id={personagem_id}')
        content = json.loads(request.content)
        inventario = content["results"]
        i = 1
        response = ""
        for object in inventario:
            desc = "\n     Descrição: " + object["item"]["descricao"]
            cat = "\n     Categoria: " + object["item"]["categoria"]
            response = response + str(i) + " - " +  "Nome: " + object["item"]["nome"] + cat +  desc  + "\n" 
            i = i + 1
        return "Inventario de personagem " + personagem_id + ': \n' + response   
