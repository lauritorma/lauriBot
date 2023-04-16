
import random
from telegram.ext import Updater, CommandHandler
import config


def lauri_fakta(update, context):
    with open('facts.txt', 'r', encoding='utf-8') as f:
        facts = f.readlines()

    fact = random.choice(facts).strip()

    context.bot.send_message(chat_id=update.message.chat_id, text=fact)

updater = Updater(token=config.API_KEY, use_context=True)
updater.dispatcher.add_handler(CommandHandler('laurifakta', lauri_fakta))

updater.start_polling()
updater.idle()
