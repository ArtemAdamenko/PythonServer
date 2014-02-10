# -*- coding: utf-8 -*-
import threading
import time
import datetime
from core.gGeneral import printLog
from defines.gDefines import *
import psycopg2
class AThreadDataBase(threading.Thread):
    
    #...........................................................................
    def __init__(self):
        self.pBase = {  'host'  : '192.168.137.142'
                      , 'path'  : ''
                      , 'dbname': 'CDS'
                      , 'port'  : '5432'
                      , 'login' :'postgres'
                      , 'password':'zaUgD5Lt'
                      , 'alias' : ''  }
        self.commitTimeout      = 500 # milisecond
        self.commitRecordCount  = 1
        self.dbConnect          = None
        self.LastCommitDataTime = None
        self.countRequests      = 0
        self.countExecQueryOK   = 0
        self.countExecQueryErrors=0
        self.lastTimeCommit     = None
        self.CommitTimeOut      = 500 # milisecond
        
        self.buffer             = {}
        self.Worked             = False
        self.CountConnections   = 0
        
        self.QueryStartTime     = None
        self.QueryEndTime       = None        
        self.QueryRuntime       = None
        threading.Thread.__init__(self)
    #...........................................................................    
    def run(self):
        self.LogFileName        = 'DataBase%s%s%sWork.log' % (SLASH,self.getName(),SLASH)
        self.SnapshotFileName        = 'DataBase%s%s%sSnapshot.sql' % (SLASH,self.getName(),SLASH)
        self.LogFileNameErrors  = 'DataBase%s%s%sErrors.log' % (SLASH,self.getName(),SLASH)
        if self.DataBaseConnect():
            self.Work()
            self.DataBaseDisconnect()
    #...........................................................................    
    def DataBaseConnect(self):      
        
        if self.dbConnect == None :
            try:
                printLog (self.getName() +':Подключение к базе данных "%s" ...' % ( str(self.pBase['alias'])),False, self.LogFileName, False)

                self.dbConnect = psycopg2.connect("dbname='CDS' user='postgres' host='192.168.137.142' password='zaUgD5Lt' port='5432'")

                self.CountConnections += 1
                printLog (self.getName() +':Подключение к базе данных "%s" ВЫПОЛНЕНО.' % ( str(self.pBase['alias'])),False, self.LogFileName, False)
                return True
            except Exception as e:
                printLog (self.getName() +':Ошибка подключения к базе данных %s: %s' % ( str(self.pBase), str(e)),True, self.LogFileName, False)
                printLog (self.getName() +':Ошибка подключения к базе данных %s: %s' % ( str(self.pBase), str(e)),True, self.LogFileNameErrors, False)
                return False        
        else:
            printLog (self.getName() +':Подключение к базе данных "%s" уже выполнено.' % ( str(self.pBase['alias'])),False, self.LogFileName, False)
            return True
            
    #...........................................................................    
    def DataBaseDisconnect(self):
        if self.dbConnect:
            try:
                printLog (self.getName() +':Закрытие подключения к базе данных "%s"...' % str(self.pBase['alias']),False, self.LogFileName, False)
                self.dbConnect.close();
                printLog (self.getName() +':Подключение к базе данных "%s" закрыто.' % str(self.pBase['alias']),False, self.LogFileName, False)
                self.dbConnect = None
                return True
            except Exception as e:
                printLog (self.getName() +':Ошибка закрытия подключения к базе данных %s' % str(e),True, self.LogFileName, False)
                printLog (self.getName() +':Ошибка закрытия подключения к базе данных %s' % str(e),True, self.LogFileNameErrors, False)
                return True
        else:
            return True
    #...........................................................................
    def ExecQuery(self, _sql, _fetchall = False, ResultData = None):
        try:
            
            self.QueryRuntime = None
            self.QueryStartTime = datetime.datetime.now()
            cursor = None
            result = False
            self.countRequests +=1
            if not self.DataBaseConnect():
                raise Exception ("Нет подключения к базе данных.")
            
            cursor = self.dbConnect.cursor()
            if cursor:
                #printLog('Выполнение sql-запроса: %s' % str(_sql), True, self.LogFileName, False)
                cursor.execute(_sql)

                    
                if _fetchall:
                    result = cursor.fetchall()
                    for rows in result:
                        if ResultData!=None:
                            ResultData.append(rows);
                            

                self.dbConnect.commit()
                self.LastCommitDataTime = time.time()
                self.countExecQueryOK+=1
                result = True
            cursor=None
            self.QueryEndTime = datetime.datetime.now()
            self.QueryRuntime = self.QueryEndTime - self.QueryStartTime
            
        except Exception as e :
            self.countExecQueryErrors+=1
            result = False
            
            printLog('-', True, self.LogFileName)
            printLog(self.getName() +':Ошибка выполнения sql-запроса :  %s' % str(e), True, self.LogFileName)
            printLog(self.getName() +':Текст запроса:%s' % str(_sql), True, self.LogFileName)
            
            printLog('-', True, self.LogFileNameErrors)
            printLog(self.getName() +':Ошибка выполнения sql-запроса :  %s' % str(e), True, self.LogFileNameErrors)
            printLog(self.getName() +':Текст запроса:%s' % str(_sql), True, self.LogFileNameErrors)
            
            
            
        return result    
            
    #...........................................................................

    def Work(self):
        pass
#------------------------------------------------------------------------------#
