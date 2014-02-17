# -*- coding: utf-8 -*-
import datetime
import time
from core.gDB import AThreadDataBase
from defines.gDefines import *
from core.gGeneral import printLog



class ThreadDataBasePj(AThreadDataBase):
    #........................................................................... 
    def __init__(self):
        
        AThreadDataBase.__init__(self)
        #self.pBase['path']  = 'c:%sscat%sworkbin%sdb%sprojects.fdb' % (SLASH,SLASH,SLASH,SLASH)
        #self.pBase['alias'] = 'PROJECTS'
        
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
                            
                            self.ExecQuery("""  UPDATE "Objects"
                                                SET
                                                    "Last_Time" = '%s'
                                                    ,"Last_Lon" = %f
                                                    ,"Last_Lat" = %f
                                                    ,"Last_Speed" = %f
                                                WHERE "IDs" = %d; """
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
                                     , True
                                     , self.LogFileName
                                     , False
                                 )
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

                            self.ExecQuery("""  UPDATE "Objects"
                                                SET
                                                    "Last_Station" = %d
                                                    ,"Last_Station_Time" = '%s'
                                                    ,"Last_Route" = %d
                                                    
                                                WHERE "IDs" = %d; """
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
                                     , True
                                     , self.LogFileName
                                     , False
                                 )
                        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        
                            
                    except Exception as e:
                        self.CountRecordError+=1
                        printLog(self.getName() +': Ошибка обновления on-line данных %s:%s' % ( str(i),str(e)), True , self.LogFileName, True)
                        printLog(self.getName() +': Ошибка обновления on-line данных %s:%s' % ( str(i),str(e)), True , self.LogFileNameErrors, True)
                        
                self.lastTimeCommit = datetime.datetime.now()
            
            if self.dbConnect:
                self.DataBaseDisconnect()
            if int(self.CountRecord) > 0:
                printLog(self.getName() +": Записано %d объектов, online за 5 мин. = %d ." % (int(self.CountRecord), onlineCount) ,True, self.LogFileName, False)
            self.onlineCount = onlineCount
            
            

#------------------------------------------------------------------------------#