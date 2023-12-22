import io
import telebot
from utils import get_pdf_text
from gpt import GPT
from storage import VectorStorage
from keys import *


bot = telebot.TeleBot(BOT_API_KEY)
chat = GPT(OPENAI_API_KEY)
storage = VectorStorage(OPENAI_API_KEY)


@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    bot.reply_to(message, "Hi there! I'm Ragoût. For more information about me, please type /help.")

help_message = """Here some things you can do:
- Just send me the PDF file you want to ask about. I will extract the text from it and use it to answer your questions.
- You can also ask me questions just by typing them. I will try to answer them as best as I can.
    
/reset - erase chat history and start the bot over again.

"""

@bot.message_handler(commands=['help'])
def send_help_message(message):
    bot.reply_to(message, help_message)

@bot.message_handler(commands=['send'])
def send_document(message):
    bot.reply_to(message, "Send me a PDF file in the next message.")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    tmp = bot.reply_to(message, "I am working on it...") # temporary message to let the user know we are working on it
    file = bot.download_file(file_info.file_path)
    try:
        raw_text = get_pdf_text(io.BytesIO(initial_bytes=file))
    except:
        bot.reply_to(message, "I am afraid I cannot read this file. Please ensure it is a PDF file.")
        return
    storage.new_storage(message.from_user.username, raw_text)
    bot.delete_message(tmp.chat.id, tmp.message_id) # delete temporary message
    bot.reply_to(message, "I got the file! Now, what do you want to know?")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "Lovely picture! But I am afraid it is not a PDF file. Please send me a PDF file.")

@bot.message_handler(commands=['reset'])
def reset_func(message):
    chat.reset(message.from_user.username)
    storage.reset(message.from_user.username)
    bot.reply_to(message, "Your message history is resetted. Awaiting new file... or just type what you want to know.")

@bot.message_handler(func=lambda message: True)
def handle_query(message):
    if message.from_user.username in storage.vectors:
        docs = storage.retrieve(message.from_user.username, message.text, top_k=3)
        chat.new_rag(message.from_user.username, docs)
    res = chat.ask(message.from_user.username, message.text)
    bot.reply_to(message, res.content)


if __name__ == '__main__':
    bot.polling(non_stop=True)