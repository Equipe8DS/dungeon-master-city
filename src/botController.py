import telebot
from telebot.types import BotCommand


class BotController:
    __instance__ = None

    bot = telebot.TeleBot(token='')

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

    def set_commmands(self):
        commands = [
            BotCommand(command='start', description='Usado para iniciar o bot.'),
            BotCommand(command='help', description='Exibe lista de comandos.'),
            BotCommand(command='loja', description='Exibe informações de uma loja.'),
            BotCommand(command='estoque', description='Exibe o estoque de uma loja.'),
            BotCommand(command='comprar', description='Usado para comprar itens para um personagem.'),
            BotCommand(command='cidade', description='Exibe informações de uma cidade.'),
            BotCommand(command='personagem', description='Exibe informações de um personagem.'),
            BotCommand(command='inventario', description='Exibe o inventário de um personagem.'),
            BotCommand(command='itens', description='Exibe lista de itens.'),
            BotCommand(command='item', description="Exibe informações de um item."),
            BotCommand(command='historico', description='Exibe o histórico de um personagem ou loja.'),
        ]

        self.bot.set_my_commands(commands=commands)
