# -*- coding: utf-8 -*-
import datetime
import time
from core.gDB import AThreadDataBase
from defines.gDefines import *
from core.gGeneral import printLog


class ThreadGetDBObjects(AThreadDataBase):
    __DEBUG__ = False
    #........................................................................... 
    def __init__(self):
        
        AThreadDataBase.__init__(self)
        #self.pBase['path']  = 'c:%sscat%sworkbin%sdb%sprojects.fdb' % (SLASH,SLASH,SLASH,SLASH)
        #self.pBase['alias'] = 'PROJECTS'
        
        self.CommitTimeOut      = 500 # milisecond
        self.commitRecordCount  = 1
        self.CountRecord        = 0
        self.CountRecordError   = 0
        self.LastGetDataTime    = None
        self.GetTimeOut         = 300
        self.GetCountObjects    = 0
        
    #........................................................................... 
    def Work(self):
        self.Worked = True
        while self.Worked:
            OList = []
            try:
                if self.DataBaseConnect():
                        printLog(self.getName() +':Получение списка зарегистрированных объектов...' , True , self.LogFileName)    
                        self.ExecQuery("""SELECT "Objects"."IDs",
							                     "Objects"."Obj_ID",
							                     "Objects"."Proj_ID",
			                                     "Objects"."Phone",
			                                     COALESCE("Granits"."Block_Number", -1),
							                     COALESCE("Granits"."Block_Type", -1),
                                                 "Objects"."Provider"
                                                 FROM "Objects" left join "Granits" on "Objects"."IDs"="Granits"."OIDs";"""
                                       , True
                                       , OList
                                       )
                        global DBObjectsList
                        
                        for j in DBObjectsList:
                            j.isDB=False
                        #синхронизируем буфер с даннми из базы
                        for i in OList:
                            OL_exist = False
                            for j in DBObjectsList:
                                if j.Phone == i[3]:
                                    OL_exist = True
                                    j.isDB = True
                            if not OL_exist:
                                DBObjectsList.append(TObject(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
                        
                        
                        if self.__DEBUG__:
                            printLog(self.getName() +':Список загруженных объектов:', True , self.LogFileName)
                            for d in OList:
                                printLog(self.getName() + str(d), True , self.LogFileName)
                                
                            printLog(self.getName() +':Буфер объектов после загрузки из БД:', True , self.LogFileName)
                            for d in DBObjectsList:
                                printLog(self.getName() + "Phone:%s/BlockNumber:%s/Ids:%s/LastTime:%s" % ( str(d.Phone), str(d.BlockNumber), str(d.Ids), str(d.LastTime) )
                                , True , self.LogFileName)
                            
                        OList = []        
                        self.GetCountObjects = int(len(DBObjectsList))
                        printLog(self.getName() +':Объекты получены. Количество = %d.' % self.GetCountObjects, True , self.LogFileName)
                self.DataBaseDisconnect()
                self.LastGetDataTime = datetime.datetime.now()
            except Exception as e :
                printLog(self.getName() +':Ошибка получения списка зарегистрированных объектов :%s' % ( str(e)), True , self.LogFileName, False)
                printLog(self.getName() +':Ошибка получения списка зарегистрированных объектов :%s' % ( str(e)), True , self.LogFileNameErrors, False)
            
            time.sleep(self.GetTimeOut)
                
#------------------------------------------------------------------------------#
