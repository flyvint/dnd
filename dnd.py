#!/usr/bin/python3

import requests
import lxml.html
import re
import datetime
import edutatardataprovider
import configparser

conf= configparser.ConfigParser()
conf.read( "dnd.conf" )
user=  conf[ "EduTatarRuAuth" ][ "user" ]
passwd=conf[ "EduTatarRuAuth" ][ "password" ]

dprov= edutatardataprovider.EduTatarDataProvider()
if dprov.login(user, passwd) == False:
	print( "login failed" )
	exit(1)

mrmap= dprov.get_marks_for_day( datetime.datetime(2018,1,31) )



