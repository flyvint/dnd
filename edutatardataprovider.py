import requests
import lxml.html
# import re
# import datetime
import sys


def log(*args):
    print("edu: " + " ".join(map(str, args)))
    sys.stdout.flush()


class Marks:

    def __init__(self):
        self.marks = ()


class EduTatarDataProvider:

    def __init__(self):
        self.hdr = {}
        self.hdr["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64;" \
                                 " rv:58.0) Gecko/20100101 Firefox/58.0"
        self.url_0 = "https://edu.tatar.ru"
        self.s = requests.session()
        pass

    def isLoggedOut(self, doc):
        loginnode = doc.xpath(".//div[@class = 'login-form']")
        log("loginnode:", loginnode)
        if len(loginnode) > 0:
            return True
        return False

    def getUrl(self, url, isCheckFoLogout= True):
        self.hdr["Referer"] = "https://edu.tatar.ru"
        r = self.s.get(self.url_0 + url, headers=self.hdr, verify=True)
        doc = lxml.html.document_fromstring(r.text)

        if isCheckFoLogout is True:
            if self.isLoggedOut(doc):
                log("edu.tatar.ru session expired -> login")
                self.login()
                r = self.s.get(self.url_0 + url, headers=self.hdr, verify=True)
                doc = lxml.html.document_fromstring(r.text)

        return doc

    def setAuth(self, user, passwd):
        self.user = user
        self.passwd = passwd

    def login(self):
        log("login...")
        self.getUrl("/logon", isCheckFoLogout=False)

        self.hdr["Referer"] = "https://edu.tatar.ru/logon"
        logindata = {"main_login": self.user,
                     "main_password": self.passwd}
        r = self.s.post(self.url_0 + "/logon",
                        data=logindata,
                        headers=self.hdr,
                        allow_redirects=True, verify=True)

        if "Неверный логин" in r.text:
            raise Exception("Login failed", r.text)

        if "Личный кабинет" not in r.text:
            raise Exception("something wrong:", r.text)

        log("login ok")
        return True

    def getMarksForDay(self, date):
        ts = int(date.timestamp())
        # log("ts:", ts)
        doc = self.getUrl("/user/diary/day?for=" + str(ts))

        dairyRowArr = doc.xpath(".//div[@class='d-table']//tbody/tr")
        log("dairyRowArr:", dairyRowArr)

        marksmap = {}
        for dr in dairyRowArr:
            marks = dr.xpath(".//table[@class='marks']//td")
            if len(marks) > 0:
                subjxp = dr.xpath("./td[2]/text()")
                if len(subjxp) > 0:
                    subj = subjxp[0]

                log("subj:", subj)
                log("marks:", marks)
                mrlist = []
                for m in marks:
                    mreasons = m.xpath("./@title")
                    log("  reasons:", mreasons)
                    mmarks = m.xpath(".//div/text()")
                    log("  marks:", mmarks)
                    for m, r in zip(mmarks, mreasons):
                        mrlist.append((m, r))
                        log("mrlist:", mrlist)

                marksmap[subj] = marksmap.get(subj, []) + mrlist
        return marksmap
