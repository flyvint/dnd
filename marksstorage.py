import sys
# import os
import sqlite3


def log(*args):
    print("stor: " + " ".join(map(str, args)))
    sys.stdout.flush()


class MarksStorage:
    def __init__(self):
        self.dbversion = 1

    def __del__(self):
        self.db.close()

    def initDB(self, dbfile, dbinitfile):
        log("create db")
        with open(dbinitfile, 'r') as myfile:
            sqlscript = myfile.read()

        dbcur = self.db.cursor()
        dbcur.executescript(sqlscript)
        self.db.commit()

    def isDbValid(self):
        dbcur = self.db.cursor()
        try:
            dbcur.execute("select value from config where name='version'")
            dbvers = dbcur.fetchone()
            log("version:", dbvers)
            if dbvers is None:
                return False

            dbversint = int(dbvers[0])
            if dbversint != self.dbversion:
                log("version missmatch {} != {}".format(
                    dbversint, self.dbversion))
                return False

        except sqlite3.OperationalError:
            return False
        return True

    def openDbFile(self, dbfile, dbinitfile):
        self.db = sqlite3.connect(dbfile)

        if not self.isDbValid():
            self.initDB(dbfile, dbinitfile)
