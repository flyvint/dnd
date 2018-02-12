#!/usr/bin/python3

import requests
import lxml.html
import re
import datetime
import configparser
import locale
import time

import edutatardataprovider
import telegrambot

# for datetime.strftime
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

conf= configparser.ConfigParser()
conf.read( "dnd.conf" )
user=  conf[ "EduTatarRuAuth" ][ "user" ]
passwd=conf[ "EduTatarRuAuth" ][ "password" ]

token= conf["Telegram"]["token"]

tbot= telegrambot.TelegramBot()
tbot.setToken( token )

timeout= conf["Telegram"]["timeout"]

dprov= edutatardataprovider.EduTatarDataProvider()
if dprov.login(user, passwd) == False:
	print( "login failed" )
	exit(1)

date= datetime.datetime.today()
while True:
	msg= tbot.getMessage( timeout )
	print(msg)
	if msg == None:
		time.sleep(5)
		continue

	if msg.text == "today":
		date= datetime.datetime.today()
	elif msg.text == "prevday":
		date= date - datetime.timedelta(days=1)
	else:
		date= datetime.datetime.today()

	print("date:", date)

	mrmap= dprov.get_marks_for_day( date )
	print("marks map:", mrmap)
	if len(mrmap) > 0:
		answerText="Оценки за " + date.strftime("%A (%d %b)") + "\n"
		for subj in mrmap.keys():
			t= subj + " "
			for mr in mrmap[subj]:
				print(mr)
				t += " %s(%s)" % (mr)
			answerText += t + "\n"
	else:
		answerText= date.strftime("%A (%d %b)") + " оценок нет"

	print("answerText:", answerText)

	tbot.sendMessage( msg, answerText )

	time.sleep(5)

