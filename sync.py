# -*- coding: utf-8 -*-

from symbol import lambdef
import datetime
import threading


#_______________________________________________________________________
                        
                                                                
                                
from defines.gDefines   import *  
from core.gListener     import Alistener
from core.gGeneral      import printLog                         

class TDataServer():
    LogFileName = "main.log"
    LogFileNameErrors = "main_errors.log"
    modules=None
    Worked = False
    DateTimeStart = None
    __SERVER_VERSION__ = 2.3
    __SERVER_ALIAS__ = "чебурашка"
    def __init__(self):
        try:
            tpl_mess_init_module_err = "Ошибка инициализации модуля \"%s\" : %s"
            count_init_errors = 0
            self.DateTimeStart = datetime.datetime.now() 
            
            self.modules=[]
            
            
            #..................................................................................................................................
            try:
                m_name      = 'DBSync'
                m_caption   = 'Модуль репликации данных'            
                from modules.fdbSync  import TFDBSync
                self.modules.append({'module':TFDBSync(), 'name':m_name, 'caption': m_caption})
            except Exception as m_ex:
                printLog(tpl_mess_init_module_err % ( str(m_name), str(m_ex)) , True, self.LogFileNameErrors)
                count_init_errors +=1
            #..................................................................................................................................
            
            
            
            
        except Exception as e:
            printLog("Ошибка инициализации модулей [%s]." % str(e) , True, self.LogFileNameErrors, True)

    def Start(self):
        import sys
        import time
        StartingErrors = 0
        printLog("Запуск модулей .", True, self.LogFileName, True)
        for m in self.modules:
            try:
                
                m['module'].setName(m['name'])
                printLog("Запуск модуля \"%s\" ..." % m['caption'], True, self.LogFileName, True)
                m['module'].start()
                if m['module'].__class__.__name__=='ThreadGetDBObjects':
                    while m['module'].GetCountObjects==0:
                        pass
                
                
                time.sleep(0.05)
            except Exception as e:
                printLog("Ошибка запуска модуля [%s] %s." % (str(m['name']), str(e)) , True, self.LogFileNameErrors, True)
                StartingErrors+=1
        
        time.sleep(1)
        self.Worked = True
        

    def Stop(self):
        self.Worked = False

    def __del__(self):
        pass

    


DataServer = TDataServer()
DataServer.Start()

