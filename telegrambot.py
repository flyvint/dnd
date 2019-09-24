import requests
import json
import time
import sys


def log(*args):
    print("bot: " + " ".join(map(str, args)))
    sys.stdout.flush()


class TelegramMessage:
    def __init__(self, chatId, text, username, updateId):
        self.chatId = chatId
        self.text = text
        self.username = username
        self.updateId = updateId

    def __str__(self):
        return "TelegramMessage(chatId=%s, text=%s, username=%s, updateId=%s)"\
            % (self.chatId, self.text, self.username, self.updateId)


class TelegramBot:
    proxies= None

    def __init__(self):
        self.net = requests.session()
        self.lastUpdateId = 0

    def setProxy(self, httpProxy, httpsProxy):
        self.proxies= { "http": httpProxy, "https": httpsProxy }

    def checkToken(self, token):
        respjson = self.net.get(
            "https://api.telegram.org/bot%s/getMe" % token, proxies= self.proxies).json()
        log("getMe response:", respjson)
        if respjson["ok"] is not True:
            raise Exception("invalid token[%s]" % token)

    def setToken(self, token):
        self.token = token
        self.url = "https://api.telegram.org/bot%s" % token
        self.checkToken(token)

    def setKeyboardTokens(self, today, prevday, nextday, week):
        self.keybTokenToday = today
        self.keybTokenPrevDay = prevday
        self.keybTokenNextDay = nextday
        self.keybTokenWeek = week

    def getUrlJson(self, url, timeout=60):
        p = {'timeout': timeout, 'offset': self.lastUpdateId + 1}
        while True:
            try:
                return self.net.get(url, params=p, proxies= self.proxies).json()
            except requests.exceptions.ConnectionError as e:
                time.sleep(5)
            except json.decoder.JSONDecodeError as e:
                time.sleep(5)
            except Exception as e:
                raise e

    def getMessage(self, timeout):
        url = self.url + "/getUpdates"
        respjson = self.getUrlJson(url, timeout)
        log("getUpdates response:", respjson)
        if respjson["ok"] is not True:
            return None

        resultjson = respjson['result']
        if len(resultjson) <= 0:
            return None
        firstresultjson = resultjson[0]

        if "message" in firstresultjson:
            log("message")
            updateId = firstresultjson['update_id']
            chatId = firstresultjson['message']['chat']['id']
            text = firstresultjson['message']['text']
            username = ""
            if "username" in firstresultjson['message']['from']:
                username = firstresultjson['message']['from']['username']
            elif "first_name" in firstresultjson['message']['from']:
                username = firstresultjson['message']['from']['first_name']
            return TelegramMessage(chatId, text, username, updateId)

        elif "callback_query" in firstresultjson:
            log("callback_query")
            updateId = firstresultjson['update_id']
            chatId = firstresultjson['callback_query']['message']['chat']['id']
            text = firstresultjson['callback_query']['data']
            callbackquery = firstresultjson['callback_query']
            if 'message' in callbackquery:
                username = callbackquery['message']['from']['username']
            elif 'from' in callbackquery:
                username = callbackquery['from']['first_name']
            else:
                username = ""
            return TelegramMessage(chatId, text, username, updateId)

    def sendMessage(self, inMsg, answerText):
        # inlineKeyb = json.dumps( { 'inline_keyboard': [ \
        #   [ \
        #       { 'text': 'Сегодня', 'callback_data': 'today' }, \
        #       { 'text': '-1', 'callback_data': 'prevday' }, \
        #       { 'text': 'Неделя', 'callback_data': 'week' }, \
        #   ] ] } )
        inlineKeyb = json.dumps(
            {
                'keyboard': [
                    [
                        {'text': self.keybTokenPrevDay},
                        {'text': self.keybTokenToday},
                        {'text': self.keybTokenNextDay},
                        {'text': self.keybTokenWeek},
                    ],
                ],
                'resize_keyboard': True
            })
        params = {'chat_id': inMsg.chatId,
                  'text': answerText,
                  'parse_mode': 'Markdown',
                  'reply_markup': inlineKeyb}

        log("send:", params)
        response = self.net.post(self.url + '/sendMessage', data=params, proxies= self.proxies)
        log("response:", response.text)

        self.lastUpdateId = inMsg.updateId
        return response
