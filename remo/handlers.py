from telebot import TeleBot
from telebot.types import Message, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo


def connect_handlers(bot: TeleBot, config: dict):
    '''
    Подключение хэндлеров.
    '''
    welcome_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    welcome_kb.add(
        KeyboardButton('⚙ Выполнить команды на сервере'),
        KeyboardButton('🔑 Подключиться по SSH'),
    )
    
    commands_kb = ReplyKeyboardMarkup(row_width=1)
    commands_kb.add(
        KeyboardButton("Открыть", web_app=WebAppInfo(config["webapp_url"]))
    )
    
    @bot.message_handler(commands=["start"])
    def welcome(msg: Message):
        bot.send_message(msg.chat.id, 'Привет!', reply_markup=welcome_kb)
        print(msg.chat.id)
    
    @bot.message_handler(func=lambda msg: msg.text == "⚙ Выполнить команды на сервере")
    def auth(msg: Message):
        if msg.chat.id in config['admins']:
            bot.send_message(msg.chat.id, "У вас есть доступ. Нажмите на кнопку, чтобы открыть исполнитель команд.", reply_markup=commands_kb)
        else:
            bot.send_message(msg.chat.id, "У вас нет доступа.")
    
    @bot.message_handler(func=lambda msg: msg.text == "🔑 Подключиться по SSH")
    def ssh_get_info(msg: Message):
        pass