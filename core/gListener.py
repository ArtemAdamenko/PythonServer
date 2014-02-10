# -*- coding: utf-8 -*-
#------------------------------------------------------------#
import threading
import socket
import datetime
#------------------------------------------------------------#

from defines.gDefines import *
from core.gGeneral import printLog

     
#------------------------------------------------------------#
class Alistener(threading.Thread):
    __LOG__                 = True      # включение/выключение логирования данного класса
    __DEBUG__               = False     # включение/выключение отладки данного класса
    ConnectionTimeOutIdle   = 600       # период простоя подкючения - секунды
    countPackages           = 0         # количество пакетов
    sizeReciveData          = 0         # объем трафика
    #................................................................................................................................................
    def __init__(self, _host, _port, _sType,_maxClient):
        self.host                   = _host
        self.port                   = _port
        self.maxClients             = _maxClient
        self.type                   = _sType
        self.sServer                = None
        self.LogFileName            = "Network%s%s%sListening.log" % (SLASH, str(self.port), SLASH)
        self.LogFileNameErrors      = "Network%s%s%sErrors.log" % (SLASH, str(self.port), SLASH )
        self.Worked                 = False
        self.Connections            = []
        self.countPackages          = 0
        self.sizeReciveData         = 0
        threading.Thread.__init__(self)
    #................................................................................................................................................    
    def __del__(self):
        if not self.sServer is None:
            self._Stop()
        printLog('Сервер %s остановлен' % str(self.getName()))
        
    #................................................................................................................................................
    def run(self):
        try:
            printLog ("Запуск сервера %s ..." % str(self.getName()), self.__LOG__, self.LogFileName)    
            self.sServer = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            self.sServer = None 
            printLog ("Ошибка запуска сервера %s: %s" % (str(self.getName()), e), self.__LOG__, self.LogFileNameErrors)

        if not self.sServer is None:
            try:
                self.sServer.bind ((str(self.host), int(self.port)))
                self.sServer.listen (int(self.maxClients))
            except socket.error as e:
                self.sServer = None
                printLog ("Ошибка открытия порта %d для прослушивания %s: %s" % ( self.port, str(self.host), str(e) ), self.__LOG__, self.LogFileNameErrors)
                

            if not self.sServer is None:
                self.Worked = True
                printLog("Сервер %s запущен.\r\n" % str(self.getName()))
                while self.Worked:
                    printLog ('Ожидание водящих подключений %s:%d\r\n' % ( str(self.host), int(self.port) ) , self.__LOG__, self.LogFileName, self.__DEBUG__)
                    channel, details = self.sServer.accept ()
                    printLog ('Новое входящее подключение %s:%s ...' % (str(details[0]), str(details[1])) , self.__LOG__, self.LogFileName, self.__DEBUG__)

                    try:
                        if self.type    == PKG_TYPE_M2M :
                            from modules.gM2MClient import talkToClientM2M
                            self.Connections.append(talkToClientM2M (channel, details, PKG_M2M_PARSE_TIME_MASK))

                        elif self.type  == PKG_TYPE_MPS :
                            from modules.gM2MClient import talkToClientM2M
                            self.Connections.append(talkToClientM2M (channel, details, PKG_MPS_PARSE_TIME_MASK))

                        elif self.type  == PKG_TYPE_CDS :
                            from modules.gCDSClient import talkToClientCSD
                            self.Connections.append(talkToClientCSD (channel, details))

                        elif self.type  == PKG_TYPE_ASC :
                            from modules.ASC import TASC6
                            self.Connections.append(TASC6 (channel, details))

                        elif self.type == PKG_TYPE_WEBCONTROL:
                            from modules.webControl import TThrWebControl
                            self.Connections.append(TThrWebControl (channel, details, self.modules))

                        self.Connections[len(self.Connections)-1].setName('TCP_%s_%s' % (str (details[0]).replace('.','_'), str(details[1]) ) )
                        if self.LogFileName.find(SLASH) > 0:
                            s = self.LogFileName
                            s = s.split(SLASH)
                            s.pop()

                            for i in s:
                                self.Connections[len(self.Connections)-1].LogPath = self.Connections[len(self.Connections)-1].LogPath + SLASH + str(i)
                            s = None
                        self.Connections[len(self.Connections)-1].start ()
                        
                    except Exception as ec:
                        printLog ("Ошибка открытия входящего подключения на интерфейсе %s:%s : %s" % ( str(self.host), str(self.port), str(ec) ), self.__LOG__, self.LogFileNameErrors)
                    
                    self.SweepConnections()
                    self.CalcCountPackages()
                   
            self._Stop()
    #................................................................................................................................................        
    def _Stop(self):
        try:
            self.Worked = False
            printLog (self.getName()+": Остановка сервера ... " , self.__LOG__, self.LogFileName, self.__DEBUG__)
            if not self.sServer is None:
                self.sServer.close ()
                printLog (self.getName()+": Слушающий сокет закрыт." , self.__LOG__, self.LogFileName, self.__DEBUG__)                
                self.CloseConnections()
                self.sServer = None
            else:
                raise Exception ("Сервер не работает или уже остановлен.")
        except Exception as ex:
            printLog (self.getName()+":Некорректная остановка модуля: %s " % str(ex), self.__LOG__, self.LogFileNameErrors, self.__DEBUG__)
    #................................................................................................................................................
    def CloseConnections(self):
        try:
            printLog (self.getName()+": Закрытие %d подключений ... " % len(self.Connections), self.__LOG__, self.LogFileName, self.__DEBUG__)
            while len(self.Connections) > 0:
                try:
                    self.Connections[len(self.Connections)-1].Worked=False
                    self.Connections[len(self.Connections)-1].kill()
                    self.Connections.pop()
                except Exception as ex1:
                    printLog (self.getName()+":Ошибка закрытия подключения: %s " % str(ex1), self.__LOG__, self.LogFileNameErrors, self.__DEBUG__)

            
            del self.Connections
            
        except Exception as ex:
            printLog (self.getName()+":Ошибка закрытия подключений: %s " % str(ex), self.__LOG__, self.LogFileNameErrors, self.__DEBUG__)
    #................................................................................................................................................
    def SweepConnections(self):
        try:
            printLog ("Запуск чистки подключений..." , self.__LOG__, self.LogFileName)
            
            
            # ищем неактивные 
            # и залипшие (по которым давно нет передачи данных) 
            # подключения
            
            try:
                printLog ("Определение мертвых подключений(всего подключений:%d)..." % (len(self.Connections)) , self.__LOG__, self.LogFileName)
                idxs = []
                i = 0
                x1 = 0
                x2 = 0
                x3 = 0
                for c in self.Connections:
                    if i < len(self.Connections) -1:
                        if not c.Worked:
                            idxs.append(i)
                            x1 += 1
                        elif c.LastTimeReciveData < ( datetime.datetime.now() - datetime.timedelta(seconds = self.ConnectionTimeOutIdle) ) :
                            idxs.append(i)
                            x2 += 1
                        elif not c.isAlive():
                            idxs.append(i)
                            x3 += 1
                    i+=1
                i=None
                printLog ("Определение мертвых подключений выполнено(выключенных-%d/залипших-%d/неактивных-%d)." % (x1, x2, x3) , self.__LOG__, self.LogFileName)
            except Exception as e1:
                raise Exception ("Ошибка определения мертвых подключений: %s" %  str(e1))
            x1 = None
            x2 = None
            x3 = None
            # удаляем неактивные 
            # и залипшие(по которым давно нет передачи данных) 
            # подключения
            if ( (not idxs is None) and (len(idxs)) ) > 0:
                try:
                    printLog ("Уничтожение мертвых %d подключений(всего подключений:%d)..." % (len(idxs),len(self.Connections)) , self.__LOG__, self.LogFileName)
                    
                    idxs.reverse()
                    
                    x = 0
                    i = 0
                    
                    
                    for i in idxs:
                        if self.Connections[i].Worked:
                            self.Connections[i].Worked = False
                        printLog ("Уничтожение мертвого подключения %s" % str(self.Connections[i].getName()) , self.__LOG__, self.LogFileName)
                        self.Connections[i].kill()
                        del self.Connections[i]   
                        self.Connections.pop(i)
                        
                    i = None
                    printLog ("Уничтожение мертвых подключений выполнено(всего подключений:%d)." % len(self.Connections) , self.__LOG__, self.LogFileName)
                    
                except Exception as e1:
                    raise Exception ("Ошибка удаления мертвых подключений[%s]: %s" % (str(idxs), str(e1) ) )
                
            else:
                printLog ("Все подключения живы." , self.__LOG__, self.LogFileName)
                
            idxs=None
                    
            printLog ("Чистка подключений выполнена." , self.__LOG__, self.LogFileName)
        except Exception as e:
            printLog ("Ошибка чистки подключений: %s" %  str(e), self.__LOG__, self.LogFileNameErrors)
            printLog ("Ошибка чистки подключений: %s" %  str(e), self.__LOG__, self.LogFileName)
    #................................................................................................................................................    
    def CalcCountPackages(self):
        try:
            
            for c in self.Connections:
                self.countPackages  += c.countPackages
                self.sizeReciveData += c.sizeReciveData
        except socket.error as e:
            printLog ("Ошибка подсчета каличества полученных пакетов %s: %s" % (str(self.getName()), e), self.__LOG__, self.LogFileNameErrors)
            
    