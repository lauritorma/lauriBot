
# -*- coding: utf-8 -*-

import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config

# Random line from facts.txt

def lauri_fakta(update, context):
    with open('facts.txt', 'r', encoding='utf-8') as f:
        facts = f.readlines()

    fact = random.choice(facts).strip()

    context.bot.send_message(chat_id=update.message.chat_id, text=fact)

# Greet new group member

def greet_new_member(update, context):
    for member in update.message.new_chat_members:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Toivottakaa {member.first_name} tervetulleeksi LauriMafiaan! 🤝  \nJos haluat kuulla faktaa Laureista, kirjoita /laurifakta 👨‍🏫")

# Get member count

def get_group_members(update, context):
    chat_id = update.message.chat_id
    member_count = context.bot.get_chat_members_count(chat_id)
    context.bot.send_message(chat_id=chat_id, text=f"Laurimafiassa on tällä hetkellä {member_count} Lauria! Hyvää työtä Laurit! 😎")

# Message when bot joins group

def welcome_message(update, context):
    """Sends a welcome message when the bot is added to a group chat."""
    message = f"Laurimaista päivää kaikille! Minä olen {context.bot.name} ja olen saapunut jakamaan Laurien ilosanomaa! 🤝 \nJos haluat kuulla faktaa Laureista, kirjoita /laurifakta 👨‍🏫"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

welcome_handler = MessageHandler(Filters.status_update.new_chat_members, welcome_message)

# Updater for telegram bot

updater = Updater(token=config.API_KEY, use_context=True)

# Handler for random fact
updater.dispatcher.add_handler(CommandHandler('laurifakta', lauri_fakta))

# Handler for new member greeting
updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, greet_new_member))

# Handler for getting member count
updater.dispatcher.add_handler(CommandHandler('laurit', get_group_members))

# Handler for bot joining the group
updater.dispatcher.add_handler(welcome_handler)

# Start bot
updater.start_polling()

updater.idle()
