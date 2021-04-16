# t.me/ExchangeRatesFactoryBot
import telebot
from config import valuta, TOKEN
from extensions import APIException, ValutaConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите через пробел <имя валюты>, <валюта в которую перевести>, <количество>\n' \
           'Что бы увидеть список всех доступных валют, введите /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in valuta.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        valu = message.text.split(' ')

        if len(valu) > 3:
            raise APIException('Введено больше трех параметров.')
        elif len(valu) < 3:
            raise APIException('Введено меньше трех параметров.')
        quote, base, amount = valu
        price = ValutaConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. {e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {price}'
        bot.send_message(message.chat.id, text)

bot.polling()
