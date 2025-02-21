import telebot as tb
from .handlers import connect_handlers
from .functions import load_config
from .server import run_server
import threading

CONFIG_PATH = "config.json"

def run_bot():
    '''
    Функция запуска бота.
    '''
    
    threading.Thread(target=run_server, daemon=True).start()
    
    config = load_config(CONFIG_PATH)
    bot = tb.TeleBot(config['TOKEN'])
    connect_handlers(bot, config)
    bot.infinity_polling()
    