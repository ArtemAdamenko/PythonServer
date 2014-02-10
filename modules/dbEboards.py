# -*- coding: utf-8 -*-
import datetime
import time
from core.gDB import AThreadDataBase
from defines.gDefines import *
from core.gGeneral import printLog



class ThreadDataBaseEBOARDS(AThreadDataBase):
    PointTrackTimeLength    = 10800 # длительность хранения трека координат 3 часа 
    BStationTrackTimeLength = 10800 # длительность хранения трека остановок 3 часа 
    LastSweepTrackDateTime  = None  # время последней чистки треков
    SweepTrackTimeOut       = 60    # период чистки треков
    #........................................................................... 
    def __init__(self):
        self.LastSweepTrackDateTime = datetime.datetime.now()
        AThreadDataBase.__init__(self)
        self.pBase['path']  = 'c:%sscat%sworkbin%sdb%sEBOARDS.fdb' % (SLASH,SLASH,SLASH,SLASH)
        self.pBase['alias'] = 'EBOARDS'
        
        self.CommitTimeOut      = 500 # milisecond
        self.commitRecordCount  = 1
        self.CountRecord        = 0
        self.CountRecordError   = 0
        self.onlineCount        = 0
        
    #...........................................................................     
    def Work(self):
        
        global DBObjectsList
        global TObject
        self.CountRecord        = 0
        onlineCount = 0
        self.Worked = True
        while self.Worked:
            self.CountRecord        = 0
            onlineCount = 0
            onlineRouteCount        = 0
            if self.DataBaseConnect():
                
                for i in DBObjectsList:
                    try:
                        # запись траектории ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        is_update = not (i.LastReciveTime == None)
                        
                        if is_update:
                            
                            if i.LastReciveTime >= (datetime.datetime.now() - datetime.timedelta(seconds=600)):
                                onlineCount +=1
                            if not i.PrevReciveTime == None:
                               is_update = i.LastReciveTime > i.PrevReciveTime
                        
                        if is_update:
                            
                            self.ExecQuery("""  UPDATE OBJECTS O
                                                SET 
                                                    O.LAST_TIME_ = '%s'
                                                    ,O.LAST_LON_ = %f
                                                    ,O.LAST_LAT_ = %f
                                                    ,O.LAST_SPEED_ = %f
                                                WHERE O.IDS_ = %d; """
                                            % (
                                                i.LastTime
                                                ,i.LastPoint.LON
                                                ,i.LastPoint.LAT
                                                ,i.Speed
                                                ,i.Ids
                                              )
                                        )
                                                                   
                            
                            self.CountRecord+=1
                            printLog("Записана траетория(%s) Объект:%d: пакетов: %d " % ( self.getName()
                                                                                           , int(i.Ids)
                                                                                           , i.CountRecivedPackaged
                                                                                          )
                                     , False
                                     , self.LogFileName
                                     , False
                                 )
                            self.appendBaseData(i)
                        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                        # запись последней остановки ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        is_route_update = False
                        is_route_update = not (i.Route == None)
                        if is_route_update:
                            is_route_update = not (i.Route.RouteLastTimeUpdate == None)
                        
                            if is_route_update:
                                if i.Route.RouteLastTimeUpdate >= (datetime.datetime.now() - datetime.timedelta(seconds=600)):
                                    onlineRouteCount +=1
                                if not i.Route.RoutePrevTimeUpdate == None:
                                    is_route_update = i.Route.RouteLastTimeUpdate > i.Route.RoutePrevTimeUpdate

                        if is_route_update:

                            self.ExecQuery("""  UPDATE OBJECTS O
                                                SET
                                                    O.LAST_STATION_ = %d
                                                    ,O.LAST_STATION_TIME_ = '%s'
                                                    ,O.LAST_ROUT_ = %d
                                                    
                                                WHERE O.IDS_ = %d; """
                                            % (
                                                i.Route.LastStation
                                                ,i.Route.LastStationTime
                                                ,i.Route.LastRoute
                                                ,i.Ids
                                              )
                                        )


                            self.CountRecord+=1
                            printLog("Записана последня остановка(%s) Объект:%d: пакетов: %d " % ( self.getName()
                                                                                           , int(i.Ids)
                                                                                           , i.CountRecivedPackaged
                                                                                          )
                                     , False
                                     , self.LogFileName
                                     , False
                                 )
                            self.appendBuseData(i)
                        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        
                            
                    except Exception as e:
                        self.CountRecordError+=1
                        printLog(self.getName() +': Ошибка обновления on-line данных %s:%s' % ( str(i),str(e)), True , self.LogFileName, True)
                        printLog(self.getName() +': Ошибка обновления on-line данных %s:%s' % ( str(i),str(e)), True , self.LogFileNameErrors)
                        
                self.lastTimeCommit = datetime.datetime.now()
            
            
            if int(self.CountRecord) > 0:
                printLog(self.getName() +": Записано %d объектов, online за 5 мин. = %d ." % (int(self.CountRecord), onlineCount) ,True, self.LogFileName, False)
            self.onlineCount = onlineCount
            
            if self.dbConnect:
                self.DataBaseDisconnect()
                
            self.SweepTracks()
            
    def SweepTracks(self):
        if (datetime.datetime.now()  > (self.LastSweepTrackDateTime + datetime.timedelta(seconds=self.SweepTrackTimeOut) )):
            if self.DataBaseConnect():
                try:
                    printLog(self.getName() +": Удаление устаревших треков координат..."  ,True, self.LogFileName, False)
                    self.ExecQuery("delete FROM BASEDATA a where abs(datediff(second, a.TIME_, current_timestamp)) > %d; " % ( self.PointTrackTimeLength))
                    printLog(self.getName() +": Удаление устаревших треков координат выполнено."  ,True, self.LogFileName, False)
                except Exception as e:
                    printLog(self.getName() +": Ошибка удаления устаревших треков координат :%s." % str(e) ,True, self.LogFileName, False)
                    printLog(self.getName() +": Ошибка удаления устаревших треков координат :%s." % str(e) ,True, self.LogFileNameErrors, False)
                    
                try:
                    printLog(self.getName() +": Удаление устаревших треков остановок..."  ,True, self.LogFileName, False)
                    self.ExecQuery("delete FROM BUSDATA a where abs(datediff(second, a.TIME_, current_timestamp)) > %d; " % ( self.PointTrackTimeLength))
                    printLog(self.getName() +": Удаление устаревших треков остановок выполнено."  ,True, self.LogFileName, False)
                except Exception as e:
                    printLog(self.getName() +": Ошибка удаления устаревших треков остановок :%s." % str(e) ,True, self.LogFileName, False)
                    printLog(self.getName() +": Ошибка удаления устаревших треков остановок :%s." % str(e) ,True, self.LogFileNameErrors, False) 
                    
                try:
                    printLog(self.getName() +": Служебные расчеты для мониторов ..."  ,True, self.LogFileName, False)
                    self.ExecQuery(" EXECUTE PROCEDURE GET_AVERAGE_TRAFFIC; ")
                    printLog(self.getName() +": Служебные расчеты для мониторов выполнена."  ,True, self.LogFileName, False)
                except Exception as e:
                    printLog(self.getName() +": Ошибка выполнения служебных расчетов для мониторов :%s." % str(e) ,True, self.LogFileName, False)
                    printLog(self.getName() +": Ошибка выполнения служебных расчетов для мониторов :%s." % str(e) ,True, self.LogFileNameErrors, False)      
                    
                    
                    
                try:
                    printLog(self.getName() +": Сборка мусора ..."  ,True, self.LogFileName, False)
                    self.ExecQuery(" SELECT count(*) FROM OBJECTS; ", True)
                    self.ExecQuery(" SELECT count(*) FROM AVGTRAFFIC; ", True)
                    self.ExecQuery(" SELECT count(*) FROM BASEDATA; ", True)
                    self.ExecQuery(" SELECT count(*) FROM BUSDATA; ", True)
                    printLog(self.getName() +": Сборка мусора выполнена."  ,True, self.LogFileName, False)
                except Exception as e:
                    printLog(self.getName() +": Ошибка сборки мусора :%s." % str(e) ,True, self.LogFileName, False)
                    printLog(self.getName() +": Ошибка сборки мусора :%s." % str(e) ,True, self.LogFileNameErrors, False)     
                
                self.LastSweepTrackDateTime = datetime.datetime.now()
                if self.dbConnect:
                    self.DataBaseDisconnect()

