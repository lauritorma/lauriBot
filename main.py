
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config

#Random line from facts.txt

def lauri_fakta(update, context):
    with open('facts.txt', 'r', encoding='utf-8') as f:
        facts = f.readlines()

    fact = random.choice(facts).strip()

    context.bot.send_message(chat_id=update.message.chat_id, text=fact)

# Greet new group member

def greet_new_member(update, context):
    for member in update.message.new_chat_members:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Toivottakaa {member.first_name} tervetulleeksi LauriMafiaan! 🤝  \nJos haluat kuulla faktaa Laureista, kirjoita /laurifakta 👨‍🏫")


# Updater for telegram bot 

updater = Updater(token=config.API_KEY, use_context=True)

# handler for random fact
updater.dispatcher.add_handler(CommandHandler('laurifakta', lauri_fakta))

# handler for new member greeting 

updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, greet_new_member))

# start bot

updater.start_polling()

updater.idle()
