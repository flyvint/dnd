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

	def check_for_logged_out( self, doc ):
		loginnode= doc.xpath(".//div[@class='login']")
		print("loginnode:", loginnode)
		if len(loginnode) > 0:
			return True
		return False

	def get_url( self, url, is_check_logout= True ):
		self.hdr["Referer"]=  "https://edu.tatar.ru"
		r= self.s.get( self.url_0 + url, headers= self.hdr, verify=True )
		doc= lxml.html.document_fromstring( r.text )

		if is_check_logout == True:
			if self.check_for_logged_out( doc ):
				print( "edu.tatar.ru session expired -> login" )
				self.login( self.user, self.passwd )
				r= self.s.get( self.url_0 + url, headers= self.hdr, verify=True )
				doc= lxml.html.document_fromstring( r.text )

		return doc

	def login(self, user, passwd):
		self.user= user
		self.passwd= passwd

		self.s = requests.session()
		self.get_url( "/logon", is_check_logout=False )
		
		self.hdr["Referer"]=  "https://edu.tatar.ru/logon"
		logindata= { "main_login":user, "main_password":passwd }
		r = self.s.post( self.url_0 + "/logon",
					data=logindata,
					headers= self.hdr,
					allow_redirects=True, verify=True )

		if "Неверный логин" in r.text:
		    raise Exception("Login failed")
		    
		if "Личный кабинет" not in r.text:
		    raise Exception("something wrong")

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
						print("mrlist:", mrlist)
					
				marksmap[subj]= marksmap.get(subj,[]) + mrlist
		return marksmap
