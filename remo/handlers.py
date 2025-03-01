from telebot import TeleBot
from telebot.types import Message, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from .functions import validate_ip_address
import psutil
import paramiko

allowed_users = []

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
        KeyboardButton("Открыть", web_app=WebAppInfo(config["webapp_url"])),
        KeyboardButton("Мониторинг ресурсов")
    )
    
    @bot.message_handler(commands=["start"])
    def welcome(msg: Message):
        bot.send_message(msg.chat.id, 'Привет!', reply_markup=welcome_kb)
    
    @bot.message_handler(func=lambda msg: msg.text == "⚙ Выполнить команды на сервере")
    def auth(msg: Message):
        if msg.chat.id in config['admins']:
            bot.send_message(msg.chat.id, "У вас есть доступ.", reply_markup=commands_kb)
            allowed_users.append(msg.chat.id)
        else:
            bot.send_message(msg.chat.id, "У вас нет доступа.")
    
    @bot.message_handler(func=lambda msg: msg.text == "Мониторинг ресурсов" and msg.chat.id in allowed_users)
    def resource_monitor(msg: Message):
        cpu = psutil.cpu_percent(interval=1)
        mem, total_mem = psutil.virtual_memory().percent, psutil.virtual_memory().total
        parts = psutil.disk_partitions()
        disks = {}
        for part in parts:
            disks[part.device] = f"Использовано: {round(psutil.disk_usage(part.mountpoint).used / 1024 / 1024 / 1024, 2)} GB ({psutil.disk_usage(part.mountpoint).percent}%)"
        disks = "; ".join([f"{disk}. {disk_info}\n" for disk, disk_info in disks.items()])
        result = f'''
🎛 Процессор - {cpu}%.
💾 Оперативная память - Использовано: {mem}%; Всего: {round(total_mem / 1024 / 1024 / 1024, 2)} GB.
💽 Диски - {disks}
        '''
        bot.send_message(msg.chat.id, result)
    
    @bot.message_handler(func=lambda msg: msg.text == "🔑 Подключиться по SSH")
    def ssh_get_info(msg: Message):
        bot.send_message(msg.chat.id, "Отправь мне IP-адрес для подключения.")
        bot.register_next_step_handler(msg, get_ip_address)
        
    def get_ip_address(msg: Message):
        address = msg.text
        if not validate_ip_address(address):
            bot.send_message(msg.chat.id, "Неправильно введённый IP-адрес. Попробуйте написать ещё раз.")
            bot.register_next_step_handler(msg, get_ip_address)
        else:
            bot.send_message(msg.chat.id, "Отлично! Теперь напиши мне свой никнейм.")
            bot.register_next_step_handler(msg, get_username, address)

    def get_username(msg: Message, address: str):
        bot.send_message(msg.chat.id, "Отлично! Теперь напиши мне свой пароль! Только на ушко!!")
        bot.register_next_step_handler(msg, get_password, address, msg.text)
        
    def get_password(msg: Message, address: str, username: str):
        bot.send_message(msg.chat.id, "Хорошо! Сейчас попробую подключиться...")
        
        