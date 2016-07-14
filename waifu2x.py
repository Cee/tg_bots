from __future__ import print_function
import telebot
import argparse
import requests
import time

WAIFU_URL = 'http://waifu2x.udp.jp/api'

bot = telebot.TeleBot("TOKEN_HERE")
strip = lambda a:a.lstrip(a.split()[0]).lstrip().rstrip()

def post_image(filename):
	data = dict(url=filename, scale=2, noise=3)
	res = requests.post(WAIFU_URL, data=data)
	return res.content

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "OAO")

@bot.message_handler(commands=['waifu2x'])
def waifu(message):
	filename = strip(message.text)

	file_save_name = str(int(time.time())) + '_waifu2x.png'

	try:
		res = post_image(filename=filename)
	except requests.HTTPError:
		bot.reply_to(message, 'Something wrong with the Internet, please try again later.')
	else:
		with open(file_save_name, 'wb') as hand:
			hand.write(res)
	photo = open(file_save_name, 'rb')
	bot.send_document(message.chat.id, photo)

bot.polling()