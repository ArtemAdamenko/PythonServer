# -*- coding: utf-8 -*-
__DEBUG__ = False
__LOG__  = True
#------------------------------------------------------#
from core.nClient import netClient
from defines.pkgDefines import *
from core.gGeneral import printLog
from defines.gDefines import *
from modules.dbOnline import ThreadDataBasePj
from modules.dbData import ThreadDataBaseData
#------------------------------------------------------#
class talkToClientM2M (netClient):
    #...........................................................................
    def __init__(self, clientSock, addr, _M2M_PARSE_TIME_MASK):
        self.M2M_PARSE_TIME_MASK = _M2M_PARSE_TIME_MASK
        self.clientSock = clientSock
        self.addr = addr
        self.AnswerPkgType = PKG_UNKNOWN
        self.clSData = ''
        self.recvData=''
        self.lastBlockData = {}
        self.countPackages = 0
        self.ReciveBufferSize =  M2M_RECIVE__BUFFER_SIZE

        netClient.__init__(self, clientSock, addr)
    #...........................................................................    
    
    
    #...........................................................................    
    def processing (self):
        try:
            self.clSData = ''
            self.lastBlockData = {}
            

            self.AnswerPkgType = self.IdentPackageType(self.recvData)

            if self.AnswerPkgType != PKG_UNKNOWN:
                if self.AnswerPkgType == PKG_PUT_COORD:
                    self.lastBlockData = self.parsinPackage(self.recvData)
                    self.appnedBlockToBuffers()
                    self.countPackages+=1
                    self.clSData = self.getPackageAnswer(TemplatePackageAnswer[self.AnswerPkgType], self.lastBlockData['BLOCK_NUMBER'])

                if len(self.clSData)>0:
                    try:
                        printLog (self.getName()+":Отправка данных ...", __LOG__, self.LogFileName, __DEBUG__)
                        buff = bytes(str(self.clSData).encode('utf-8') )
                        printLog(buff, __LOG__, self.LogFileName)
                        if self.clientSock.sendall(buff)==None:
                            printLog (self.getName()+":отправка данных выполнена.", __LOG__, self.LogFileName, __DEBUG__)
                        else:
                            printLog (self.getName()+":Ошибка отправки данных.",__LOG__, self.LogFileName, __DEBUG__)
                            printLog (self.getName()+":Ошибка отправки данных.",__LOG__, self.LogFileNameErrors, __DEBUG__)
                            self.Worked = False
                    except Exception as emess:
                        printLog (self.getName()+":Ошибка: <"+str(emess)+'>',__LOG__, self.LogFileName, __DEBUG__)
                        printLog (self.getName()+":Ошибка: <"+str(emess)+'>',__LOG__, self.LogFileNameErrors, __DEBUG__)
            
        except Exception as pr_ex:
            printLog (self.getName()+":Ошибка обработки данных: <"+str(pr_ex)+'>',__LOG__, self.LogFileName, __DEBUG__)
            printLog (self.getName()+":Ошибка обработки данных: <"+str(pr_ex)+'>',__LOG__, self.LogFileNameErrors, __DEBUG__)

                
                    
            
        
        
        
    #...........................................................................
    def parsinPackage(self, data):
        res = {}
        data=str(data)
        sStart = '<Coord'
        sEnd = '/>'
        res['VALID'] = True
        s = data[data.find(sStart)+len(sStart):]
        s = s[:s.find(sEnd)]
        s = s.split()

        try:
            res['BLOCK_NUMBER']=self.getObjectIdFromPackage(data)
        except Exception as emess:
            printLog(self.getName()+':Ошибка разборки пакета:'+str(emess), True, self.LogFileName)
            printLog(self.getName()+':Ошибка разборки пакета:'+str(emess), True, self.LogFileNameErrors)
            res['BLOCK_NUMBER']=-1
            res['VALID'] = False
            
        
        for i in s:
            a=i.replace('"', '').split('=')
            if a[0].upper() == 'TIME':
                try:
                    tt = time.strptime(a[1], self.M2M_PARSE_TIME_MASK)
                    tt_hour = tt.tm_hour + PKG_M2M_HOURS_INC
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
                    
                    res[a[0].upper()] = '%s.%s.%d %s:%s:%s'% (str(tt_day).rjust(2,"0")
                                                           ,str(tt_mount).rjust(2,"0")
                                                           , tt_year
                                                           , str(tt_hour).rjust(2,"0")
                                                           , str(tt.tm_min).rjust(2,"0")
                                                           , str(tt.tm_sec).rjust(2,"0")
                                                           )
                    
                except Exception as e:
                    printLog(self.getName()+":Ошибка определения времени в пакете:"+str(e), True, self.LogFileName)
                    printLog(self.getName()+":Ошибка определения времени в пакете:"+str(e), True, self.LogFileNameErrors)
                    res['VALID']=False
                    
                    
            else:
                res[a[0].upper()]=a[1]
                if a[0].upper() == 'SPEED':
                    try:
                        res[a[0].upper()] = float(a[1])
                    except Exception as e:
                        res[a[0].upper()] = 0.0
                        printLog(self.getName()+":Ошибка определения скорости в пакете:"+str(e), True, self.LogFileName)
                        printLog(self.getName()+":Ошибка определения скорости в пакете:"+str(e), True, self.LogFileNameErrors)
                        
                        
                if (a[0].upper() == 'LON') or (a[0].upper() == 'LAT'):
                    try:
                        res[a[0].upper()] = int(a[1][:a[1].find('.')])*100 + float('0.'+a[1][a[1].find('.')+1:])*60
                    except Exception as e:
                        res[a[0].upper()] = 0.0
                        printLog(self.getName()+":Ошибка определения координат в пакете:"+str(e), True, self.LogFileName)
                        printLog(self.getName()+":Входные данные = \"%s\"" % str(a), True, self.LogFileName)
                        printLog(self.getName()+":Ошибка определения координат в пакете:"+str(e), True, self.LogFileNameErrors)
                        printLog(self.getName()+":Входные данные = \"%s\"" % str(a), True, self.LogFileNameErrors)
                        
                        res['VALID']=False
        return res
    def IdentPackageType(self, data):
        pkgType = PKG_UNKNOWN

        try:
            if str(data).find('PutCoord') > 0:
                pkgType = PKG_PUT_COORD

            if str(data).find('PutMessage') > 0:
                pkgType = PKG_PUT_MESSAGE

            if str(data).find('PutMsgAnswer') > 0:
                pkgType = PKG_PUT_MSG_ANSWER

        except Exception as e:
            printLog (self.getName()+":Ошибка определения типа пакета:" + str(e), True, self.LogFileName)
            printLog (self.getName()+":Ошибка определения типа пакета:" + str(e), True, self.LogFileNameErrors)
            pkgType = PKG_UNKNOWN

        if pkgType == PKG_UNKNOWN:
            pass

        return pkgType

    #...........................................................................
    def getObjectIdFromPackage(self, _Str):
        sStart = '<ObjectID>'
        sEnd   = '</ObjectID>'
        _Str=str(_Str)
        oid = _Str[_Str.find(sStart)+len(sStart):_Str.find(sEnd)]
        return oid
    #...........................................................................    
    def getMessageIdFromPackage(self, Str):
        sStart = '<MessageID>'
        sEnd   = '</MessageID>'
        oid = Str[Str.find(sStart)+len(sStart):Str.find(sEnd)]
        return oid
    #...........................................................................    
    def getImputPackageContent(self, str):
        sStart = '</ObjectID>'
        sEnd   = '</ws:PutCoord>'
        res = str[ str.find(sStart)+len(sStart)+1: str.find(sEnd)-1 ]
        return res

    #...........................................................................
    def getPackageAnswer(self, TemplatePackage, ObjectId):
        _data = TemplatePackage % ObjectId       
        _answer  = AnswerHeader    
        _answer += "Content-Length: "+str(len(_data))+"\r\n"
        _answer += "Cache-Control: no-cache\r\n\r\n"
        _answer += _data
        return _answer
        
    #...........................................................................
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
                            
                            
                            
                            
                            for o in DBObjectsList:
                                if o.BlockNumber:
                                    if o.BlockNumber == int(rec['BLOCK_NUMBER']):
                                        printLog(self.getName()+':Добавление блока %s в буффер: LON: %s LAT: %s SPEED: %s'  % (str(rec['BLOCK_NUMBER']), str(rec['LON']), str(rec['LAT']), str(rec['SPEED'])),True,self.LogFileName, False)
                                        
                                        #o.Update(rec['TIME'], rec['LON'], rec['LAT'] , rec['SPEED'])        
                                        o.Update(rec['TIME'], rec['LAT'], rec['LON'] , rec['SPEED']) # lon и lat наоборот потому что в пакете все как обычно через жопу, бля!
                                        
                                        BufferObjects.append(o)
                                        
                            #________________________________________________________________________
                            
        except Exception as emess:
            printLog(self.getName()+':Ошибка занесения данных в буфер:' + str(emess),True,self.LogFileName, False)
            printLog(self.getName()+':Ошибка занесения данных в буфер:' + str(emess),True,self.LogFileNameErrors, False)
    #...........................................................................

    
#------------------------------------------------------------------------------------------------- 
