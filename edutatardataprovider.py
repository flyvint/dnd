import requests
import lxml.html
import re
import datetime

class Marks:

	def __init__(self):
		self.marks= ()
		
	# def 


class EduTatarDataProvider:
	
	def __init__(self):
		self.hdr= {}
		self.hdr["User-Agent"]= "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
		self.url_0= "https://edu.tatar.ru"
		pass

	def get_url( self, url ):
		self.hdr["Referer"]=  "https://edu.tatar.ru"
		r= self.s.get( self.url_0 + url, headers= self.hdr, verify=True )
		return lxml.html.document_fromstring( r.text )

	def login(self, user, passwd):
		self.user= user
		self.passwd= passwd

		self.s = requests.session()
		self.get_url( "/logon" )
		
		self.hdr["Referer"]=  "https://edu.tatar.ru/logon"
		logindata= { "main_login":user, "main_password":passwd }
		r = self.s.post( self.url_0 + "/logon",
					data=logindata,
					headers= self.hdr,
					allow_redirects=True, verify=True )

		if "Неверный логин" in r.text:
		    print( "login failed" )
		    return False
		    
		if "Личный кабинет" not in r.text:
		    print("something wrong")
		    return False

		print("login ok")
		return True

	def get_marks_for_day(self, date):
		ts= int( date.timestamp() )
		# print("ts:", ts)
		doc= self.get_url( "/user/diary/day?for=" + str(ts) )

		dairyRowArr= doc.xpath(".//div[@class='d-table']//tbody/tr")
		print( "dairyRowArr:", dairyRowArr)

		marksmap= {}
		for dr in dairyRowArr:
			marks= dr.xpath( ".//table[@class='marks']//td" )
			if len(marks) > 0:
				subjxp= dr.xpath( "./td[2]/text()")
				if len(subjxp) > 0:
					subj= subjxp[0]

				print("subj:", subj)
				print("marks:", marks)
				mrlist= []
				for m in marks:
					mreasons= m.xpath("./@title")
					print("  reasons:", mreasons)
					mmarks= m.xpath(".//div/text()")
					print("  marks:", mmarks)
					for m,r in zip( mmarks, mreasons ):
						mrlist.append( (m,r) )
					
				if subj in marksmap:
					marksmap[subj].append( mrlist )
				else:
					marksmap[subj]= mrlist
		print( "marksmap:", marksmap )
		return marksmap


