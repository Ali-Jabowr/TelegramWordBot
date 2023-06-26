from firebase_admin import db
from functions import keyboard_handler

class ShowVocabularyHandler:
    def __init__(self, bot, users_ref):
        self.bot = bot
        self.callback_handler = None
        self.user_input_handler = None
        self.users_ref = users_ref
        
    def register(self, call):
        chat_id = call.message.chat.id

        if call.data == 'show':
            self.bot.send_message(chat_id, "Here are your vocabularies:", parse_mode="HTML")

            if self.callback_handler:
                self.bot.remove_handler(self.callback_handler)
            if self.user_input_handler:
                self.bot.remove_handler(self.user_input_handler)

            self.callback_handler = self.bot.register_next_step_handler(call.message, self.handle_show_vocabulary(call.message, call.from_user.id))
                

    def handle_show_vocabulary(self, message, user_id):            
        curr_user = self.users_ref.child(f'{user_id}')
        vocabs_ref = db.reference(f'/users/{user_id}/vocabs').get()
        chat_id = message.chat.id
        
        if vocabs_ref:
            for key, value in vocabs_ref.items():
                self.bot.send_message(chat_id, f"{key} : {value}")
            self.bot.send_message(chat_id, "Please choose an option: ", reply_markup=keyboard_handler())
            
        else:
            self.bot.send_message(chat_id, "You don't have any vocabulary.")
            self.bot.send_message(chat_id, "Do you want to add any? ", reply_markup=keyboard_handler())
