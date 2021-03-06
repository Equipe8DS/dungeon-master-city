import os

import telebot
from dotenv import load_dotenv
from telebot.types import BotCommandScopeDefault

from botController import BotController
from bot_utils import BotUtils
from cidade.cidade_controller import CidadeController
from historico.historico_controller import HistoricoController
from item.item_controller import ItemController
from jogador.jogador_controller import JogadorController
from loja.compra_controller import CompraController
from loja.loja_controller import LojaController
from personagem.personagem_controller import PersonagemController

bot_controller = BotController.get_instance()
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
bot_controller.bot = telebot.TeleBot(token=bot_token)
bot = bot_controller.bot

cidade_controller = CidadeController()
item_controller = ItemController()
jogador_controller = JogadorController()
loja_controller = LojaController()
compra_controller = CompraController()
personagem_controller = PersonagemController()
historico_controller = HistoricoController()
bot_util = BotUtils.get_instance()


@bot.message_handler(commands=['comprar'])
def comprar_item(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot_util.set_uid_telegram(uid)
    bot.send_chat_action(cid, 'typing')
    compra_controller.iniciar_interacao(chat_id=cid)


@bot.message_handler(commands=['jogadores'])
def send_jogadores_lista(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot_util.set_uid_telegram(uid)
    bot.send_chat_action(cid, 'typing')

    results = jogador_controller.buscar_jogadores()
    response = bot_controller.gerar_lista_por_nomes(results)
    bot.reply_to(message, "Jogadores registrados: \n" + response, parse_mode="Markdown")


@bot.message_handler(commands=['cidade'])
def send_info_cidade(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot_util.set_uid_telegram(uid)
    bot.send_chat_action(cid, 'typing')

    cidade_controller.escolher_cidade_info(chat_id=cid)


@bot.message_handler(commands=['estoque'])
def send_info_estoque(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot_util.set_uid_telegram(uid)
    bot.send_chat_action(cid, 'typing')

    loja_controller.escolher_estoque_loja(chat_id=cid)


@bot.message_handler(commands=['item'])
def send_info_item(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot_util.set_uid_telegram(uid)
    bot.send_chat_action(cid, 'typing')

    try:
        item_name = ' '.join(message.text.split(' ')[1:])
        item = item_controller.buscar_item_nome(item_nome=item_name)

        if not item_name:
            bot.send_message(cid, "Insira o nome do item que deseja visualizar.")
        else:
            info = item_controller.info_detalhada_item(item=item)
            bot.send_message(cid, info, parse_mode="Markdown")
    except Exception as e:
        print(e)
        bot.send_message(cid, "Houve um erro ao consultar o item.", parse_mode="Markdown")


@bot.message_handler(commands=['jogador'])
def send_info_jogador(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot_util.set_uid_telegram(uid)
    bot.send_chat_action(cid, 'typing')

    results = jogador_controller.buscar_jogador()
    response_dict = bot_controller.gerar_dicionario_lista_por_nome(results)

    jogador_name = ' '.join(message.text.split(' ')[1:])

    if not jogador_name:
        bot.send_message(cid, "Insira o nome do jogador que deseja visualizar.")
    else:
        try:
            info = jogador_controller.info_detalhada_jogador(jogador=response_dict[jogador_name])
            bot.send_message(cid, info, parse_mode="Markdown")
        except Exception as e:
            print(e)
            bot.send_message(cid, "Houve um erro ao consultar o jogador.", parse_mode="Markdown")


@bot.message_handler(commands=['loja'])
def send_info_loja(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot_util.set_uid_telegram(uid)
    bot.send_chat_action(cid, 'typing')

    loja_controller.escolher_loja_info(chat_id=cid)


@bot.message_handler(commands=['personagem'])
def send_info_personagem(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')

    uid = message.from_user.id
    bot_util.set_uid_telegram(uid)

    personagem_controller.escolher_personagem_info(chat_id=cid)


@bot.message_handler(commands=['inventario'])
def send_inventario_personagem(message):
    cid = message.chat.id
    bot_controller.bot.send_chat_action(chat_id=cid, action='typing')

    uid = message.from_user.id
    bot_util.set_uid_telegram(uid_telegram=uid)

    personagem_controller.iniciar_interacao_inventario(chat_id=cid)


@bot.message_handler(commands=['itens'])
def send_itens_lista(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot_util.set_uid_telegram(uid)
    bot.send_chat_action(cid, 'typing')

    results = item_controller.buscar_itens()
    response = bot_controller.gerar_lista_por_nomes(results)
    bot.reply_to(message, "Itens registrados: \n" + response, parse_mode="Markdown")


@bot.message_handler(commands=['historico'])
def send_historico(message):
    historico_controller.inicia_interacao_historico(message=message)

@bot.message_handler(commands='help')
def send_historico(message):
    chat_id = message.chat.id

    commands = bot.get_my_commands(scope=BotCommandScopeDefault(), language_code='')
    message = '*Seja bem-vindo! A grande Redzay te espera.*\n\n' \
              'A seguir, a lista de comandos dispon??veis para este bot.\n\n'

    for command in commands:
        message += f'/{command.command}: {command.description}\n\n'

    message = bot_util.escape_chars(message)
    bot.send_message(chat_id=chat_id, text=message, parse_mode='MarkdownV2')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    uid = message.from_user.id
    bot_util.set_uid_telegram(uid)

    jogador_controller.inserir_username(cid)


bot_controller.set_commmands()
bot.polling(non_stop=True)
# while True:
#    try:
#        bot.polling()
#    except Exception:
#        time.sleep(15)
