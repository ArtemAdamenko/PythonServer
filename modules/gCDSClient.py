# -*- coding: utf-8 -*-/
__DEBUG__ = False
__LOG__  = True
#------------------------------------------------------#
from core.nClient import netClient
import struct
import os
import socket
import copy
from defines.pkgDefines import *
from defines.gDefines import *

from core.gGeneral import printLog

from modules.dbOnline import ThreadDataBasePj
from modules.dbData import ThreadDataBaseData
from ctypes import *
#------------------------------------------------------#
class talkToClientCSD (netClient):
    #...........................................................................
    def __init__(self, clientSock, addr):
        
        self.clientSock = clientSock
        self.addr = addr
        self.recvData=''
        self.recvDecodeData=[]
        self.lastBlockData = {}
        self.buffPackages=dict()
        
        self.countPackages = 0
        self.Worked = False
        self.LastRecivedDateTime = None
        self.ReciveBufferSize = CDS_RECIVE__BUFFER_SIZE
        
        netClient.__init__(self, clientSock, addr)
    #...........................................................................    
    
    #...........................................................................    
    def processing (self):
        try:
            self.recvDecodeData = self.decodeInputPackage(self.recvData)
            self.lastBlockData = {}
            if self.recvDecodeData and self.Worked:

                pkg=None
                pkg_size = None

                if      self.recvDecodeData[0]==1   :   pkg_size = CDS_PKG_SIZE_TYPE_1
                elif    self.recvDecodeData[0]==2   :   pkg_size = CDS_PKG_SIZE_TYPE_2

                if pkg_size and self.Worked:
                    while (( int(len(self.recvDecodeData) / pkg_size) > 0 ) and self.Worked ):
                        pkg_size = None
                        if      self.recvDecodeData[0]==1   :   pkg_size = CDS_PKG_SIZE_TYPE_1
                        elif    self.recvDecodeData[0]==2   :   pkg_size = CDS_PKG_SIZE_TYPE_2

                        if pkg_size and self.Worked:
                            pkg = self.recvDecodeData[:pkg_size]

                            if len(pkg)==pkg_size and self.Worked:


                                pkg = self.parsingPackage(pkg)
                                printLog (self.getName()+": Получен пакет: {%s}" % ( str(self.recvDecodeData[:pkg_size]) ),True, self.LogFileName)

                                if pkg and self.Worked:
                                    printLog (self.getName()+": Получен пакет типа [%s] от объекта[%s] : {%s}" % (str(self.recvDecodeData[0]), str(pkg.Phone), str(self.recvDecodeData[:pkg_size]) ),True, self.LogFileName)
                                    self.appnedPackageToBuffers(pkg,self.recvDecodeData[0])
                                self.countPackages+=1

                        self.recvDecodeData = self.recvDecodeData[pkg_size:]
                        if len(self.recvDecodeData) == 0 or self.recvDecodeData == None or not self.Worked:
                            break
            else:
                self.Worked = False
        except Exception as pr_ex:
            printLog (self.getName()+":Ошибка обработки данных: <"+str(pr_ex)+'>',True, self.LogFileName)
            printLog (self.getName()+":Ошибка обработки данных: <"+str(pr_ex)+'>',True, self.LogFileNameErrors)

    #...........................................................................
    

            
    def sdatetimeIncHour(self, _sdatetime, _parse_mask, _hinc):
        try:
            rsdatetime = None
            tt = time.strptime(_sdatetime, _parse_mask)
            tt_hour = tt.tm_hour + _hinc
            tt_day = tt.tm_mday
            tt_mount = tt.tm_mon
            tt_year = tt.tm_year
            if tt_hour >= 24:
                tt_hour = abs(24 - tt_hour)
                tt_day += 1
                import calendar
                count_days = calendar.monthrange(tt_year, tt_mount)
                if tt_day > count_days[1]:
                    tt_day = 1
                    tt_mount +=1
                    if tt_mount > 12:
                        tt_year += 1

            rsdatetime = '%s.%s.%d %s:%s:%s'% (str(tt_day).rjust(2,"0")
                                                           ,str(tt_mount).rjust(2,"0")
                                                           , tt_year
                                                           , str(tt_hour).rjust(2,"0")
                                                           , str(tt.tm_min).rjust(2,"0")
                                                           , str(tt.tm_sec).rjust(2,"0")
                                                           )
        except Exception as e:
            printLog("Ошибка инкремента дата-времени(%s):%s" % (_sdatetime , str(e)), True, self.LogFileName, False)
            
        return rsdatetime

    


    def parsingPackage(self, data):
        try:
            result = None
            if   (data[0] == 1)  : # если пакет 1-го типа
            
                # телефон ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _tmp = data[3:8]
                    _phone=""
                    for i in _tmp:
                        a= str("%X" % i).rjust(2,'0')
                        _phone+= a #'-'+str( hex(i) ) 
                except Exception as e:
                    raise Exception ('Ошибка получения номера телефона:' + str(e))
                    
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                # координата широты ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _tmp = data[8:12]
                    
                    atmp=""
                    for a in _tmp:
                        atmp +=("%X" % int(a)).rjust(2,"0")  
                    _lon_ = struct.unpack('f', bytes.fromhex(atmp))[0]
                    
                except Exception as e:
                    raise Exception ('Ошибка получения координаты широты:' + str(e))
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                # координата долготы ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _tmp = data[12:16]
                    
                    atmp=""
                    for a in _tmp:
                        atmp +=("%X" % int(a)).rjust(2,"0")
                     
                    _lat_ = struct.unpack('f', bytes.fromhex(atmp))[0]
                except Exception as e:
                    raise Exception ('Ошибка получения координаты долготы:' + str(e))
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                # Скорость ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _speed = float(data[16])
                except Exception as e:
                    raise Exception ('Ошибка получения скорости:' + str(e))
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                # Дата-время ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    
                    _date_time = "%s.%s.20%d %s:%s:%s" % (str(data[17]).rjust(2,"0")
                                                        , str(data[18]).rjust(2,"0")
                                                        , int(data[19])
                                                        , str(data[20]).rjust(2,"0")
                                                        , str(data[21]).rjust(2,"0"), 
                                                        str(data[22]).rjust(2,"0"), )
                    _date_time = self.sdatetimeIncHour(_date_time, PKG_CDS_PARSE_TIME_MASK, PKG_CDS_HOURS_INC)

                    if not self.chekValidDateTime(_date_time,PKG_CDS_PARSE_TIME_MASK):
                        raise Exception ('Некорректная дата-время:' + str(_date_time))


                    
                    
                    
                except Exception as e:
                    raise Exception ('Ошибка получения даты-времени:' + str(e)) 
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                
                
                # контрльная сумма ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _crc = data[25]
                except Exception as e:
                    raise Exception ('Ошибка получения контрльной суммы:' + str(e)) 
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                global TObject
                result = TObject(None,data[2],data[1],_phone,None,None)
                
                result.Update(_date_time, _lon_, _lat_, _speed)
                
            elif data[0] == 2 : # если пакет 2-го типа - с остановками
                # код маршрута ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _last_route = int(data[2])
                except Exception as e:
                    raise Exception ('Ошибка получения кода маршрута :' + str(e))
                 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                # телефон ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _tmp = data[4:9]
                    _phone=""
                    for i in _tmp:
                        a= str("%X" % i).rjust(2,'0')
                        _phone+= a #'-'+str( hex(i) ) 
                except Exception as e:
                    raise Exception ('Ошибка получения номера телефона:' + str(e))
                    
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                              
                # последняя остановка ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _last_station= int(data[9])
                except Exception as e:
                    raise Exception ('Ошибка последней остановки:' + str(e))
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
                 
                # пассажиро-поток ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                #
                #
                #
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                 
                
                
                # Дата-время последней оставновки ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                try:
                    
                    _last_date_time = "%s.%s.20%d %s:%s:%s" % (str(data[22]).rjust(2,"0")
                                                        , str(data[23]).rjust(2,"0")
                                                        , int(data[24])
                                                        , str(data[25]).rjust(2,"0")
                                                        , str(data[26]).rjust(2,"0"), 
                                                        str(data[27]).rjust(2,"0"), )
                    
                    _last_date_time = self.sdatetimeIncHour(_last_date_time, PKG_CDS_PARSE_TIME_MASK, PKG_CDS_HOURS_INC)
                    if not _last_date_time:
                        raise Exception ('Ошибка инкремена.' + str(data))

                    if not self.chekValidDateTime(_last_date_time, PKG_CDS_PARSE_TIME_MASK):
                        raise Exception ('Некорректная дата-время:' + str(_last_date_time))
                    
                    
                except Exception as e:
                    raise Exception ('Ошибка получения даты-времени последней оставновки:%s{%s}(%d)'  % (str(e) , str(data), len(data)))
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                # предыдущая остановка ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _prev_station = int(data[28])
                except Exception as e:
                    raise Exception ('Ошибка предыдущей остановки:' + str(e))
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                        
                # Дата-время предыдущей оставновки ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                try:                    
                    _date_time_prev = "%s.%s.20%d %s:%s:%s" % (str(data[29]).rjust(2,"0")
                                                        , str(data[30]).rjust(2,"0")
                                                        , int(data[31])
                                                        , str(data[32]).rjust(2,"0")
                                                        , str(data[33]).rjust(2,"0"), 
                                                        str(data[34]).rjust(2,"0"), )
                    _date_time_prev = self.sdatetimeIncHour(_date_time_prev, PKG_CDS_PARSE_TIME_MASK, PKG_CDS_HOURS_INC)

                    if not self.chekValidDateTime(_date_time_prev, PKG_CDS_PARSE_TIME_MASK):
                        raise Exception ('Некорректная дата-время:' + str(_date_time_prev))
                    
                    
                except Exception as e:
                    raise Exception ('Ошибка получения даты-времени предыдущей оставновки:' + str(e)) 
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                # контрльная сумма ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _crc = data[37]
                except Exception as e:
                    raise Exception ('Ошибка получения контрльной суммы:' + str(e)) 
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                result = TObject(None,data[3],data[1],_phone, None, None)
                result.UpdateRoute(_last_route, _last_station, _last_date_time, _prev_station, _date_time_prev)
                
        except Exception as e:
            printLog ("Ошибка разбора пакета:" + str(e), True, self.LogFileName)
            result = None

        return result

    #...........................................................................
    def appnedPackageToBuffers(self, obj, pkg_type):
        try:
            global DBObjectsList
            global TObject
            global BufferObjects
            
           
            
            for o in DBObjectsList:
                if int(o.Phone) == int(obj.Phone):
                    obj.Oid = o.Oid
                    obj.Pid = o.Pid
                    obj.Ids = o.Ids
                    
                    is_append_to_buff = True
                    if pkg_type == 1:
                        o.Update(obj.LastTime, obj.LastPoint.LON, obj.LastPoint.LAT , obj.Speed)                        
                    elif pkg_type == 2:  
                        if o.Route:
                            if ( obj.Route.LastStation == o.Route.LastStation ):
                                #obj_rlasttime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(obj.Route.LastStationTime ,"%d.%m.%Y %H:%M:%S")))
                                #o_rlasttime   = datetime.datetime.fromtimestamp(time.mktime(time.strptime(o.Route.LastStationTime ,"%d.%m.%Y %H:%M:%S")))
                                
                                #if (obj_rlasttime >= o_rlasttime):
                                is_append_to_buff = False
                                obj_rlasttime = None
                                o_rlasttime = None
                                
                        o.UpdateRoute(obj.Route.LastRoute, obj.Route.LastStation, obj.Route.LastStationTime, obj.Route.PrevStation, obj.Route.PrevStationTime)
                    
                    if is_append_to_buff:
                        BufferObjects.append(obj)
                    else:
                        printLog (self.getName()+':Получена дублирующая остановка [маршрут: %s; телефон: %s]. Последняя зафиксированная %s - %s : получена %s - %s' %  ( str(obj.Route.LastRoute), str(obj.Phone), str(o.Route.LastStation), str(o.Route.LastStationTime), str(obj.Route.LastStation), str(obj.Route.LastStationTime) ), True, self.LogFileNameErrors)
                    
                                    
            #________________________________________________________________________
        except Exception as emess:
            printLog (self.getName()+':Ошибка занесения данных в буфер:' + str(emess), True, self.LogFileName)
            printLog (self.getName()+':Ошибка занесения данных в буфер:' + str(emess), True, self.LogFileNameErrors)

            
#------------------------------------------------------------------------------------------------- 