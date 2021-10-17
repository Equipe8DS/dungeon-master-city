import json
import os

import telebot
from dotenv import load_dotenv

from botController import BotController
from cidade.cidade_controller import CidadeController
from item.item_controller import ItemController
from jogador.jogador_controller import JogadorController
from loja.loja_controller import LojaController
from personagem.personagem_controller import PersonagemController

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(token=bot_token)

bot_controller = BotController()
cidade_controller = CidadeController()
item_controller = ItemController()
jogador_controller = JogadorController()
loja_controller = LojaController()
personagem_controller = PersonagemController()


# @bot.message_handler(commands=['comprar'])
# def comprar_item(message):
#     cid = message.chat.id
#     nome_personagem, nome_loja, nome_item, quantidade = message.text.split(' ')[1:]
#     bot.send_chat_action(cid, 'typing')
#
#     if not nome_loja or not nome_personagem or not nome_item or not quantidade:
#         bot.send_message(cid, "Campos faltantes.")
#     else:
#         mensagem_processamento = bot.send_message(cid, text='Processando a compra, por favor aguarde...',
#                                                   parse_mode="Markdown")
#         try:
#             bot.send_chat_action(cid, 'typing')
#
#             info = loja_controller.comprar_item(nome_loja, nome_personagem, nome_item, quantidade)
#             bot.delete_message(message_id=mensagem_processamento.message_id, chat_id=cid)
#             bot.send_message(chat_id=cid, text=info)
#         except Exception as e:
#             print(e)
#             bot.delete_message(message_id=mensagem_processamento.message_id, chat_id=mensagem_processamento.chat.id)
#             bot.send_message(chat_id=cid, text='Houve um erro ao comprar o item.')

@bot.message_handler(commands=['comprar'])
def comprar_item(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')
    bot_controller.selecionar_personagem(chat_id=cid)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot_controller.processa_compra(dados=call)


@bot.message_handler(commands=['cidades'])
def send_cidades_lista(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')

    results = cidade_controller.buscar_cidade()
    response = bot_controller.gerar_lista_por_nomes(list=results)
    bot.reply_to(message, "Cidades registradas: \n" + response, parse_mode="Markdown")


@bot.message_handler(commands=['jogadores'])
def send_jogadores_lista(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')

    results = jogador_controller.buscar_jogador()
    response = bot_controller.gerar_lista_por_nomes(results)
    bot.reply_to(message, "Jogadores registrados: \n" + response, parse_mode="Markdown")


@bot.message_handler(commands=['cidade'])
def send_info_cidade(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')

    results = cidade_controller.buscar_cidade()
    response_dict = bot_controller.gerar_dicionario_lista_por_nome(results)

    cidade_name = ' '.join(message.text.split(' ')[1:])

    if not cidade_name:
        bot.send_message(cid, "Insira o nome da cidade que deseja visualizar.")
    else:
        try:
            info = cidade_controller.info_detalhada_cidade(cidade=response_dict[cidade_name])
            bot.send_message(cid, info, parse_mode="Markdown")
        except Exception as e:
            print(e)
            bot.send_message(cid, "Houve um erro ao consultar a cidade.", parse_mode="Markdown")


@bot.message_handler(commands=['estoque'])
def send_info_estoque(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')

    loja_name = ' '.join(message.text.split(' ')[1:])
    loja = loja_controller.buscar_loja_nome(loja_nome=loja_name)

    if not loja_name:
        bot.send_message(cid, "Insira o nome da loja que deseja visualizar o estoque.")
    else:
        try:
            info = loja_controller.info_detalhada_estoque(loja=loja)
            bot.send_message(cid, 'Estoque da loja ' + loja_name + ': \n\n' + info, parse_mode="Markdown")
        except Exception as e:
            print(e)
            bot.send_message(cid, "Houve um erro ao consultar a loja.", parse_mode="Markdown")


@bot.message_handler(commands=['item'])
def send_info_item(message):
    cid = message.chat.id
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
    bot.send_chat_action(cid, 'typing')

    try:
        loja_name = ' '.join(message.text.split(' ')[1:])
        loja = loja_controller.buscar_loja_nome(loja_nome=loja_name)

        if not loja_name:
            bot.send_message(cid, "Insira o nome da loja que deseja visualizar.")
        else:
            info = loja_controller.info_detalhada_loja(loja=loja)
            bot.send_message(cid, info, parse_mode="Markdown")
    except Exception as e:
        print(e)
        bot.send_message(cid, "Houve um erro ao consultar a loja.", parse_mode="Markdown")


@bot.message_handler(commands=['personagem'])
def send_info_personagem(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')

    try:
        personagem_name = ' '.join(message.text.split(' ')[1:])
        personagem = personagem_controller.buscar_personagem_nome(personagem_nome=personagem_name)

        if not personagem_name:
            bot.send_message(cid, "Insira o nome do personagem que deseja visualizar.")
        else:
            info = personagem_controller.info_detalhada_personagem(personagem)
            bot.send_message(cid, info, parse_mode="Markdown")
    except Exception as e:
        print(e)
        bot.send_message(cid, "Houve um erro ao consultar o personagem.", parse_mode="Markdown")


@bot.message_handler(commands=['itens'])
def send_itens_lista(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')

    results = item_controller.buscar_itens()
    response = bot_controller.gerar_lista_por_nomes(results)
    bot.reply_to(message, "Itens registrados: \n" + response, parse_mode="Markdown")


@bot.message_handler(commands=['lojas'])
def send_lojas_lista(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')

    results = loja_controller.buscar_loja()
    response = bot_controller.gerar_lista_por_nomes(list=results)
    bot.reply_to(message, "Lojas registradas: \n" + response, parse_mode="Markdown")


@bot.message_handler(commands=['personagens'])
def send_personagens_lista(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')

    results = personagem_controller.buscar_personagens()
    response = bot_controller.gerar_lista_por_nomes(results)
    bot.reply_to(message, "Personagens registrados: \n" + response, parse_mode="Markdown")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')
    bot.reply_to(message, "Seja bem-vindo ! A grande Redzay te espera.")


bot_controller.bot = bot
bot.polling(non_stop=True)
# while True:
#    try:
#        bot.polling()
#    except Exception:
#        time.sleep(15)