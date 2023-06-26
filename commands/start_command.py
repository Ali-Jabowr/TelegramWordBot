from functions import *

class SatrtCommandHandler:
    def __init__(self, bot) -> None:
        self.bot = bot

    def register(self, users_ref):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            global user_id
            user_id = message.from_user.id
            
            user_ref = users_ref.child(f'{message.from_user.id}')
            user_ref.set({
                "id": message.from_user.id,
                "name": message.from_user.username,
            })
            # Send a welcome message
            self.bot.send_message(message.chat.id, "Welcome to the Vocabulary Bot!") 
            # Send the keyboard as a reply
            self.bot.send_message(message.chat.id, "What would you like to do?", reply_markup=keyboard_handler())






