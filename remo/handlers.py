from telebot import TeleBot
from telebot.types import Message, KeyboardButton, ReplyKeyboardMarkup
import subprocess as sp

welcome_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
welcome_kb.add(
    KeyboardButton('⚙ Выполнить команды на сервере'),
    KeyboardButton('🔑 Подключиться по SSH')
)

def connect_handlers(bot: TeleBot, config: dict):
    '''
    Подключение хэндлеров.
    '''
    @bot.message_handler(commands=["start"])
    def welcome(msg: Message):
        bot.send_message(msg.chat.id, 'Привет!', reply_markup=welcome_kb)
    
    
    # Локальное выполнение команд
    
    @bot.message_handler(func=lambda msg: msg.text == "⚙ Выполнить команды на сервере")
    def proceed_commands_localy(msg: Message):
        bot.send_message(msg.chat.id, 'Отправь мне команду, чтобы я выполнил её на локальном сервере.')
        bot.register_next_step_handler(msg, proceed_command)
        
    def proceed_command(msg: Message):
        if msg.text.strip() in config['dangerous']:
            bot.send_message(msg.chat.id, 'Ай-ай-ай!! Опасная команда!')
            return
        
        result = sp.run(msg.text.split(), capture_output=True, text=True).stdout.strip()
        bot.send_message(msg.chat.id, f'Команда выполнена. Консольный вывод:\n\n{result}')