import telebot
from utilities import TOKEN, keys
from exeptions import Converter, ApiExeption

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.send_message(message.chat.id, text=f'Здравствуй {message.from_user.username}!\n\nВыбери нужную команду:\n/values\n/convert')

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    text = 'Введите валюту из которой будем конвертировать:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = 'Введите валюту в которую конвертируем:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = 'Введите количество конвертируемой валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()

    try:
        new_price = Converter.get_price(base, quote, amount)
    except ApiExeption as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n {e}')
    else:
        text = f'{amount} {base} в {quote} |=>> {new_price}'
        bot.send_message(message.chat.id, text)
   

bot.polling()
