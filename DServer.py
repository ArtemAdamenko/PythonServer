# -*- coding: utf-8 -*-

from symbol import lambdef
import datetime
import threading
                                                                                                                       
from defines.gDefines   import *  
from core.gListener     import Alistener
from core.gGeneral      import printLog                         

class TDataServer():
    __DEBUG__ = True
    LogFileName = "main.log"
    LogFileNameErrors = "main_errors.log"
    modules=None
    Worked = False
    DateTimeStart = None
    __SERVER_VERSION__ = 2.15
    __SERVER_ALIAS__ = "чебурашка"

    def __init__(self):
        try:
            tpl_mess_init_module_err = "Ошибка инициализации модуля \"%s\" : %s"
            count_init_errors = 0
            self.DateTimeStart = datetime.datetime.now() 
            printLog("Инициализация модулей...", True, self.LogFileName, self.__DEBUG__)
            self.modules=[]                      
            #..................................................................................................................................
            try:
                m_name      = 'GetDBObjects'
                m_caption   = 'Модуль чтения списка зарегистрированных объектов'            
                from modules.dbObjects  import ThreadGetDBObjects
                self.modules.append({'module':ThreadGetDBObjects(), 'name':m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)) , True, self.LogFileNameErrors, self.__DEBUG__)
                count_init_errors +=1
            #..................................................................................................................................
            try:    
                m_name      = 'Sweep'
                m_caption   = 'Модуль сборки мусора.'
                from modules.dbSweep    import ThreadDataBaseSweeper
                self.modules.append({'module':ThreadDataBaseSweeper(), 'name':m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors, self.__DEBUG__)
                count_init_errors +=1
            #..................................................................................................................................
            try:
                m_name      = ThredDBWriteOnLineName
                m_caption   = 'Модуль обработки данных "реального времени"'
                from modules.dbOnline   import ThreadDataBasePj
                self.modules.append({'module':ThreadDataBasePj(), 'name': m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors, self.__DEBUG__ )
                count_init_errors +=1
            #..................................................................................................................................
            try:
                m_name      = ThredDBWriteBuffer
                m_caption   = 'Модуль обработки буфера данных'
                from modules.dbData     import ThreadDataBaseData
                self.modules.append({'module':ThreadDataBaseData(), 'name':m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors , self.__DEBUG__)
                count_init_errors +=1
            #..................................................................................................................................

            try:
                m_name      = 'MPS-Server'
                m_caption   = 'Модуль обработки МПС'
                self.modules.append({'module':Alistener('195.98.79.37', 8003, PKG_TYPE_MPS, 100), 'name':m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors , self.__DEBUG__)
                count_init_errors +=1
            #..................................................................................................................................
            try:
                m_name      = 'MPS-Server'
                m_caption   = 'Модуль обработки МПС2'
                self.modules.append({'module':Alistener('195.98.79.37', 8033, PKG_TYPE_MPS, 100), 'name':m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors , self.__DEBUG__)
                count_init_errors +=1
            #..................................................................................................................................
            
            
            try:
                m_name      = 'ASC-Server'
                m_caption   = 'Модуль обработки ASC'
                self.modules.append({'module':Alistener('195.98.79.37', 8333, PKG_TYPE_ASC, 999), 'name': m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors, self.__DEBUG__ )
                count_init_errors +=1
            #..................................................................................................................................
            try:
                m_name      = 'M2M-Server'
                m_caption   = 'Модуль обработки М2М'
                self.modules.append({'module':Alistener('195.98.79.37', 8000, PKG_TYPE_M2M, 5), 'name': m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors , self.__DEBUG__)
                count_init_errors +=1
            #..................................................................................................................................
            try:
                m_name      = 'AutoScan-Server'
                m_caption   = 'Модуль обработки оборудования Автоскан'
                self.modules.append({'module':Alistener('195.98.79.37', 9000, PKG_TYPE_M2M, 10), 'name': m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors , self.__DEBUG__)
                count_init_errors +=1
            #..................................................................................................................................
            try:
                m_name      = 'CDS-Server'
                m_caption   = 'Модуль обработки ЦДС'
                self.modules.append({'module':Alistener('195.98.79.37', 3070, PKG_TYPE_CDS, 2999), 'name': m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors, self.__DEBUG__ )
                count_init_errors +=1
            #..................................................................................................................................
            try:
                m_name      = 'CDS-Server'
                m_caption   = 'Модуль обработки ЦДС(Граниты)'
                self.modules.append({'module':Alistener('127.0.0.1', 3707, PKG_TYPE_CDS, 5), 'name': m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors, self.__DEBUG__ )
                count_init_errors +=1
            #..................................................................................................................................
            try:
                m_name      = 'ThredEBoardsWriteBuffer'
                m_caption   = 'Модуль обработки буфера данных для мониторов'
                from modules.dbEboards     import ThreadDataBaseEBOARDS
                self.modules.append({'module':ThreadDataBaseEBOARDS(), 'name':m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)), True, self.LogFileNameErrors, self.__DEBUG__ )
                count_init_errors +=1
            
            #..................................................................................................................................
            try:
                m_name      = 'DBSync'
                m_caption   = 'Модуль репликации данных'            
                from modules.fdbSync  import TFDBSync
                self.modules.append({'module':TFDBSync(), 'name':m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)) , True, self.LogFileNameErrors, self.__DEBUG__)
                count_init_errors +=1
            #..................................................................................................................................
            try:
                m_name      = 'WEB-Server'
                m_caption   = 'Модуль WEB-управления'
                from modules.webControl import TWebControl
                self.modules.append({'module':TWebControl('192.168.137.142', 888, PKG_TYPE_WEBCONTROL, 5), 'name': m_name, 'caption': m_caption})
                self.modules[len(self.modules) - 1]['module'].modules = self.modules
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)) , True, self.LogFileNameErrors, self.__DEBUG__)
                count_init_errors +=1
            #..................................................................................................................................
            
            
            printLog("Инициализация модулей %d выполнена, ошибок %d." %( len(self.modules),count_init_errors), True, self.LogFileName, self.__DEBUG__)
            
        except Exception as e:
            printLog("Ошибка инициализации модулей [%s]." % str(e) , True, self.LogFileNameErrors, self.__DEBUG__)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def Start(self):
        import sys
        import time
        StartingErrors = 0
        printLog("Запуск модулей .", True, self.LogFileName, self.__DEBUG__)
        for m in self.modules:
            try:
                
                m['module'].setName(m['name'])
                printLog("Запуск модуля \"%s\" ..." % m['caption'], True, self.LogFileName, self.__DEBUG__)
                m['module'].start()
                if m['module'].__class__.__name__=='ThreadGetDBObjects':
                    while m['module'].GetCountObjects==0:
                        pass
                printLog("Модуль \"%s\" запущен ." % m['caption'], True, self.LogFileName, self.__DEBUG__)
                
                time.sleep(0.05)
            except Exception as e:
                printLog("Ошибка запуска модуля [%s] %s." % (str(m['name']), str(e)) , True, self.LogFileNameErrors, self.__DEBUG__)
                StartingErrors+=1
        printLog("Запуск модулей выполнен, ошибок - %d." % StartingErrors, True, self.LogFileName, self.__DEBUG__)
        
        self.Worked = True
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def Stop(self):
        self.Worked = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __del__(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ControlModule(self,moduleIndex = None, moduleName = None, setState = False):
        try:
            mod = None
            if not moduleIndex is None:
                mod = self.modules[moduleIndex]
            elif not moduleName is None:
                for m in self.modules:
                    if m['name'] == moduleName:
                        mod = m
            if mod is None:
                raise Exception('неопределенный модуль')
            if setState == True:
                printLog("Запуск модуля %s..." % str(mod['caption']), True, self.LogFileNameErrors, self.__DEBUG__)
                mod['module'].start()
            else:            
                printLog("Остановка модуля %s..." % str(mod['caption']), True, self.LogFileNameErrors, self.__DEBUG__)
                mod['module']._Stop()
            printLog("Операция успешно выполнена." , True, self.LogFileNameErrors, self.__DEBUG__)
        except Exception as e :
            printLog("Ошибка запуска/остановки[%s] модуля: %s" % (str(setState),str(e)), True, self.LogFileNameErrors, self.__DEBUG__)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def rebootModule(self, moduleIndex = None):
        try:
            
            printLog("Операция успешно выполнена." , True, self.LogFileNameErrors, self.__DEBUG__)
        except Exception as e :
            printLog("Ошибка перезагрузки модуля: %s" % str(e), True, self.LogFileNameErrors, self.__DEBUG__)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DataServer = TDataServer()
DataServer.Start()

