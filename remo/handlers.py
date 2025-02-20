from telebot import TeleBot
from telebot.types import Message, KeyboardButton, ReplyKeyboardMarkup

welcome_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
welcome_kb.add(
    KeyboardButton('⚙ Выполнить команды на сервере'),
    KeyboardButton('🔑 Подключиться по SSH')
)

def connect_handlers(bot: TeleBot):
    '''
    Подключение хэндлеров.
    '''
    @bot.message_handler(commands=["start"])
    def welcome(msg: Message):
        bot.send_message(msg.chat.id, 'Привет!', reply_markup=welcome_kb)