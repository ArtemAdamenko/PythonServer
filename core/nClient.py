# -*- coding: utf-8 -*-/

#------------------------------------------------------#
import threading
import datetime
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
class netClient (threading.Thread):
    __DEBUG__               = False
    __LOG__                 = True
    clientSock              = None      # сокет
    addr                    = None      # данные адреса
    recvData                = None      # полученные данные
    recvDecodeData          = None      # декодированные полученные данные
    buffPackages            = dict()    # буфер пакетов
    countPackages           = 0         # количество полученных пакетов
    Worked                  = False     # состояние
    LastRecivedDateTime     = None      #
    ReciveBufferSize        = None      # размер фходного буфера
    
    TimeStartClient         = None      # время запуска клиента(подключения)
    TimeOutActivity         = 600       # максимальный период активности подключения (секунды)
    LastTimeReciveData      = None      # время последнего получения данных
    LogPath                 = ""
    LogFileName             = ""
    LogFileNameErrors       = ""
    countPackages           = 0         #  количество полученных пакетов
    sizeReciveData          = 0         # объем полученных данных - байты
    #...........................................................................
    def __init__(self, clientSock, addr):
        
        self.clientSock = clientSock
        self.addr = addr
        self.recvData=''
        self.recvDecodeData=[]
        self.TimeStartClient = datetime.datetime.now()
        self.LastTimeReciveData = datetime.datetime.now()
        threading.Thread.__init__(self)
    #........................................................................... 
    
    #...........................................................................    
    def run (self):
        
        try:
            
            self.LogFileName = self.LogPath + SLASH + '__conn__'+ str (self.addr[0]).replace('.','_')+'.log'
            self.LogFileNameErrors = self.LogPath + SLASH + '__conn__'+ SLASH+ 'errors'+SLASH+ str (self.addr[0]).replace('.','_')+'.log'
            
            printLog(self.getName()+': Входящее подключение: '.ljust(30,'.') + str (self.addr).rjust(30, '.')+'\r\n', self.__LOG__, self.LogFileName, self.__DEBUG__)
            if self.ReciveBufferSize:
                self.Worked = True
            else:
                raise Exception('Входной буфер не инициализирован.')
                
            while self.Worked:
                try:      
                    
                        
                    printLog (self.getName()+": Получение данных (%d)..." % self.ReciveBufferSize, self.__LOG__, self.LogFileName, self.__DEBUG__)
                    
                    self.recvData = self.clientSock.recv (self.ReciveBufferSize)
                    

                    printLog (self.getName()+":Получены данные:\r\n[" + str(self.recvData) + "] - %d байт(а)." % len(self.recvData), self.__LOG__, self.LogFileName, self.__DEBUG__)
                    if self.recvData:
                        self.LastTimeReciveData = datetime.datetime.now()
                        printLog (self.getName()+":Получены данные:\r\n[" + str(self.recvData) + "] - %d байт(а)." % len(self.recvData), self.__LOG__, self.LogFileName, self.__DEBUG__)
                        self.sizeReciveData += len(self.recvData)
                        try:
                            self.processing()
                        except Exception as pr_ex:
                            raise Exception ("ошибка внутреннего обработчика <%s>" % str(pr_ex))
                            printLog(self.getName()+': Ошибка:' + str(n_ex), self.__LOG__, self.LogFileNameErrors, self.__DEBUG__)
                    else:
                        printLog (self.getName()+":Ничего не получено.", self.__LOG__, self.LogFileName, self.__DEBUG__)
                        self.Worked = False
                        
                
                except Exception as err:
                    self.Worked = False
                    
                    if err.args[0] == 10053:
                        printLog (self.getName()+": Клиент инициировал отключение.", self.__LOG__, self.LogFileName, self.__DEBUG__)
                    elif err.args[0] == 10054:
                        printLog (self.getName()+": Клиент отключился.", self.__LOG__, self.LogFileName, self.__DEBUG__)
                    elif err.args[0] == 10054:
                        raise Exception ("нет возможности работать с подключением: [ %s ] сокет: %s" % ( str(err), str(self.clientSock) ))
                        self.clientSock
                    else:
                        raise Exception ("другая ошибка: [%s] сокет: %s" % ( str(err), str(self.clientSock) ))
                    
                
                       
        except Exception as n_ex:
            printLog(self.getName()+': Ошибка:' + str(n_ex), self.__LOG__, self.LogFileName, self.__DEBUG__)
            printLog(self.getName()+': Ошибка:' + str(n_ex), self.__LOG__, self.LogFileNameErrors, self.__DEBUG__)
            
            
        self.kill()
        printLog (self.getName()+": Подключение закрыто.", self.__LOG__, self.LogFileName, self.__DEBUG__)
    #...........................................................................
    def chekValidDateTime(self, _sdatetime, _parse_mask):
        
        try:
            valid = False
            if _sdatetime:
                
                
                try:
                    curr_dt = datetime.datetime.now()
                    pkg_dt = time.strptime(_sdatetime, _parse_mask)
                except Exception as ex:
                    raise Exception ('Ошибка приведения к формату[%s] :%s' % ( str(_parse_mask), str(_sdatetime) ))
               
                pkg_dt = datetime.datetime(pkg_dt.tm_year, pkg_dt.tm_mon, pkg_dt.tm_mday, pkg_dt.tm_hour , pkg_dt.tm_min , pkg_dt.tm_sec)
                
                
                valid = ( pkg_dt < (curr_dt + datetime.timedelta(seconds = 600)) )
                if not valid:
                    raise Exception ('Некорректное значение времени-из будущего: текущее :%s; получено :%s' % ( str(curr_dt), str(pkg_dt) ))
                        
                             

        except Exception as e:
            valid = False
            printLog("Ошибка проверки даты-времени(%s):%s" % (_sdatetime , str(e)), True, self.LogFileName, False)
            printLog("Ошибка проверки даты-времени(%s):%s" % (_sdatetime , str(e)), True, self.LogFileNameErrors, False)
            
            
        return valid
    #...........................................................................
    def decodeInputPackage(self, data):
        try:
            result = []
            for i in data:
                result.append(i)
        except Exception as e:
            printLog("Ошибка декодирования входных данных %s" % str(e), True, self.LogFileName)
            printLog("Ошибка декодирования входных данных %s" % str(e), True, self.LogFileNameErrors, self.__DEBUG__)
            #result = []
        return result
    #...........................................................................
    def processing(self):
        pass
            
    def kill(self):
        try:
            printLog (self.getName()+": Завершение подключения...", self.__LOG__, self.LogFileName, self.__DEBUG__)
            self.Worked = False
            self.clientSock.close()
        except Exception as kill_ex:
            printLog(self.getName()+': Ошибка закрытия подключения:' + str(kill_ex), self.__LOG__, self.LogFileName, self.__DEBUG__)
            printLog(self.getName()+': Ошибка закрытия подключения:' + str(kill_ex), self.__LOG__, self.LogFileNameErrors, self.__DEBUG__)
        
        
#------------------------------------------------------------------------------------------------- 