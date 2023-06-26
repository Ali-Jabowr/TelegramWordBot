from telebot import types
from firebase_admin import db

def keyboard_handler():
    # Create an inline keyboard with options
    markup = types.InlineKeyboardMarkup(row_width=2)
    add_button = types.InlineKeyboardButton("Add Vocabulary", callback_data='add')
    show_button = types.InlineKeyboardButton("Show Vocabularies", callback_data='show')
    delete_button = types.InlineKeyboardButton("delete Vocabularies", callback_data='delete')
    edit_button = types.InlineKeyboardButton("edit Vocabularies", callback_data='edit')
    chatgpt_button = types.InlineKeyboardButton("chatgpt", callback_data='chatgpt')
    markup.add(add_button, show_button, delete_button, edit_button, chatgpt_button)
    return markup

def handle_add_vocab(user_id, vocabulary):
    """
    Handles the addition of vocabulary entries for a user.

    Parameters:
        user_id (str): The unique identifier for the user.
        vocabulary (str): The vocabulary input provided by the user.
    """
    ref = db.reference("/")
    users_ref = ref.child('users')
    curr_user = users_ref.child(f'{user_id}')
    vocabs_ref = db.reference(f'/users/{user_id}/vocabs').get()

    new_vocabs = {}

    arr_vocabs = vocabulary.split(',')
    for vocab in arr_vocabs[:-1]:
        temp_arr = vocab.split(':')
        new_vocabs.update({f'{temp_arr[0].strip().lower()}': f'{temp_arr[1].strip().lower()}'})
        
    # Check if there are existing vocabulary entries
    if vocabs_ref:     
        # If there are existing entries, update them with the new entries
        curr_vocabs = vocabs_ref.copy()
        curr_vocabs.update(new_vocabs)
        new_vocabs = curr_vocabs
        
    # Update the user's vocabulary entries in the database
    curr_user.update({'vocabs': new_vocabs})
