import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
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

# Add new fact to facts.txt

INPUT_FACT = 0

def add_fact_start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Kirjoita uusi Laurifakta:")
    return INPUT_FACT

def add_fact_input(update, context):
    fact = update.message.text.strip()

    with open('facts.txt', 'a', encoding='utf-8') as f:
        f.write(fact + '\n')

    context.bot.send_message(chat_id=update.message.chat_id, text="Uusi fakta on lisätty!")

    return ConversationHandler.END

# Get member count

def get_group_members(update, context):
    chat_id = update.message.chat_id
    member_count = context.bot.get_chat_members_count(chat_id)
    context.bot.send_message(chat_id=chat_id, text=f"LauriMafiassa on tällä hetkellä {member_count} jäsentä! Hyvä Laurit!")

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

# Handler for adding a new fact
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('uusifakta', add_fact_start)],
    states={
        INPUT_FACT: [MessageHandler(Filters.text, add_fact_input)]
    },
    fallbacks=[]
)
updater.dispatcher.add_handler(conv_handler)


# Handler for bot joining the group
updater.dispatcher.add_handler(welcome_handler)

# Start bot
updater.start_polling()

updater.idle()
