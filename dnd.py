#!/usr/bin/python3

# import requests
# import lxml.html
# import re
import datetime
import locale
import time
import traceback
import sys

import edutatardataprovider
import telegrambot
import marksstorage
import config
from telegrambot import TelegramBot

botKeybTokenToday = "сегодня"
botKeybTokenPrevDay = "-1"
botKeybTokenNextDay = "+1"
botKeybTokenWeek = "неделя"

def log(*args):
    print("main: " + " ".join(map(str, args)))
    sys.stdout.flush()

class Main:
    conf= None
    dprov= None
    tbot= None
    stor= None

    def __init__(self):
        self.conf= config.Config()
        self.conf.read()

        self.dprov = edutatardataprovider.EduTatarDataProvider()
        self.dprov.setAuth(self.conf.eduUser, self.conf.eduPasswd)

        self.tbot = telegrambot.TelegramBot()
        self.tbot.setProxy(self.conf.tlgHttpProxy, self.conf.tlgHttpsProxy)
        self.tbot.setToken(self.conf.tlgToken)
        self.tbot.setKeyboardTokens(today=botKeybTokenToday,
                               prevday=botKeybTokenPrevDay,
                               nextday=botKeybTokenNextDay,
                               week=botKeybTokenWeek)

        self.stor = marksstorage.MarksStorage()
        self.stor.openDbFile("marks.sqlite", "marks.sql")

    def sendMarksForDay(self, inMsg, date):
        log("date:", date)

        mrmap = self.dprov.getMarksForDay(date)
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

        self.tbot.sendMessage(inMsg, answerText)


    def main(self):
        date = datetime.datetime.today()
        while True:
            try:
                msg = self.tbot.getMessage(self.conf.tlgTimeout)
                log(msg)
                if msg is None:
                    time.sleep(1)
                    continue

                if msg.text == "/start":
                    self.sendMarksForDay(msg, date)

                elif msg.text == botKeybTokenToday:
                    date = datetime.datetime.today()
                    self.sendMarksForDay(msg, date)

                elif msg.text == botKeybTokenPrevDay:
                    date = date - datetime.timedelta(days=1)
                    self.sendMarksForDay(msg, date)

                elif msg.text == botKeybTokenNextDay:
                    date = date + datetime.timedelta(days=1)
                    self.sendMarksForDay(msg, date)

                elif msg.text == botKeybTokenWeek:
                    log("show week info")
                    self.tbot.sendMessage(msg, "show week info")

                else:
                    log("unknown command:", msg.text)
                    self.tbot.sendMessage(msg, "упс :)")


            except KeyboardInterrupt:
                exit(0)
            except:
                log("!!!! exception !!!!")
                log("vvvvvvvvvvvvvvvvvvv")
                traceback.print_exc()
                log("^^^^^^^^^^^^^^^^^^^")
                log("")

            time.sleep(1)

    def test(self):
        date = datetime.datetime.today() - datetime.timedelta(days=1)

        mrmap = self.dprov.getMarksForDay(date)
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



if __name__ == "__main__":
    log("started")

    # for datetime.strftime
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

    m= Main()
    m.main()
    # m.test()
