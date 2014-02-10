# -*- coding: utf-8 -*-

global __STATDEBUG__
__STATDEBUG__ = False

def thisloaded():
    import sys
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s", ["stat"])
    except getopt.error as msg:
        print (msg)
        print ("""Для получения статистики запускать нужно с ключом -s или -stat""")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-s", "--stat"):
            global __STATDEBUG__
            __STATDEBUG__ = True
           
            #sys.exit(0)
    # process arguments
   
thisloaded()

class TFDBStatistic():
    params = None
    path    = "\"c:\\Program Files\\Firebird\\Firebird_2_5\\bin\\gstat.exe\""
    PageSize = None
    CreationDate = None
    PageSize = None
    PageSize = None
    StatData = None
    CmdPath = None
    DBFileName = None
    #---------
    def __init__(self, dbPath):
        import os
        self.DBFileName = os.path.basename(dbPath)
        self.params = " -a -r -z -i %s -user SYSDBA -pass zaUgD5Lt" % dbPath
        self.CmdPath = self.path + self.params
    #---------
    def getStat(self):
        self.loadStat()
        self.PageSize = self.getParam(str(self.StatData), "Page size")
        self.CreationDate = self.getParam(str(self.StatData), "Creation date")
    #---------
    def loadStat(self):
        if self.CmdPath:
            import subprocess
            p = subprocess.Popen(self.CmdPath, shell = True, stdin =  subprocess.PIPE, stdout = subprocess.PIPE, stderr =  subprocess.PIPE)
            self.StatData = str(p.communicate()[0])           
    #---------
    def getParam(self, dataIn, paramName, endLParam = None):
        res = None
        if (not dataIn is None) and (not paramName is None) :
            try:
                res = dataIn.split('\\r\\n')
                for r in res:
                    if r.find(paramName)>-1:
                        res = r[r.find(paramName)+len(paramName):]       
                        break
                res = res.replace('\\t','')
                res = res.replace(' ','')
                if not endLParam is None:
                    if res.find(endLParam) > 0:
                        res = res[:res.find(',')]
            except Exception as e:                
                res = None
        return res
    #---------
    def getTableInfo(self, tableName):
        result = {'name':None, 'ver':None, 'rec':None}
        res = self.StatData[self.StatData.find("Analyzing database pages"):]
        res = res.split('\\r\\n\\r\\n')
        result['name'] = tableName
        zzz = None
        for r in res:          
            if r.find(tableName) == 0:               
                result['ver'] =self.getParam(r,'total versions:',',')
                result['rec'] =self.getParam(r,'total records:',',')              
        return result    
    #---------        

if __STATDEBUG__:
    print ('-'*100)    
    FDBStatistic = TFDBStatistic("c:\\SCAT\\WORKBIN\\DB\\EBOARDS.FDB")
    FDBStatistic.getStat()

    print ("Статистика для базы \"%s\" :" % str(FDBStatistic.DBFileName))
    print ("Размер страницы:"+str(FDBStatistic.PageSize))
    print ("Дата/время создания БД:"+str(FDBStatistic.CreationDate))
    print(FDBStatistic.getTableInfo('OBJECTS' ))
    print(FDBStatistic.getTableInfo('BASEDATA' ))

    print ('-'*100)    
    FDBStatistic = TFDBStatistic("c:\\SCAT\\WORKBIN\\DB\\PROJECTS.FDB")
    FDBStatistic.getStat()

    print ("Статистика для базы \"%s\" :" % str(FDBStatistic.DBFileName))
    print ("Размер страницы:"+str(FDBStatistic.PageSize))
    print ("Дата/время создания БД:"+str(FDBStatistic.CreationDate))
    print(FDBStatistic.getTableInfo('OBJECTS' ))

    print ('-'*100)    