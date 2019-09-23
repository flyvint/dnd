#!/usr/bin/python3

# import requests
# import lxml.html
# import re
import datetime
import configparser
import locale
import time
import traceback
import sys

import edutatardataprovider
import telegrambot
import marksstorage

botKeybTokenToday = "сегодня"
botKeybTokenPrevDay = "-1"
botKeybTokenNextDay = "+1"
botKeybTokenWeek = "неделя"


def log(*args):
    print("main: " + " ".join(map(str, args)))
    sys.stdout.flush()


def parseConfig():
    conf = configparser.ConfigParser()
    conf.read("dnd.conf")

    global user
    global passwd
    user = conf["EduTatarRuAuth"]["user"]
    passwd = conf["EduTatarRuAuth"]["password"]

    global token
    token = conf["Telegram"]["token"]

    global timeout
    timeout = conf["Telegram"]["timeout"]


def sendMarksForDay(inMsg, date):
    log("date:", date)

    mrmap = dprov.getMarksForDay(date)
    log("marks map:", mrmap)
    datestr = date.strftime("*%A* (%d %b)")
    if len(mrmap) > 0:
        answerText = "Оценки за " + datestr + "\n"
        for subj in mrmap.keys():
            t = "*" + subj + "*" + "\n"
            for mr in mrmap[subj]:
                log(mr)
                t += "%s (%s)\n" % (mr)
            answerText += t
    else:
        answerText = datestr + "\nоценок нет"

    log("answerText:", answerText)

    tbot.sendMessage(inMsg, answerText)


def main():
    # for datetime.strftime
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

    parseConfig()

    global stor
    stor = marksstorage.MarksStorage()
    stor.openDbFile("marks.sqlite", "marks.sql")

    global tbot
    tbot = telegrambot.TelegramBot()
    tbot.setToken(token)
    tbot.setKeyboardTokens(today=botKeybTokenToday,
                           prevday=botKeybTokenPrevDay,
                           nextday=botKeybTokenNextDay,
                           week=botKeybTokenWeek)

    global dprov
    dprov = edutatardataprovider.EduTatarDataProvider()
    dprov.setAuth(user, passwd)

    date = datetime.datetime.today()
    while True:
        try:
            msg = tbot.getMessage(timeout)
            log(msg)
            if msg is None:
                time.sleep(1)
                continue

            if msg.text == botKeybTokenToday:
                date = datetime.datetime.today()
                sendMarksForDay(msg, date)

            elif msg.text == botKeybTokenPrevDay:
                date = date - datetime.timedelta(days=1)
                sendMarksForDay(msg, date)

            elif msg.text == botKeybTokenNextDay:
                date = date + datetime.timedelta(days=1)
                sendMarksForDay(msg, date)

            elif msg.text == botKeybTokenWeek:
                log("show week info")

            else:
                log("unknown command:", msg.text)

        except KeyboardInterrupt:
            exit(0)
        except:
            log("!!!! exception !!!!")
            log("vvvvvvvvvvvvvvvvvvv")
            traceback.print_exc()
            log("^^^^^^^^^^^^^^^^^^^")
            log("")

        time.sleep(1)


if __name__ == "__main__":
    log("started")
    main()
