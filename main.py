import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('6492336348:AAFqJMdDgMk5ZgvJyHl2LOi5ZgwbU7s_N1c')
c = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, '<b>Salemetsiz be?! Sommany engiziniz.</b>', parse_mode='html')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount=int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, '<b>Qate! Sandy engiziniz.</b>', parse_mode='html')
        bot.register_next_step_handler(message, summa)
        return

    if amount>0:
        markup=types.InlineKeyboardMarkup(row_width=2)
        btn1=types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2=types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3=types.InlineKeyboardButton('GBP/EUR', callback_data='gbp/eur')
        btn4 = types.InlineKeyboardButton('Basqa', callback_data='else')
        markup.add(btn1,btn2,btn3,btn4)
        bot.send_message(message.chat.id, 'Valyutany tandanyz:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, '<b>Qate! San 0-den jogary bolu kerek. Qaitadan engiziniz.</b>', parse_mode='html')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call:True)
def callback_data(call):
    if call.data!='else':
        values=call.data.upper().split('/')
        result=c.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Result is {round(result,2)}. Again please.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Eki valuytany slash arqyly jazynyz.')
        bot.register_next_step_handler(call.message, owncurrency)

def owncurrency(message):
    try:
        values=message.text.upper.split('/')
        result=c.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Result is {round(result, 2)}. Again please.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f'Durystap jazynyz.')
        bot.register_next_step_handler(message, owncurrency)


bot.polling(none_stop=True)

