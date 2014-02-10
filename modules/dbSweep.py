# -*- coding: utf-8 -*-
import datetime
import time
from core.gDB import AThreadDataBase
from defines.gDefines import *
from core.gGeneral import printLog

class ThreadDataBaseSweeper(AThreadDataBase):
    dbPJStats = None
    dbPJTableObjectStats = None
    #........................................................................... 
    def __init__(self):
        
        AThreadDataBase.__init__(self)
        #self.pBase['path']  = 'c:%sscat%sworkbin%sdb%sprojects.fdb' % (SLASH,SLASH,SLASH,SLASH)
        #self.pBase['alias'] = 'PROJECTS'
        
        self.CommitTimeOut      = 500 # milisecond
        self.commitRecordCount  = 1
        self.CountRecord        = 0
        self.CountRecordError   = 0
        self.LastSweepDataTime  = None
        self.SweepTimeOut       = 60       
        self.SweepRunTime       = None
        self.SweepIsProcessing  = False
    #........................................................................... 
    def Work(self):
        self.NetLogFileName        = 'Network%s%s%sWork.log' % (SLASH,self.getName(),SLASH)
        self.NetLogFileNameErrors  = 'Network%s%s%sErrors.log' % (SLASH,self.getName(),SLASH)
        self.Worked = True
        
        while self.Worked:
            try:
                printLog(self.getName() +':Получение статистики по базе PROJECTS...' , True , self.LogFileName) 
                from modules.dbStat import TFDBStatistic
                self.dbPJStats = TFDBStatistic("c:\\SCAT\\WORKBIN\\DB\\PROJECTS.FDB")
                self.dbPJStats.getStat()
                self.dbPJTableObjectStats = self.dbPJStats.getTableInfo('OBJECTS' )
                printLog(self.getName() +"Размер страницы:"+str(self.dbPJStats.PageSize) , True , self.LogFileName) 
                printLog(self.getName() +"Дата/время создания БД:"+str(self.dbPJStats.CreationDate) , True , self.LogFileName) 
                printLog(self.getName() +':Сведения по таблице "OBJECTS":.' + str(self.dbPJTableObjectStats) , True , self.LogFileName) 
                
                printLog(self.getName() +':Получена статистика по базе PROJECTS.' , True , self.LogFileName) 
                
                if self.DataBaseConnect():
                        printLog(self.getName() +':Cборка мусора on-line данных...' , True , self.LogFileName)  
                        self.SweepIsProcessing = True
                        self.ExecQuery(""" SELECT count(*) FROM "Objects"; """, True)
                        self.SweepIsProcessing = False
                        printLog(self.getName() +':Cборка мусора on-line данных выполнена за %s [%s - %s].' % ( str(self.QueryRuntime), str(self.QueryEndTime) , str(self.QueryStartTime) ), True , self.LogFileName, False)
                        self.SweepRunTime = self.QueryRuntime  
                self.DataBaseDisconnect()        
            except Exception as e :
                printLog(self.getName() +':Ошибка сборки мусора on-line данных :%s' % ( str(e)), True , self.LogFileName)
                printLog(self.getName() +':Ошибка сборки мусора on-line данных :%s' % ( str(e)), True , self.LogFileNameErrors)
            self.LastSweepDataTime = datetime.datetime.now()
            self.CleanNetwork(600)
            time.sleep(self.SweepTimeOut)                                                        
#------------------------------------------------------------------------------#

    def CleanNetwork(self, cleanTimeOut):
        try:          
            printLog ("Чистка сетевых потоков..." , True, self.NetLogFileName) 
            import threading
            z = 0
            r = 0
            for thr in threading.enumerate():
                
                try:
                    if thr.getName().find('CP_') >0 :
                        r += 1
                        if thr.Worked:
                            if datetime.datetime.now()  > (thr.LastTimeReciveData + datetime.timedelta(seconds = cleanTimeOut) ):
                                printLog("Сетевой поток [%s] залип (последняя активность: %s), завершение..." % ( str(thr.getName()) , str(thr.LastTimeReciveData) ), True, self.NetLogFileName)
                                thr.kill()
                                printLog("Сетевой поток [%s] залип (последняя активность: %s), завершен." % ( str(thr.getName()) , str(thr.LastTimeReciveData) ), True, self.NetLogFileName)
                                z += 1
                except Exception as e:
                    printLog("Ошибка завершения сетевой потока [%s] (последняя активность: %s):." % ( str(thr.getName()) , str(thr.LastTimeReciveData), str(e) ), True, self.NetLogFileNameErrors)
            
            printLog ("Завершено %d из %d сетевых потоков:(всего потоков: %d)." % (z, r, len(threading.enumerate())), True, self.NetLogFileName)  
            printLog ("Чистка сетевых потоков выполнена." , True, self.NetLogFileName)
            
        except Exception as e:
            printLog ("Ошибка чистки сетевых потоков: %s" % ( e), self.__LOG__, self.NetLogFileNameErrors)
 #------------------------------------------------------------------------------#                           
