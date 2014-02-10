# -*- coding: utf-8 -*-
__DEBUG__ = False
#------------------------------------------------------------------------------#
import os
import datetime
from defines.gDefines import *
#------------------------------------------------------------------------------#
def printLog (aString, OutToLogFile = False, LogFileName=None, DisplayPrint=__DEBUG__):
    
    aString = str(datetime.datetime.now()) + '#' + str(aString).rjust(80,'.')
    if DisplayPrint:
        print (aString)
        #pass
    if OutToLogFile and LogFileName:
        Logging(aString,LogFileName)
        
#------------------------------------------------------------------------------#
def Logging(mess, logFileName, endL = '\n'):
    
    aString = str(datetime.datetime.now()) + '#' + str(mess) + endL
    log_file_name = ""
    log_dir = str(datetime.datetime.now())
    log_dir = log_dir[8:10]+log_dir[5:7]+log_dir[:4]
    log_dir = os.getcwd() + SLASH+LOG_DIR + SLASH + log_dir
    
    if logFileName.find(SLASH) > -1:
        
        s = logFileName
        s = s.split(SLASH)
        
        logFileName = s[len(s)-1]
        s.pop()
        for i in s:
            try:
                log_dir = log_dir + SLASH + str(i)
                if not os.path.exists(log_dir):
                    printLog('Создание  каталога для логов:'+log_dir, False, None, __DEBUG__)
                    os.mkdir(log_dir )               
            except Exception as e:
                printLog('Ошибка создания каталога для логов: '+ str(e), False, None, __DEBUG__)
        
        printLog('Файл лога:'+logFileName, False, None, __DEBUG__)    
    
    if not os.path.exists(log_dir):
        printLog('Создание  каталога для логов:'+log_dir, False, None, __DEBUG__)
        try:
            os.mkdir(log_dir )
        except Exception as e:
            printLog('Ошибка создания каталога для логов: '+ str(e), False, None, __DEBUG__)
            
    if logFileName.find("_conn__") > 0:
        log_dir = log_dir + SLASH + 'connections'
        logFileName = logFileName[logFileName.find('_conn__')+len('_conn__'):]
        if not os.path.exists(log_dir):
            printLog('Создание  каталога для логов подключений:'+log_dir, False, None, __DEBUG__)
            try:
                os.mkdir(log_dir )
            except Exception as e:
                printLog('Ошибка создания каталога для логов: '+ str(e), False, None, __DEBUG__)
        
    log_file_name =  log_dir + SLASH + logFileName
    printLog('Файл лога:'+log_file_name, False, None, False)
    try:
        if os.path.exists(log_file_name):
            f = open( log_file_name, 'a' )
        else:
            f = open(log_file_name, 'w' )
        f.write( str(aString) )
        f.close()
    except IOError as  strerror:
        printLog('*'*50, False, None, __DEBUG__)
        printLog ("Ошибка ввода/вывода: "+str(strerror), False, None, __DEBUG__)
        printLog('*'*50, False, None, __DEBUG__)     
#------------------------------------------------------------------------------#