#------------------------------------------------------------------------------#


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
                    
                if  self.ExecQuery("""  INSERT INTO BASEDATA (OIDS_, TIME_, LON_, LAT_, SPEED_) VALUES (%d, '%s', %f, %f, %f); """
                                                % (
                                                     obj.Ids
                                                    ,str(obj.LastTime)
                                                    ,obj.LastPoint.LON
                                                    ,obj.LastPoint.LAT
                                                    ,obj.Speed

                                                    
                                                  )
                    ):
                    printLog("Записана  в архив(%s) траектория объекта:%d/%d " % ( self.getName(), int(obj.Oid), int(obj.Pid))
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
                
    def appendBuseData(self, obj = None):
        if obj:
            try:
                if obj.Route.PrevStationTime == None:
                    raise Exception ("Нет Сведений о времени пред. остановки(%s)" % str(obj.Route.PrevStationTime))
                
                if  self.ExecQuery("""  INSERT INTO BUSDATA (OIDS_, ROUT_, TIME_, STATION_)  VALUES ( %d, %d, '%s', %d);"""
                                                % (
                                                     obj.Ids
                                                    ,obj.Route.LastRoute
                                                    ,str(obj.Route.LastStationTime)
                                                    ,obj.Route.LastStation  
                                                  )
                    ):
                    printLog("Записана  в архив(%s) остановка объекта:%d/%d " % ( self.getName(), int(obj.Oid), int(obj.Pid))
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
#------------------------------------------------------------------------------#