import requests
from functions import keyboard_handler, handle_add_vocab

class ChatgptAPI:
    API_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
    API_KEY = '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'
    MODEL_ID = 'gpt-3.5-turbo'

    def __init__(self, bot):
        self.bot = bot
        self.callback_handler = None
        self.user_input_handler = None

    def register(self, call):
        # Register the callback for chatgpt
        chat_id = call.message.chat.id

        if call.data == 'chatgpt':
            self.bot.send_message(chat_id, "Please enter vocabulary that you want to translate:", parse_mode="HTML")

            if self.callback_handler:
                self.bot.remove_handler(self.callback_handler)
            if self.user_input_handler:
                self.bot.remove_handler(self.user_input_handler)

            self.bot.register_next_step_handler(call.message, self.handle_user_input)

    def handle_user_input(self, message):
        # Handle the user input after the prompt
        prompt = message.text
        self.handle_chatgpt(message, prompt)

    def handle_user_choice(self, message, result, user_id):
        # Handle the user's choice to add vocabs or not
        user_input = message.text.lower()
        if user_input == 'yes':
            handle_add_vocab(user_id, result)
            self.bot.send_message(message.chat.id, 'Vocab added successfully...')
            self.bot.send_message(message.chat.id, 'Please choose an option...', reply_markup=keyboard_handler())
        elif user_input == 'no':
            self.bot.send_message(message.chat.id, 'Please choose an option...', reply_markup=keyboard_handler())
        else:
            self.bot.send_message(message.chat.id, 'Invalid option...', reply_markup=keyboard_handler())

    def handle_chatgpt(self, message, user_input):
        # Handle the chatgpt request
        chat_id = message.chat.id

        headers = {
            'Authorization': f'Bearer {self.API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': self.MODEL_ID,
            'messages': [
                {
                    'role': 'system', 'content': f'translate into Russian the words {user_input}'
                }
            ]
        }

        try:
            # Send the request to the chatgpt API
            response = requests.post(self.API_ENDPOINT, headers=headers, json=data)
            chatgpt_answer_content = response.json()['choices'][0]['message']['content']

            if len(chatgpt_answer_content.split()) > 1:
                # If multiple words are returned, handle them separately
                result = self.handle_multiple_words(chatgpt_answer_content, user_input)

                self.bot.send_message(chat_id, result)
                self.bot.send_message(chat_id, 'Do you want to add these vocabs into the database? (Yes/No)')
                self.bot.register_next_step_handler(
                    message,
                    self.handle_user_choice,
                    result,
                    message.from_user.id
                )
            else:
                # If a single word is returned, send the translation
                self.bot.send_message(chat_id, f'"{user_input}": {chatgpt_answer_content}\n')
                self.bot.send_message(chat_id, 'Please choose an option...', reply_markup=keyboard_handler())

        except requests.exceptions.RequestException:
            # Handle any errors that occur during the request
            self.bot.send_message(chat_id, 'An error has occurred. Please choose an option...', reply_markup=keyboard_handler())

    def handle_multiple_words(self, chatgpt_answer_content, user_input):
        # Handle multiple words and translations
        user_input_words = user_input.split(',')
        chatgpt_answer_words = chatgpt_answer_content.split(',')

        final_message = ''

        for word, translation in zip(user_input_words, chatgpt_answer_words):
            final_message += f'{word}: {translation}, '

        return final_message
