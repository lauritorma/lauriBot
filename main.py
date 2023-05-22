# -*- coding: utf-8 -*-
import random
import datetime
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
        welcome_message = "Toivottakaa {name} tervetulleeksi LauriMafiaan! \U0001F91D\nJos haluat kuulla faktaa Laureista, kirjoita /laurifakta \U0001F468‍🏫".format(name=member.first_name)
        context.bot.send_message(chat_id=update.message.chat_id, text=welcome_message)

# Get member count

def get_group_members(update, context):
    chat_id = update.message.chat_id
    member_count = context.bot.get_chat_members_count(chat_id)
    count_message = "Laurimafiassa on tällä hetkellä {} Lauria! Hyvää työtä Laurit! \U0001F60E".format(member_count)
    context.bot.send_message(chat_id=chat_id, text=count_message)

# Send random text from randomText.txt

def send_random_text(context):
    with open('randomText.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    random_line = random.choice(lines).strip()

    context.bot.send_message(chat_id=config.GROUP_CHAT_ID, text=random_line)

# Message when bot joins group

def welcome_message(update, context):
    """Sends a welcome message when the bot is added to a group chat."""
    message = "Laurimaista päivää kaikille! Minä olen {bot_name} ja olen saapunut jakamaan Laurien ilosanomaa! \U0001F91D\nJos haluat kuulla faktaa Laureista, kirjoita /laurifakta \U0001F468‍🏫".format(bot_name=context.bot.name)
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

# Handler for sending random text
updater.job_queue.run_daily(send_random_text, time=datetime.time(hour=random.randint(0, 23), minute=random.randint(0, 59)), days=(0, 1, 2, 3, 4, 5, 6), context=config.GROUP_CHAT_ID, name='random_text')

# Handler for bot joining the group
updater.dispatcher.add_handler(welcome_handler)

# Start bot
updater.start_polling()

updater.idle()
