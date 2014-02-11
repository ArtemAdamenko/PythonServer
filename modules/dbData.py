# -*- coding: utf-8 -*-
import datetime
import time
from core.gDB import AThreadDataBase
from defines.gDefines import *
from core.gGeneral import printLog
class ThreadDataBaseData(AThreadDataBase):
    #........................................................................... 
    ForceSnapshotBuffer = False
    RecCommitSnapshotBuffer = 100 # количество фиксируемых записей при сбросе в файл
    def __init__(self):
        
        AThreadDataBase.__init__(self)
        #self.pBase['path']  = 'c:%sscat%sworkbin%sdb%sdata.fdb' % (SLASH,SLASH,SLASH,SLASH)
        #self.pBase['alias'] = 'DATA'
        
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
                
                while len(BufferObjects)>0:
                    try:
                        if self.ForceSnapshotBuffer:
                            self.SnapshotBuffer(BufferObjects,len(BufferObjects), self.SnapshotFileName)
                            self.ForceSnapshotBuffer = False
                        if self.DataBaseConnect():
                            if BufferObjects[0].Route:

                                self.appendBuseData(BufferObjects[0])
                            else:
                                self.appendBaseData(BufferObjects[0])

                            if len(BufferObjects) > 0:
                                BufferObjects.pop(0)
                            
                            self.CountRecord +=1
                            
                            if self.CountRecord % self.commitRecordCount == 0:
                                self.DataBaseDisconnect()
                            
                    except Exception as e:
                        printLog(self.getName() +": Ошибка записи буфера в базу: %s; размер буфера = %d" % (str(e) , len(BufferObjects)), True,self.LogFileNameErrors, False )
                    finally:
                        printLog(self.getName() +': Объем буфера: %d' % len (BufferObjects), True , self.LogFileName, False)
                self.DataBaseDisconnect()
                time.sleep(1)
    #...........................................................................           
    def appendBaseData(self, obj = None):
        if obj:
            try:
                
                    
                if obj.Speed == None:
                    raise Exception ("Нет Сведений о скорости(%s)" % str(obj.Speed))

                if obj.LastTime == None:
                    raise Exception ("Нет Сведений о последнем времени(%s)" % str(obj.LastTime))
                
                if (obj.LastPoint.LON == None) or (obj.LastPoint.LON < 3000) or (obj.LastPoint.LON > 7000):
                    raise Exception ("Некорректное значение последней координате широты (%s)" % str(obj.LastPoint.LON))
                    
                if (obj.LastPoint.LAT == None) or (obj.LastPoint.LAT < 3000) or (obj.LastPoint.LAT > 7000):
                    raise Exception ("Некорректное значение последней координате долготы (%s)" % str(obj.LastPoint.LAT))
                    
                if  self.ExecQuery(" SELECT \"APPEND_BASE_DATA\"(CAST(%d AS smallint), CAST(%d AS smallint), %s, CAST('%s' AS timestamp with time zone), %f, %f, %f, 0, '%s'); "
                                                % (
                                                     obj.Oid
                                                    ,obj.Pid
                                                    ,str(obj.Phone)
                                                    ,str(obj.LastTime)
                                                    ,obj.LastPoint.LON
                                                    ,obj.LastPoint.LAT
                                                    ,obj.Speed

                                                    ," "
                                                  )
                    ):
                    printLog("Записана  в архив(%s) траектория объекта %d/%d(%s) : [%s]" % ( self.getName(), int(obj.Oid), int(obj.Pid),str(obj.Phone),str(obj.LastTime))
                                         , True
                                         ,self.LogFileName
                                         ,False
                                     )
                else:
                    raise Exception ('Ошибка SQL.')
                
            except Exception as e:
                printLog(self.getName() +': Ошибка записи траектории  %s:%s' % ( str(obj.Oid),str(e)), True , self.LogFileName)
                printLog(self.getName() +': Ошибка записи траектории  %s:%s' % ( str(obj.Oid),str(e)), True , self.LogFileNameErrors)
                printLog("Проект:"+str(obj.Pid), True , self.LogFileNameErrors)
                printLog("Объект:"+str(obj.Oid), True , self.LogFileNameErrors)
                printLog("Телефон:"+str(obj.Phone), True , self.LogFileNameErrors)
                printLog("Последнее время:"+str(obj.LastTime), True , self.LogFileNameErrors)
                printLog("Широта:"+str(obj.LastPoint.LON), True , self.LogFileNameErrors)
                printLog("Долгота:"+str(obj.LastPoint.LAT), True , self.LogFileNameErrors)
                printLog("Скорость:"+str(obj.Speed), True , self.LogFileNameErrors)
    #...........................................................................               
    def appendBuseData(self, obj = None):
        if obj:
            try:
                if obj.Route.PrevStationTime == None:
                    raise Exception ("Нет Сведений о времени пред. остановки(%s)" % str(obj.Route.PrevStationTime))
                
                if  self.ExecQuery(" SELECT \"APPEND_BUS_DATA\"(%d, %d, '%s', %d, %d, CAST('%s' AS timestamp with time zone), CAST('%s' AS timestamp with time zone)); "
                                                % (
                                                     obj.Oid
                                                    ,obj.Pid
                                                    ,str(obj.Phone)
                                                    ,obj.Route.LastRoute
                                                    ,obj.Route.LastStation
                                                    ,obj.Route.LastStationTime
                                                    ,obj.Route.PrevStationTime

                                                    
                                                  )
                    ):
                    printLog("Записана  в архив(%s) остановка объекта %d/%d(%s): [маршрут  %d N ост. %d - время %s] " % ( self.getName(), int(obj.Oid), int(obj.Pid), str(obj.Phone), obj.Route.LastRoute, obj.Route.LastStation,obj.Route.LastStationTime)
                                         , True
                                         ,self.LogFileName
                                         ,False
                                     )
                else:
                    raise Exception ('Ошибка SQL.')
            except Exception as e:
                printLog(self.getName() +': Ошибка записи остановки  %s:%s' % ( str(obj.Oid),str(e)), True , self.LogFileName)
                printLog(self.getName() +': Ошибка записи остановки  %s:%s' % ( str(obj.Oid),str(e)), True , self.LogFileNameErrors)
                printLog("Проект:"+str(obj.Pid), True , self.LogFileNameErrors)
                printLog("Объект:"+str(obj.Oid), True , self.LogFileNameErrors)
                printLog("Телефон:"+str(obj.Phone), True , self.LogFileNameErrors)
                printLog("код маршрута:"+str(obj.Route.LastRoute), True , self.LogFileNameErrors)
                printLog("последняя остановка:"+str(obj.Route.LastStation), True , self.LogFileNameErrors)
                printLog("время последней остановки:"+str(obj.Route.LastStationTime), True , self.LogFileNameErrors)
                printLog("пред. оставновка:"+str(obj.Route.PrevStation), True , self.LogFileNameErrors)
                printLog("время пред. остановки:"+str(obj.Route.PrevStationTime), True , self.LogFileNameErrors)
    #...........................................................................   
    def SnapshotBuffer(self, inbuf, lenSnapshot, fname):
        try:
            printLog("Сброс буфера в файл [%s]..." % str(fname), True , self.LogFileName)      
            printLog("Объем буфера: %d, чистим %d записей" % ( len(inbuf), lenSnapshot ), True , self.LogFileName)      
            dump = []
            
            s = ''
            i = 0
            for obj in inbuf[:lenSnapshot]:
                i +=1
                if obj.Route:
                    s = " SELECT \"APPEND_BUS_DATA\"(%d, %d, '%s', %d, %d, CAST('%s' AS timestamp with time zone), CAST('%s' AS timestamp with time zone)); " % (
                                                     obj.Oid
                                                    ,obj.Pid
                                                    ,str(obj.Phone)
                                                    ,obj.Route.LastRoute
                                                    ,obj.Route.LastStation
                                                    ,obj.Route.LastStationTime
                                                    ,obj.Route.PrevStationTime


                                                  )
                else:
                    s = " SELECT \"APPEND_BASE_DATA\"(CAST(%d AS smallint), CAST(%d AS smallint), %s, CAST('%s' AS timestamp with time zone), %f, %f, %f, 0, '%s'); " % (
                                                     obj.Oid
                                                    ,obj.Pid
                                                    ,str(obj.Phone)
                                                    ,str(obj.LastTime)
                                                    ,obj.LastPoint.LON
                                                    ,obj.LastPoint.LAT
                                                    ,obj.Speed

                                                    ," "
                                                  )
                if i % RecCommitSnapshotBuffer :
                    s = s + ' commit;'
                    
                printLog(s,True,fname)
                
            # чистим буфер
            inbuf[:lenSnapshot] = [] 
            
            
            
            printLog("Объем буфера: %d после чистки" % ( len(inbuf) ), True , self.LogFileName) 
            printLog("Сброс буфера в файл [%s] выполнен." % str(fname), True , self.LogFileName)                  
        except Exception as e:
            printLog("Ошибка сброса буфера"+str(e), True , self.LogFileName)
            printLog("Ошибка сброса буфера"+str(e), True , self.LogFileNameErrors)
    #...........................................................................   
#------------------------------------------------------------------------------#
