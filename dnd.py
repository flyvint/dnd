#!/usr/bin/python3

import requests
import lxml.html
import re

url_0 = "https://edu.tatar.ru"

user="50194001176"
passwd="vDhCHmfE"

hdr= {}
hdr["User-Agent"]= "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"

def get_url( url ):
    r= s.get( url_0 + url, headers= hdr, verify=False )
    return lxml.html.document_fromstring( r.text )


print("login")
s = requests.session()
get_url( "/logon" )

hdr["Referer"]=  "https://edu.tatar.ru/logon"
logindata= { "main_login":user, "main_password":passwd }
r = s.post( url_0 + "/logon", data=logindata, headers= hdr, allow_redirects=True, verify=False )

if "Неверный логин" in r.text:
    print( "login failed" )
    exit(1)
    
if "Личный кабинет" not in r.text:
    print("something wrong")
    exit(2)

print("login ok")

hdr["Referer"]=  "https://edu.tatar.ru"
secsfromepoch=1517259600
doc= get_url( "/user/diary/day?for=" + str(secsfromepoch) )

a= doc.xpath( ".//div[@class='d-table']//tbody/tr/td[2]/text()" )
print( "a:", a )

