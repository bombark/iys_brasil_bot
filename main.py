#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
from uuid import uuid4
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
import toml




class Data:
    def __init__(self):
        with open('./data.toml', 'r') as fd:
            toml_string = fd.read()
            self.data = toml.loads(toml_string)
        print(self.data)

    def getBotId(self):
        return self.data["bot_id"]

    def getMembers(self):
        return self.data["members"]

    def getHelp(self):
        help = ""
        help += "/membros : mostra todos os membros\n"
        help += "/eventos : mostra todos os eventos\n"
        help += "/tarefas : mostra todas as tarefas\n"
        help += "/planilha : link da planilha\n"
        return help

gData = Data();




# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    #first_name = update.message.chat.first_name
    #last_name = update.message.chat.last_name
    username = update.message.chat.username
    text = "Opa "+str(username)+"!\n"+gData.getHelp()
    update.message.reply_text(text)


def status_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    #update.message.reply_text('status')

    chat_id = update.message.chat.id

    text = ""
    for i in range(1,25):
        text += '| | | | | |\n';

    context.bot.sendMessage(chat_id=chat_id, text="<b> aaa</b><table><tr><td>ssss</td></tr></table>", parse_mode="HTML")
    #context.bot.sendPhoto(chat_id=chat_id, photo="error1.png", caption="This is the test photo caption")
    #update.message.reply_text(text)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text( gData.getHelp() )


def link_planilha(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('http://bit.ly/centralbrazil')

def membros(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    membros = "# Membros\n"
    for user_id, name in gData.getMembers().items():
        membros += "- @"+user_id+"\n";

    chat_id = update.message.chat.id
    #context.bot.sendMessage(chat_id=chat_id, text="<b> aaa</b><table><tr><td>ssss</td></tr></table>", parse_mode="HTML")
    context.bot.sendMessage(chat_id=chat_id, text=membros, parse_mode="Markdown")



def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def tarefas(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    # markup = types.InlineKeyboardMarkup()
    # stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
    # for key, value in stringList.items():
    #     markup.add(
    #         types.InlineKeyboardButton(text=value, callback_data="['value', '" + value + "', '" + key + "']"),
    #         types.InlineKeyboardButton(text=crossIcon, callback_data="['key', '" + key + "']")
    #     )
    list_of_cities = ['Erode','Coimbatore','London', 'Thunder Bay', 'California']
    button_list = []
    for each in list_of_cities:
        button_list.append(InlineKeyboardButton(each, callback_data = each))
    reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1)) #n_cols = 1 is for single column and mutliple rows
    context.bot.send_message(chat_id=update.message.chat_id, text='Choose from the following',reply_markup=reply_markup)


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    print("opa")
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(), title="Caps", input_message_content=InputTextMessageContent(query.upper())
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            ),
        ),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            ),
        ),
    ]

    update.inline_query.answer(results)


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    #updater = Updater("1596057293:AAHsl_8tFYBwuBAUogQudRDlG5SbjRAjOkE", use_context=True)
    updater = Updater(gData.getBotId(), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("status", status_command))
    dispatcher.add_handler(CommandHandler("membros", membros))
    dispatcher.add_handler(CommandHandler("tarefas", tarefas))
    dispatcher.add_handler(CommandHandler("planilha", link_planilha))



    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
