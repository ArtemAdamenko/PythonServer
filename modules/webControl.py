# -*- coding: utf-8 -*-


import time

from core.gGeneral import printLog
from core.nClient import netClient
from defines.gDefines import *
from core.gListener import Alistener

WC_ANSW_HEADER = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n\r\n"
WC_ANSW_LIST_STATE_MAIN = "<ServerModules count=\"%d\">\r\n%s\r\n</Modules>\r\n"

WC_ANSW_LIST_STATE_ITEM =  "<Module number=\"%d\" name=\"%s\" caption=\"%s\">\r\n" # блок описания модуля, порядкоый номер, служебное имя, название
WC_ANSW_LIST_STATE_ITEM += "<State mess=\"%s\">%s</State>\r\n" # статус модуля 1-работает, 0-выключен, 2 - пауза, 3 - сломан
WC_ANSW_LIST_STATE_ITEM += "<Content>%s</Content>\r\n"
WC_ANSW_LIST_STATE_ITEM += "</Module>\r\n\r\n"

MODULE_ACT_STOP     = 0
MODULE_ACT_START    = 1



class TWebControl (Alistener):
    modules=None

    

class TThrWebControl (netClient):
    __DEBUG__ = False
    __LOG__  = True
    #...........................................................................
    def __init__(self, clientSock, addr, _modules):
        
        self.modules = _modules
        self.clientSock = clientSock
        self.addr = addr
        self.recvData=''
        self.recvDecodeData=[]
        self.lastBlockData = {}
        self.buffPackages=dict()
        
        self.countPackages = 0
        self.clSData = ''
        
        self.countPackages = 0
        self.ReciveBufferSize = 8196
        
        self.Worked = False
        
        netClient.__init__(self, clientSock, addr)
    #...........................................................................  
        
    def getModuleContent(self, m):
        res = ""
        sline = ""
        try:
            if m['module'].__class__.__name__=='Alistener' or m['module'].__class__.__name__ == 'TWebControl':
                sline += "\r\n<ListenIp>%s</ListenIp>\r\n" % m['module'].host
                sline += "<ListenPort>%d</ListenPort>\r\n" % m['module'].port
                sline += "<Connections count=\"%d\">\r\n</Connections>\r\n" % len(m['module'].Connections)
                          
            elif m['module'].__class__.__name__=='ThreadDataBaseSweeper':
                sline += "\r\n<TimeOut>%d</TimeOut>\r\n" % m['module'].SweepTimeOut
                sline += "<LastDataTime>%s</LastDataTime>\r\n" % str(m['module'].LastSweepDataTime)               
                sline += "<PJPageSize>%s</PJPageSize>\r\n" % str(m['module'].dbPJStats.PageSize)               
                sline += "<PJDateCreate>%s</PJDateCreate>\r\n" % str(m['module'].dbPJStats.CreationDate)               
                sline += "<PJTableObjectStatsVER>%s</PJTableObjectStatsVER>\r\n" % str(m['module'].dbPJTableObjectStats['ver'])               
                sline += "<PJTableObjectStatsREC>%s</PJTableObjectStatsREC>\r\n" % str(m['module'].dbPJTableObjectStats['rec'])               
                sline += "<SweepIsProcessing>%s</SweepIsProcessing>\r\n" % str(m['module'].SweepIsProcessing)               

            elif m['module'].__class__.__name__=='ThreadGetDBObjects':
                sline += "\r\n<TimeOut>%d</TimeOut>\r\n" % m['module'].GetTimeOut
                sline += "<LastDataTime>%s</LastDataTime>\r\n" % str(m['module'].LastGetDataTime)
                sline += "<GetCountObjects>%s</GetCountObjects>\r\n" % str(m['module'].GetCountObjects)           

            elif m['module'].__class__.__name__=='ThreadDataBaseData':
                global BufferObjects
                sline += "\r\n<Buffer len=\"%d\" writed=\"%d\"></Buffer>\r\n" % ( len(BufferObjects), m['module'].CountRecord )          
                sline += "<CountDBConnections >%d</CountDBConnections>\r\n" % m['module'].CountConnections
                sline += "<ForceSnapshotBuffer >%s</ForceSnapshotBuffer>\r\n" % str(m['module'].ForceSnapshotBuffer)
                
        except Exception as e:
            pass
        
        return sline
       
    def genModulesListStates(self):
        res = ""
        i =0
        for m in self.modules:
            
            res += WC_ANSW_LIST_STATE_ITEM % (i, m['name'], m['caption']
            , "", str( (lambda s: 'OK' if s == True else 'NO' )( m['module'].Worked)  )
            , self.getModuleContent(m)
            )
            i+=1
        return res
    #...........................................................................
    def processing (self):
        
        try:
            self.clSData = ''
            self.lastBlockData = {}
            
            if str(self.recvData).find('<ModuleAction>OFF') > 0 :
                
                self.ModuleAction(self.modules[5],0)
                
            elif str(self.recvData).find('<ModuleAction>ON') > 0 :
                self.ModuleAction(self.modules[5],1)
                
            elif str(self.recvData).find('<ForceSnapshotBuffer>True') > 0 :
                for m_ in self.modules:
                    if m_['module'].__class__.__name__ == 'ThreadDataBaseData' :
                        m_['module'].ForceSnapshotBuffer = True
                        break
                
            
            
            
            self.clSData = WC_ANSW_HEADER + WC_ANSW_LIST_STATE_MAIN %(len(self.modules), str(self.genModulesListStates()) )
 
            self.countPackages+=1

            if len(self.clSData)>0:
                try:
                    printLog (self.getName()+":Отправка данных ...", self.__LOG__, self.LogFileName, self.__DEBUG__)
                    printLog (self.getName()+":данные:[%s] - %d байт(а)" % ( str(self.clSData), len(self.clSData) ), self.__LOG__, self.LogFileName, self.__DEBUG__)
                    buff = bytes(str(self.clSData).encode('utf-8') )
                    
                    
                    if self.clientSock.sendall(buff)==None:
                        printLog (self.getName()+":отправка данных выполнена.", self.__LOG__, self.LogFileName, self.__DEBUG__)
                    else:
                        printLog (self.getName()+":Ошибка отправки данных.",self.__LOG__, self.LogFileName, self.__DEBUG__)
                    self.Worked = False
                except Exception as emess:
                    printLog (self.getName()+":Ошибка: <"+str(emess)+'>',self.__LOG__, self.LogFileName, self.__DEBUG__)
            
        except Exception as pr_ex:
            printLog (self.getName()+":Ошибка обработки данных: <"+str(pr_ex)+'>',self.__LOG__, self.LogFileName,self.__DEBUG__)

        
        
    #...........................................................................
            
    
    def ModuleAction(self, m, cmd):
        try:
            if cmd == MODULE_ACT_STOP:
                printLog (self.getName()+": Остановка модуля %s[%s] ..." % str(m['name'], str(m['module'].__class__.__name__) ), self.__LOG__, self.LogFileName, self.__DEBUG__)
                
                m['module']._Stop()
                
                while m['module'].Worked:
                    time.sleep(0.1)
                printLog (self.getName()+": Остановка модуля %s[%s] выполнена." % str(m['name'], str(m['module'].__class__.__name__) ), self.__LOG__, self.LogFileName, self.__DEBUG__)
                
            elif cmd == MODULE_ACT_START:
                printLog (self.getName()+": Запуск модуля %s[%s] ..." % str(m['name'], str(m['module'].__class__.__name__) ), self.__LOG__, self.LogFileName, self.__DEBUG__)
                m['module'].Worked = True
                time.sleep(0.1)
                m['module'].start()
                printLog (self.getName()+": Запуск модуля %s[%s] выполнен." % str(m['name'], str(m['module'].__class__.__name__) ), self.__LOG__, self.LogFileName, self.__DEBUG__)
                
                
        except Exception as ex:
            printLog (self.getName()+":Ошибка управления модулем: %s " % str(ex), self.__LOG__, self.LogFileName, self.__DEBUG__)
            printLog (self.getName()+":Ошибка управления модулем: %s " % str(ex), self.__LOG__, self.LogFileNameErrors, self.__DEBUG__)
            
    #................................................................................................................................................ 