import configparser

class Config:

    eduUser= None
    eduPasswd= None
    tlgToken= None
    tlgTimeout= None
    tlgHttpProxy= None
    tlgHttpsProxy= None

    def read(self):
        conf = configparser.ConfigParser()
        conf.read("dnd.conf")

        self.eduUser = conf["EduTatarRuAuth"]["user"]
        self.eduPasswd = conf["EduTatarRuAuth"]["password"]
        self.tlgToken = conf["Telegram"]["token"]
        self.tlgTimeout = conf["Telegram"]["timeout"]
        self.tlgHttpProxy = conf["Telegram"]["http_proxy"]
        self.tlgHttpsProxy = conf["Telegram"]["https_proxy"]
