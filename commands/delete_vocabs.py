from firebase_admin import db
from functions import keyboard_handler

class DeleteVocabularyHandler:
    def __init__(self, bot, users_ref):
        self.bot = bot
        self.callback_handler = None
        self.user_input_handler = None
        self.users_ref = users_ref
        
    def register(self, call):
        chat_id = call.message.chat.id

        if call.data == 'delete':
            self.bot.send_message(chat_id, "Please enter which vocabulary you want to delete:", parse_mode="HTML")
            
            if self.callback_handler:
                self.bot.remove_handler(self.callback_handler)
            if self.user_input_handler:
                self.bot.remove_handler(self.user_input_handler)
                
            self.callback_handler = self.bot.register_next_step_handler(call.message, self.handle_user_input(call.message, call.from_user.id))
    
    def handle_user_input(self, message, user_id):
        def inner_handler(message):
            vocabulary = message.text
            self.handle_delete_handler(self.users_ref, user_id, vocabulary, message)
        return inner_handler
                
from firebase_admin import db
from functions import keyboard_handler

class DeleteVocabularyHandler:
    def __init__(self, bot, users_ref):
        self.bot = bot
        self.callback_handler = None
        self.user_input_handler = None
        self.users_ref = users_ref
        
    def register(self, call):
        chat_id = call.message.chat.id

        if call.data == 'delete':
            self.bot.send_message(chat_id, "Please enter which vocabulary you want to delete:", parse_mode="HTML")
            
            if self.callback_handler:
                self.bot.remove_handler(self.callback_handler)
            if self.user_input_handler:
                self.bot.remove_handler(self.user_input_handler)
                
            self.callback_handler = self.bot.register_next_step_handler(call.message, self.handle_user_input(call.message, call.from_user.id))
    
    def handle_user_input(self, message, user_id):
        def inner_handler(message):
            vocabulary = message.text
            self.handle_delete_handler(self.users_ref, user_id, vocabulary, message)
        return inner_handler
                
    def handle_delete_handler(self, users_ref, user_id, user_input, message):
        user_input = user_input.lower().strip()
        curr_user = None
        try:
            curr_user = users_ref.child(str(user_id))
        except AttributeError:
            self.bot.send_message(message.chat.id, "Error: Invalid user reference.")
            return
        
        vocabs_ref = db.reference(f'/users/{user_id}/vocabs').get()
        chat_id = message.chat.id 
        
        if vocabs_ref is not None and isinstance(vocabs_ref, dict):
            # Copy the existing vocabulary dictionary
            new_vocab = vocabs_ref.copy()
        else:
            self.bot.send_message(chat_id, "Vocabulary dictionary is empty.")
            self.bot.send_message(chat_id, "Please choose an option: ", reply_markup=keyboard_handler())   
            return
        
        if user_input in [key.lower().strip() for key in new_vocab]:
            try:
                # Exclude the specified key from the dictionary using a dictionary comprehension
                new_vocab = {key: value for key, value in new_vocab.items() if key.strip().lower() != user_input}  
                # Update the 'vocabs' value in the database
                curr_user.update({'vocabs': new_vocab})
                self.bot.send_message(chat_id, f"'{user_input}' deleted successfully!")
                self.bot.send_message(chat_id, "Please choose an option: ", reply_markup=keyboard_handler())
            except Exception as e:
                self.bot.send_message(chat_id, f"Error occurred while deleting vocabulary: {str(e)}")
        else:
            self.bot.send_message(chat_id, "User input does not exist in the vocabulary dictionary.")
            self.bot.send_message(chat_id, "Please choose an option: ", reply_markup=keyboard_handler())
