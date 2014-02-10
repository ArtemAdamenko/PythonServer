# -*- coding: utf-8 -*-
import datetime
import time

from defines.gDefines import *
from core.gGeneral import printLog

from core.gDB import AThreadDataBase

class TFDBSync(AThreadDataBase):
    #........................................................................... 
    pBaseSrcFDB = {  'host'  : '127.0.0.1'
                      , 'path'  : ''
                      , 'port'  : 3050
                      , 'login' :'sysdba'
                      , 'password':'zaUgD5Lt'
                      , 'alias' : ''  }
    pBaseDstFDB_1 = {  'host'  : '127.0.0.1'
                      , 'path'  : ''
                      , 'port'  : 3050
                      , 'login' :'sysdba'
                      , 'password':'zaUgD5Lt'
                      , 'alias' : ''  }
     
    dbSrcFDBConnect   = None
    dbDstFDBConnect_1 = None
    Worked            = False
    LogFileName       = ""
    LogFileNameErrors = ""
    LastSyncDataTime  = None
    SyncTimeOut       = 10
    
    def __init__(self):
        
        
        self.pBaseSrcFDB['path']  = 'c:%sscat%sworkbin%sdb%sprojects.fdb' % (SLASH,SLASH,SLASH,SLASH)
        self.pBaseSrcFDB['alias'] = 'PROJECTS'
        
        self.pBaseDstFDB_1['path']  = 'c:%sscat%sworkbin%sdb%sdata.fdb' % (SLASH,SLASH,SLASH,SLASH)
        self.pBaseDstFDB_1['alias'] = 'DATA'
        
        AThreadDataBase.__init__(self)
        
        
        
    #____________________________________________________________________________________________________     

        
    def run(self):
        
        self.LogFileName        = 'DataBase%s%s%sWork.log' % (SLASH,self.getName(),SLASH)
        self.LogFileNameErrors  = 'DataBase%s%s%sErrors.log' % (SLASH,self.getName(),SLASH)
        
        self.Worked = True
        
        while self.Worked:
            self.syncObject()
            
            
            time.sleep(self.SyncTimeOut)
    #____________________________________________________________________________________________________     
    
    def syncObject(self):
        
        printLog(self.getName() +':Репликация списка перевозчиков...' , True , self.LogFileName, True)
        from modules.sync import projects
        self.syncForData(projects.sel_src_sql, projects.sel_dst_sql , projects.del_sql, projects.ins_sql, projects.up_sql)
        printLog(self.getName() +':Репликация списка перевозчиков выполнена.' , True , self.LogFileName, True)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        printLog(self.getName() +':Репликация списка планов...' , True , self.LogFileName, True)
        from modules.sync import plans
        self.syncForData(plans.sel_src_sql, plans.sel_dst_sql , plans.del_sql, plans.ins_sql, plans.up_sql)
        printLog(self.getName() +':Репликация списка планов выполнена.' , True , self.LogFileName, True)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        printLog(self.getName() +':Репликация списка объектов...' , True , self.LogFileName, True)
        from modules.sync import objects
        self.syncForData(objects.sel_src_sql, objects.sel_dst_sql , objects.del_sql, objects.ins_sql, objects.up_sql)
        printLog(self.getName() +':Репликация списка объектов выполнена.' , True , self.LogFileName, True)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    #____________________________________________________________________________________________________   
    def syncForData(self, sel_src_sql, sel_dst_sql , del_sql, ins_sql, up_sql):
        src_objs = [] 
        dst_objs = []
        upd_objs = []
        ins_objs = []
        del_objs = []
        rec_deleted = 0
        rec_inserted = 0
        rec_updated = 0
        # step 0 ........
        # получаем список объектов из базы projects
        printLog(self.getName() +':Получение эталонных записей...' , True , self.LogFileName, False)
        self.dbConnect == None
        self.pBase['path']  = self.pBaseSrcFDB['path']
        self.pBase['alias'] = self.pBaseSrcFDB['alias']
        src_objs = []
        self.ExecQuery(sel_src_sql , True , src_objs )
        self.DataBaseDisconnect()

        printLog(self.getName() +':Получено %d записей.' % ( len(src_objs)), True , self.LogFileName, False)
        
        # step 1 ........
        #  получаем список объектов из базы data
        printLog(self.getName() +':Получение списка-назначения...' , True , self.LogFileName, False)
        self.dbConnect == None
        self.pBase['path']  = self.pBaseDstFDB_1['path']
        self.pBase['alias'] = self.pBaseDstFDB_1['alias']
        dst_objs = []
        self.ExecQuery(sel_dst_sql, True, dst_objs)
        self.DataBaseDisconnect()
        
        printLog(self.getName() +':Получено %d записей.' % ( len(dst_objs)), True , self.LogFileName, False)
        
        # step 2 ........       
        # сравниваем два списка
        
        #ищем записи которые нужно удалить
        try:
            del_objs = []
            printLog(self.getName() +':Определение записей для удаления...' , True , self.LogFileName, False)
            for d in dst_objs:
                rec_ecxist = False
                for s in src_objs:
                    if d[0] == s[0]:
                        rec_ecxist = True
                        break
                        
                if not rec_ecxist:
                    del_objs.append(d)
                            
                
            printLog(self.getName() +':Записей для удаления: %d ' % ( len(del_objs)), True , self.LogFileName, False)
            
            if len(del_objs) > 0:        
                printLog(self.getName() +':Удаление записей ...' , True , self.LogFileName, False)
                
                for i in del_objs:
                    if self.ExecQuery( del_sql % i[0]):
                        rec_deleted += 1
            
                
        except Exception as e:
            printLog(self.getName() +':Ошибка удаления записей: %s ' % ( str(e)), True , self.LogFileName, False)
        
        #ищем записи которые нужно добавить
        try:
            ins_objs = []
            printLog(self.getName() +':Определение записей для добавления...' , True , self.LogFileName, False)
            for s in src_objs:
                rec_ecxist = False
                for d in dst_objs:
                    if d[0] == s[0]:
                        rec_ecxist = True
                        break
                        
                if not rec_ecxist:
                    ins_objs.append(s)
                            
                
            printLog(self.getName() +':Записей для добавления: %d ' % ( len(ins_objs)), True , self.LogFileName, False)
            
            if len(ins_objs) > 0:
                printLog(self.getName() +':Добавление записей ...' , True , self.LogFileName, False)
                
                for i in ins_objs:
                      
                    u = []
                    for x in i:
                        if type(x) == datetime.datetime:
                            u.append("'%s'" %str( (lambda s:  str(s)[:str(s).find('.')] if str(s).find('.') >0 else str(s) )(x) ))
                        elif x is None:
                            u.append(str( (lambda s: 'null' if s is None else s )(x) ))
                        else:
                            u.append(str(x))
                            
                            
                    sep = '%s'
                    n = 0
                    sql = ins_sql
                    while ( sql.find(sep) > 0) :
                        sql = sql[:sql.find(sep)] + str(u[n]) + sql[sql.find(sep) + len(sep):]
                        n +=1
                    
                    
                    if self.ExecQuery(sql, False, None):
                        rec_inserted += 1
                
                
                
        except Exception as e:
            printLog(self.getName() +':Ошибка добавления записей: %s ' % ( str(e)), True , self.LogFileName, False)
            
        #ищем записи которые нужно обновить
        try:
            upd_objs = []
            printLog(self.getName() +':Определение записей для обновления...' , True , self.LogFileName, False)
            for s in src_objs:
                rec_isup = False
                for d in dst_objs:
                    if d[0] == s[0]:
                        for i in range(1,len(s)):
                            if not (d[i] == s[i]):
                                #printLog(str(d[i]) + ' <============>' + str(s[i]), True , self.LogFileName, False)
                                rec_isup = True
                                break
                        break
                if rec_isup:
                    upd_objs.append(s)
            
            printLog(self.getName() +':Записей для обновления: %d ' % ( len(upd_objs)), True , self.LogFileName, False)
            
            
            if len(upd_objs) > 0:
                printLog(self.getName() +':Обновление записей ...' , True , self.LogFileName, False)
                
                for i in upd_objs:
                    printLog(str(i), True , self.LogFileName, False)
                    u = []
                    for x in i:
                        if type(x) == datetime.datetime:
                            u.append("'%s'" %  str( (lambda s:  str(s)[:str(s).find('.')] if str(s).find('.') >0 else str(s) )(x) ))
                        elif x is None:
                            u.append(str( (lambda s: 'null' if s is None else s )(x) ))
                        else:
                            u.append(str(x))
                            
                    printLog(str(u), True , self.LogFileName, False)        
                    

                    
                    sep = '%s'
                    n = 1
                    sql = up_sql
                    while ( sql.find(sep) > 0) :
                        if n == len(u):
                            n = 0
                        sql = sql[:sql.find(sep)] + str(u[n]) + sql[sql.find(sep) + len(sep):]
                        n +=1
                    printLog(str(sql), True , self.LogFileName, False)  
                    
                    if self.ExecQuery( sql , False, None):
                        rec_updated += 1
                
                
            
        except Exception as e:
            printLog(self.getName() +':Ошибка обновления записей: %s ' % ( str(e)), True , self.LogFileName, False)
            
        src_objs = [] 
        dst_objs = []
        self.DataBaseDisconnect()
        printLog(self.getName() +':Добавлено: %d Удалено: %d Обновлено: %d.' % ( rec_inserted, rec_deleted, rec_updated), True , self.LogFileName, True)
    #____________________________________________________________________________________________________ 
        
#------------------------------------------------------------------------------#
