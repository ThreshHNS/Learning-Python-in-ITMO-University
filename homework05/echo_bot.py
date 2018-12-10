import telebot
from telebot import apihelper

access_token = '753613571:AAHts_GaJphVexQF9vMWuWXgBHaWqtT6C5I'
apihelper.proxy = {'https': 'socks5://telegram:telegram@sr.spry.fail:1080'}

bot = telebot.TeleBot(access_token)


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)

