from firebase_admin import db
from functions import keyboard_handler

class EditVocabularyHandler:
    def __init__(self, bot, users_ref):
        self.bot = bot
        self.callback_handler = None
        self.user_input_handler = None
        self.users_ref = users_ref

    def register(self, call):
        chat_id = call.message.chat.id

        if call.data == 'edit':
            self.bot.send_message(chat_id, "Please enter a vocabulary word to edit:", parse_mode="HTML")

            if self.callback_handler:
                self.bot.remove_handler(self.callback_handler)
            if self.user_input_handler:
                self.bot.remove_handler(self.user_input_handler)

            self.callback_handler = self.bot.register_next_step_handler(
                call.message, self.handle_user_input(call.message, call.from_user.id)
            )

    def handle_user_input(self, message, user_id):
        def inner_handler(message):
            user_input = message.text
            self.handle_edit_handler(message, user_id, user_input)

        return inner_handler

    def handle_vocab_value(self, message, user_input):
        self.bot.send_message(message.chat.id, f'Please enter the new value for the word "{user_input}":')
        new_value = message.text
        return new_value

    def handle_edit_handler(self, message, user_id, user_input):
        try:
            curr_user = self.users_ref.child(str(user_id))
        except AttributeError:
            self.bot.send_message(message.chat.id, "Error: Invalid user reference.")
            return

        user_input = user_input.lower()
        vocabs_ref = db.reference(f'/users/{user_id}/vocabs').get()
        chat_id = message.chat.id

        if vocabs_ref is not None and isinstance(vocabs_ref, dict):
            # Check if the vocabulary word exists
            if user_input in vocabs_ref:
                self.bot.send_message(chat_id, f'Please enter the new value for the word "{user_input}":')
                # Register the next step handler to capture the new value
                self.bot.register_next_step_handler(
                    message, self.handle_new_value(message, user_id, user_input)
                )
            else:
                self.bot.send_message(chat_id, f'The word "{user_input}" does not exist in the vocabulary.')
                self.bot.send_message(chat_id, "Please choose an option:", reply_markup=keyboard_handler())
        else:
            self.bot.send_message(chat_id, "Vocabulary dictionary is empty.")
            self.bot.send_message(chat_id, "Please choose an option:", reply_markup=keyboard_handler())

    def handle_new_value(self, message, user_id, user_input):
        '''
        Handles the update of a vocabulary value for a user.

        Parameters:
            message (Telegram Message object): The Telegram message object containing the user's input.
            user_id (str): The unique identifier for the user.
            user_input (str): The vocabulary word for which the value needs to be updated.

        Returns:
            func: An inner handler function responsible for updating the value and sending response messages.
        '''
        def inner_handler(message):
            new_value = message.text

            try:
                # Get the reference to the user's vocabulary entries in the database
                vocabs_ref = db.reference(f'/users/{user_id}/vocabs')
                vocabs_ref.update({user_input: new_value})

                # Send a success message to the user
                self.bot.send_message(message.chat.id, f'The value of the word "{user_input}" has been updated to "{new_value}".')
                self.bot.send_message(message.chat.id, "Please choose an option:", reply_markup=keyboard_handler())
            except Exception as e:
                self.bot.send_message(message.chat.id, f"Error occurred while updating vocabulary: {str(e)}")

        return inner_handler
