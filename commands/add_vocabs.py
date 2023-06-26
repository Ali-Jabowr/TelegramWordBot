from functions import keyboard_handler
from firebase_admin import db

class AddVocabsHandler:
    def __init__(self, bot, users_ref):
        self.bot = bot
        self.user_vocabularies = {}
        self.callback_handler = None
        self.user_input_handler = None
        self.users_ref = users_ref
    
    def register(self, call):
        # Register the callback for adding vocabs
        chat_id = call.message.chat.id

        if call.data == 'add':
            self.bot.send_message(chat_id, "Please enter a new vocabulary:\nLike this: vocabulary1:translation, vocabulary2:translation, ...", parse_mode="HTML")

            if self.callback_handler:
                self.bot.remove_handler(self.callback_handler)
            if self.user_input_handler:
                self.bot.remove_handler(self.user_input_handler)

            self.callback_handler = self.bot.register_next_step_handler(call.message, self.handle_user_input, call.from_user.id)

    def handle_user_input(self, message, user_id):
        # Handle the user's input for adding vocabs
        vocabulary = message.text
        self.handle_add(message, user_id, vocabulary)

    def handle_add(self, message, user_id, vocabulary):
        '''
        Handle the addition of vocabulary entries for a user.

        Parameters:
            - message (Telegram Message object): The Telegram message object containing the user's input.
            - user_id (str): The unique identifier for the user.
            - vocabulary (str): The vocabulary input provided by the user.
        '''
        curr_user = self.users_ref.child(f'{user_id}')
        vocabs_ref = db.reference(f'/users/{user_id}/vocabs').get()
        chat_id = message.chat.id        

        new_vocabs = {}
        arr_vocabs = vocabulary.split(',')
        
        # Split the vocabulary input into individual entries and store them in a dictionary
        for vocab in arr_vocabs:
            temp_arr = vocab.split(':')
            if len(temp_arr) == 2:
                new_vocabs.update({f'{temp_arr[0].lower()}': f'{temp_arr[1].lower()}'})
            else:
                # Handle the case when the vocabulary input format is incorrect
                self.bot.send_message(chat_id, "Invalid vocabulary input format. Please use the correct format.")
                self.bot.send_message(chat_id, "Please choose an option: ", reply_markup=keyboard_handler())
                return
            
        # Check if there are existing vocabulary entries
        if vocabs_ref:     
            curr_vocabs = vocabs_ref.copy()
            curr_vocabs.update(new_vocabs)
            new_vocabs = curr_vocabs
            
        curr_user.update({'vocabs': new_vocabs})
        self.bot.send_message(chat_id, f"Vocabulary added successfully!")
        self.bot.send_message(chat_id, "Please choose an option: ", reply_markup=keyboard_handler())
