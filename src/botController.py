import telebot


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
