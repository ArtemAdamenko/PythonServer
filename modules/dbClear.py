# -*- coding: utf-8 -*-
import datetime
import time
from core.gDB import AThreadDataBase
from defines.gDefines import *
from core.gGeneral import printLog
class ThreadDataBaseData(AThreadDataBase):
    #........................................................................... 
    ForceSnapshotBuffer = False
    def __init__(self):
        
        AThreadDataBase.__init__(self)
        self.pBase['path']  = 'c:%sscat%sworkbin%sdb%sdata.fdb' % (SLASH,SLASH,SLASH,SLASH)
        self.pBase['alias'] = 'DATA'
        
        self.CommitTimeOut      = 500 # milisecond
        self.commitRecordCount  = 100
        self.CountRecord        = 0
        self.CountConnections = 0
        self.CountRecordError   = 0
        self.bufferLen = 0
        
    #...........................................................................     
    def Work(self):
        self.Worked = True
        global BufferObjects
        global TObject
        self.CountRecord        = 0
        
        while self.Worked:
            self.bufferLen = len(BufferObjects)
            if self.DataBaseConnect():
                printLog("Очистка временных таблиц... " %  , True , self.LogFileName ,False )
                if  self.ExecQuery(" delete FROM REPORT2PRINT_1; "):
                    printLog("Очистка временных таблиц выполнена. " %  , True , self.LogFileName ,False )
                else:
                    raise Exception ('Ошибка SQL.')
                
                time.sleep(1)
                
    #...........................................................................           
