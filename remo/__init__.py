import telebot as tb
from .handlers import connect_handlers
from .functions import load_config

CONFIG_PATH = "config.json"

def run_bot():
    '''
    Функция запуска бота.
    '''
    config = load_config(CONFIG_PATH)
    
    bot = tb.TeleBot(config['TOKEN'])
    connect_handlers(bot, config)
    
    print('Бот запущен.')
    bot.infinity_polling()
    