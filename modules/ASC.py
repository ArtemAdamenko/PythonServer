# -*- coding: utf-8 -*-/


# типы пакетов
pt_PKG_INFO = 1     # информационный
pt_PKG_IMEI = 3     # IMEI



#------------------------------------------------------#

import struct
import os
import socket
import copy
import datetime
import time
from symbol import lambdef



from core.nClient import netClient
from defines.pkgDefines import *
from defines.gDefines import *

from core.gGeneral import printLog

from modules.dbOnline import ThreadDataBasePj
from modules.dbData import ThreadDataBaseData
from ctypes import *
#------------------------------------------------------#
class TASC6 (netClient):
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
        self.ReciveBufferSize = ASC_RECIVE__BUFFER_SIZE
        self.__DEBUG__ = False
        self.__LOG__   = True
        netClient.__init__(self, clientSock, addr)
    #...........................................................................    
    

    #...........................................................................    
    def processing (self):
        try:
            pkg=None
            pkg_size = None

            pkg_size = ASC_PKG_SIZE_TYPE_6
            self.recvDecodeData = self.decodeInputPackage(self.recvData)
            self.lastBlockData = {}
            if self.recvDecodeData:
                self.Worked = (len(self.recvDecodeData)%pkg_size == 0)
                if not self.Worked:
                    printLog (self.getName()+": Получены несоответствующие данному протоколу данные",True, self.LogFileName)

            if self.recvDecodeData and self.Worked:

                
                

                if pkg_size and self.Worked:
                    
                    while (( int(len(self.recvDecodeData) / pkg_size) > 0 ) and self.Worked ):
                        
                        if len(self.recvDecodeData) < pkg_size:
                            
                            printLog (self.getName()+":короткий пакет [%s] длинна = %d..." % ( str(pkg), len(pkg) ) ,True, self.LogFileName)
                        

                        if pkg_size and self.Worked:
                            pkg = self.recvDecodeData[:pkg_size]
                            
                            printLog (":Обработка пакета [%s] длинна = %d..." % ( str(pkg), len(pkg) )  ,True, self.LogFileName)
                            if len(pkg)==pkg_size and self.Worked:

                                
                                self.lastBlockData = self.parsingPackage(pkg)
                                self.appnedBlockToBuffers()
                                #printLog (self.getName()+": Получен пакет: {%s}" % ( str(self.recvDecodeData[:pkg_size]) ),True, self.LogFileName)

                                #if pkg and self.Worked:
                                #    printLog (self.getName()+": Получен пакет типа [%s] от объекта[%s] : {%s}" % (str(self.recvDecodeData[0]), str(pkg.Phone), str(self.recvDecodeData[:pkg_size]) ),True, self.LogFileName)
                                #     self.appnedPackageToBuffers(pkg,self.recvDecodeData[0])
                                self.countPackages+=1

                        self.recvDecodeData = self.recvDecodeData[pkg_size:]
                        if len(self.recvDecodeData) == 0 or self.recvDecodeData == None or not self.Worked:
                            break
            else:
                self.Worked = False
        except Exception as pr_ex:
            printLog (self.getName()+":Ошибка обработки данных: <"+str(pr_ex)+'>',True, self.LogFileName)
            printLog (self.getName()+":Ошибка обработки данных: <"+str(pr_ex)+'>',True, self.LogFileNameErrors, self.__DEBUG__)

    #...........................................................................

    
            

    def DecodeIEEE754(self, indata):
        
        try:   
            atmp=""
            for a in indata: atmp += hex(  int( str(a))  )[2:].rjust(2,"0")
            result = struct.unpack('f', bytes.fromhex(atmp))[0]
        except Exception as e:
            result = None
            printLog("Ошибка IEEE754 преобразования данных (%s):%s" % (indata , str(e)), self.__LOG__, self.LogFileName, self.__DEBUG__)
            printLog("Ошибка IEEE754 преобразования данных (%s):%s" % (indata , str(e)), self.__LOG__, self.LogFileNameErrors, self.__DEBUG__)
        return result

    def ConverCoord(self, indata):
        try:
            a = str(indata)
            result = int(a[:a.find('.')])*100 + float('0.'+a[a.find('.')+1:])*60
        except Exception as ex:
            printLog("Ошибка перевода координаты (%s):%s" % (indata , str(ex)), self.__LOG__, self.LogFileName, self.__DEBUG__)
            result = None

        return result


    def parsingPackage(self, data):
        try:
            
            result = {}
            BlockBumber = None
            ValidCoords = False
            _date_time = None
            _speed_ = None
            _lon_ = None
            _lat_ = None
            
            i = 0       
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            try:
                sbin =  str(bin(  int(  str(data[1])  )  )) + str( bin(  int(  str(data[0])  )  ) )[2:].rjust(8, '0')
                BlockBumber = int ( sbin    , 2 )
            except Exception as e1:
                raise Exception ("Ошибка определения номера блока: "+ str(e1))
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            try:
                PkgSize = int(str(data[2]))
            except Exception as e1:
                raise Exception ("Ошибка определения размера пакета: "+ str(e1))
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            try:
                PkgType = int(str(data[3]))
            except Exception as e1:
                raise Exception ("Ошибка определения типа пакета: "+ str(e1))
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            printLog ("-"*100, self.__LOG__, self.LogFileName, self.__DEBUG__)
            printLog ("Получен пакет от блока %d, размер = %d байт" % (BlockBumber, PkgSize), self.__LOG__, self.LogFileName, self.__DEBUG__)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if PkgType == pt_PKG_IMEI:
                # если получен пакет IMEI
                printLog ("Получен пакет с IMEI", self.__LOG__, self.LogFileName, self.__DEBUG__)
            elif PkgType == pt_PKG_INFO:
                # если получен информационный пакет
                printLog ("Получен информационный пакет:", self.__LOG__, self.LogFileName, self.__DEBUG__)
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                OtherByte = int(str(data[4]))
                printLog ("Служебный байт :" + str(OtherByte) , self.__LOG__, self.LogFileName, self.__DEBUG__)

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    NumPkg = int ( str(bin(  int(  str(data[6])  )  ))+ str( bin(  int(  str(data[5])  )  ) )[2:].rjust(8, '0')    , 2 )
                    printLog ("Номер пакета внутри оборудования:" + str(NumPkg) , self.__LOG__, self.LogFileName, self.__DEBUG__)
                except Exception as e1:
                    raise Exception ("Ошибка определения номера пакета: " + str(e1))

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    VerFW = int(str(data[7]))
                    printLog ("Версия прошивки :" + str(VerFW) , self.__LOG__, self.LogFileName, self.__DEBUG__)
                except Exception as e1:
                    raise Exception ("Ошибка определения версии прошивки: " + str(e1))
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    
                    StatusPkg =  (str(bin(  int(  str(data[9])  )  ))+ str( bin(  int(  str(data[8])  )  ) )[2:].rjust(8, '0'))[2:]
                    printLog ("Статус: " + str(StatusPkg) , self.__LOG__, self.LogFileName, self.__DEBUG__)
                except Exception as e1:
                    raise Exception ("Ошибка определения статуса: " + str(e1))

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    ValidCoords = (int(str(data[31]))==0)
                    printLog ("Валидность координат - " + str( (lambda s: 'OK' if s else 'NO' )(ValidCoords) ), self.__LOG__, self.LogFileName, self.__DEBUG__)
                except Exception as e1:
                    raise Exception ("Ошибка определения валидности координат: " + str(e1))

                # Время ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:

                    _time = data[32:36]
                    _time.reverse()
                    a = ""
                    for d in _time:

                        a += hex(  int( str(d))  )[2:].rjust(2,"0")
                    _time = int(a, 16)

                    printLog ("Время: %s " % str(_time), self.__LOG__, self.LogFileName, self.__DEBUG__)
                except Exception as e1:
                    raise Exception ('Ошибка получения времени от блока %d:%s' %(BlockBumber, str(e1)))

                # Дата ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:

                    _date = data[36:40]
                    _date.reverse()
                    
                    a = ""
                    for d in _date:
                       
                        a += hex(  int( str(d))  )[2:].rjust(2,"0")
                    _date = int(a, 16)

                    printLog ("Дата: %s " % str(_date), self.__LOG__, self.LogFileName, self.__DEBUG__)
                    
                except Exception as e1:
                    raise Exception ('Ошибка получения даты от блока %d:%s' % (BlockBumber, str(e1)))

                # Дата - время ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                try:
                    _date = str(_date)
                    
                    _date_time = datetime.datetime(int('20'+_date[len(_date)-2:len(_date)]), int(_date[len(_date)-4:len(_date)-2]), int(_date[:len(_date)-4]), 0, 0, 0)
                    _date_time = _date_time + datetime.timedelta(seconds = _time)
                    _date_time = _date_time + datetime.timedelta(seconds = 14400) # делаем инкремент 4 часа, потому как разница от грнивича 4 часа )))
                    printLog ("Дата-время: %s " % str(_date_time), self.__LOG__, self.LogFileName, self.__DEBUG__)
                    
                    _date_time = str(_date_time)
                    y = _date_time[:4]
                    m = _date_time[5:7]
                    d = _date_time[8:10]
                    _date_time = "%s.%s.%s %s" % (d,m,y,_date_time[11:])
                except Exception as e1:
                    raise Exception ('Ошибка получения даты-времени от блока %d:%s' %(BlockBumber, str(e1)))
                    
                if not self.chekValidDateTime(_date_time,PKG_CDS_PARSE_TIME_MASK):
                        raise Exception ('Некорректная дата-время от блока %d:%s' % (BlockBumber, str(_date_time)) )

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if ValidCoords:
                    # координата широты ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    _lon_ = self.DecodeIEEE754(data[40:44])
                    if _lon_ is None:
                        raise Exception ('Ошибка получения координаты широты от блока %d.' % BlockBumber)
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


                    # координата долготы ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    _lat_ = self.DecodeIEEE754(data[44:48])
                    if _lat_ is None:
                        raise Exception ('Ошибка получения координаты долготы от блока %d.' % BlockBumber)

                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


                    printLog ("Координаты блока %d: широта: %s / долгота: %s" % (BlockBumber, str(_lon_), str(_lat_)) , self.__LOG__, self.LogFileName, self.__DEBUG__)
                    
                    _lon_ = self.ConverCoord(_lon_)
                    _lat_ = self.ConverCoord(_lat_)
                    printLog ("Координаты блока %d: широта: %s / долгота: %s" % (BlockBumber, str(_lon_), str(_lat_)) , self.__LOG__, self.LogFileName, self.__DEBUG__)
                    

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                _height_ = self.DecodeIEEE754(data[48:52])
                printLog ("Высота над уровнем моря: %s м." % str(_height_), self.__LOG__, self.LogFileName, self.__DEBUG__)
                if _height_ is None:
                    raise Exception ('Ошибка получения высоты над уровнем моря от блока %d.' % BlockBumber)
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                _speed_ = self.DecodeIEEE754(data[52:56])
                printLog ("Скорость: %s км./ч." % str(_speed_), self.__LOG__, self.LogFileName, self.__DEBUG__)
                if _speed_ is None:
                    raise Exception ('Ошибка получения скорости от блока %d.' % BlockBumber)
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                try:
                    CountSatellite = int(str(data[64]))
                    
                    printLog ("Количество спутников %d" % CountSatellite , self.__LOG__, self.LogFileName, self.__DEBUG__)
                except Exception as e1:
                    raise Exception ("Ошибка определения количества спутников блока %d:%s " % (BlockBumber, str(e1)) )
                 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                result['BLOCK_NUMBER'] = BlockBumber
                result['VALID'] = ValidCoords
                
                result['TIME'] = _date_time
                result['SPEED'] = _speed_
                result['LON'] = _lon_
                result['LAT'] = _lat_
            else:
                 # если получен хз пакет
                printLog ("Получен НЕИЗВЕСТНЫЙ пакет", self.__LOG__, self.LogFileName, self.__DEBUG__)

          
        except Exception as e:
            printLog ("Ошибка разбора пакета:" + str(e), True, self.LogFileName, self.__DEBUG__)
            printLog ("Ошибка разбора пакета:" + str(e), True, self.LogFileNameErrors, self.__DEBUG__)
            result = {}

        return result




    def appnedBlockToBuffers(self):
        try:
            rec = self.lastBlockData

            
            if len(rec)>0:
                if ('BLOCK_NUMBER' in rec):
                    if len(rec) > 1:
                        if rec['VALID']:
                            global DBObjectsList
                            global TObject
                            global BufferObjects



                            block_exist = False
                            for o in DBObjectsList:
                                if o.BlockNumber:
                                    if o.BlockNumber == int(rec['BLOCK_NUMBER']):
                                        block_exist = True
                                        o.Update(rec['TIME'], rec['LON'], rec['LAT'] , rec['SPEED'])

                                        BufferObjects.append(o)
                            if not block_exist:
                                raise Exception ("Блок %d не зарегистрирован!" % int(rec['BLOCK_NUMBER']))
                            #________________________________________________________________________

        except Exception as emess:
            printLog(self.getName()+':Ошибка занесения данных в буфер:' + str(emess),True,self.LogFileName, self.__DEBUG__)
            printLog(self.getName()+':Ошибка занесения данных в буфер:' + str(emess),True,self.LogFileNameErrors, self.__DEBUG__)