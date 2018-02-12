import requests
import json

class TelegramMessage:
	def __init__(self, chatId, text, username, updateId):
		self.chatId= chatId
		self.text= text
		self.username= username
		self.updateId= updateId

	def __str__(self):
		return "TelegramMessage(chatId=%s, text=%s, username=%s, updateId=%s)" \
		 	% (self.chatId, self.text, self.username, self.updateId)

class TelegramBot:
	def __init__( self ):
		self.net= requests.session()
		self.lastUpdateId= 0

	def checkToken( self, token ):
		respjson= self.net.get( "https://api.telegram.org/bot%s/getMe" % token ).json()
		print( "getMe response:", respjson )
		if respjson["ok"] != True:
			raise Exception( "invalid token[%s]" % token )

	def setToken( self, token ):
		self.token= token
		self.url= "https://api.telegram.org/bot%s" % token
		self.checkToken( token )

	def getMessage( self, timeout ):
		url= self.url + "/getUpdates"
		p = { 'timeout': timeout, 'offset': self.lastUpdateId + 1 }
		respjson= self.net.get( url, params= p ).json()
		print( "getUpdates response:", respjson )
		if respjson["ok"] != True:
			return None

		resultjson= respjson['result']
		if len(resultjson) > 0:
			firstresultjson= resultjson[0]

			if "message" in firstresultjson:
				print("message")
				updateId= firstresultjson['update_id']
				chatId=   firstresultjson['message']['chat']['id']
				text=     firstresultjson['message']['text']
				username= firstresultjson['message']['from']['username']
				return TelegramMessage( chatId, text, username, updateId )

			elif "callback_query" in firstresultjson:
				print("callback_query")
				updateId= firstresultjson['update_id']
				chatId=   firstresultjson['callback_query']['message']['chat']['id']
				text=     firstresultjson['callback_query']['data']
				username= firstresultjson['callback_query']['message']['from']['username']
				return TelegramMessage( chatId, text, username, updateId )

		return None

	def sendMessage( self, inMsg, answerText ):
		inlineKeyb = json.dumps( { 'inline_keyboard': [ \
			[ \
				{ 'text': 'Сегодня', 'callback_data': 'today' }, \
				{ 'text': '-1', 'callback_data': 'prevday' }, \
				{ 'text': 'Неделя', 'callback_data': 'week' }, \
			] ] } )
		params = { 'chat_id': inMsg.chatId, 'text': answerText, 'reply_markup': inlineKeyb }

		response = self.net.post( self.url + '/sendMessage', data=params)
		print( "send response:", response )
		self.lastUpdateId= inMsg.updateId
		return response
