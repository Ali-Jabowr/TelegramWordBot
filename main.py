import telebot
from telebot import types, apihelper

import firebase_admin
from firebase_admin import db

from commands.add_vocabs import AddVocabsHandler
from commands.start_command import SatrtCommandHandler
from commands.delete_vocabs import DeleteVocabularyHandler
from commands.show_vocabs import ShowVocabularyHandler
from commands.edit_vocabs import EditVocabularyHandler
from commands.chatgpt_api import ChatgptAPI

# Firebase configuration
def configure_firebase():
    cred_obj = firebase_admin.credentials.Certificate('wordbot-81fab-firebase-adminsdk-4581q-a4242a14a5.json')
    default_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL': 'https://wordbot-81fab-default-rtdb.firebaseio.com/'
    })
    ref = db.reference("/")
    users_ref = ref.child('users')
    return users_ref

# Set the session time to live value (in seconds)
apihelper.SESSION_TIME_TO_LIVE = 900  # 15 minutes

API_TOKEN = '6075208758:AAH1EQvJS93Of7bu6UbDSlG6rwro0b8Q8T0'
bot = telebot.TeleBot(API_TOKEN)
users_ref = configure_firebase()

# Create instances of the handlers
add_vocabs = AddVocabsHandler(bot, users_ref)
start_handler = SatrtCommandHandler(bot)
delete_handler = DeleteVocabularyHandler(bot, users_ref)
show_handler = ShowVocabularyHandler(bot, users_ref)
edit_handler = EditVocabularyHandler(bot, users_ref)
chatgpt_handler = ChatgptAPI(bot)

# Register the handlers
start_handler.register(users_ref)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'add':
        add_vocabs.register(call)
    elif call.data == 'delete':
        delete_handler.register(call)
    elif call.data == 'edit':
        edit_handler.register(call)
    elif call.data == 'show':
        show_handler.register(call)
    elif call.data == 'chatgpt':
        chatgpt_handler.register(call)
    elif call.data == 'yes' or call.data == 'no':
        ChatgptAPI.handle_chatgpt_keyboard(ChatgptAPI, call)
    else:
        start_handler.register(users_ref)

# Start the bot
bot.infinity_polling()
