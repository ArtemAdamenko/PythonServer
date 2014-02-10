# -*- coding: utf-8 -*-
#-------------------------------------------------

import threading
import odbc
import time
import datetime

#-------------------------------------------------
class TControlOnline(threading.Thread):
    def __init__(self):
        print('Starting module control ...')
        self.dbConnect=None
        self.pBase = {  'host'  : '127.0.0.1'
                      , 'path'  : 'c:\\scat\\workbin\\db\\projects.fdb'
                      , 'port'  : 3050
                      , 'login' :'sysdba'
                      , 'password':'zaUgD5Lt'
                      , 'alias' : 'PROJECTS'}
        
        
        threading.Thread.__init__(self)

    def run(self):
        print('Module run ...')
        self.__del__()
        
    def __del__(self):
        print('Module stoped.')
        

    def ConnectDataBase(self):
        try:
            if self.dbConnect == None :
            try:
                printLog (self.getName() +':Подключение к базе данных "%s" ...' % ( str(self.pBase['alias'])),True, self.LogFileName)
                _strConnect = "Driver=Firebird/InterBase(r) driver;UID=%s;PWD=%s;DBNAME=%s;" % (self.pBase['login'],self.pBase['password'], self.pBase['host'] + ':' + self.pBase['path'])
                self.dbConnect = odbc.odbc(_strConnect)
                printLog (self.getName() +':Подключение к базе данных "%s" ВЫПОЛНЕНО.' % ( str(self.pBase['alias'])),True, self.LogFileName)
                return True
            except Exception as e:
                printLog (self.getName() +':Ошибка подключения к базе данных %s: %s' % ( str(self.pBase), str(e)),True, self.LogFileName)
                printLog (self.getName() +':Ошибка подключения к базе данных %s: %s' % ( str(self.pBase), str(e)),True, self.LogFileNameErrors)
                return False        
        else:
            return True
    
        except Exception as e:
            print ("Error DataBase connectin:%s" % e)
        

AControl = TControlOnline()
AControl.start()
