# -*- coding: utf-8 -*-


# типы принимаемых пакетов --------------------------------------------------------------------------------------- #
PKG_TYPE_M2M = 800  # формат М2м-телематики
PKG_TYPE_MPS = 803  # формат МПС

PKG_TYPE_CDS = 700  # формат МПС
PKG_TYPE_ASC = 900  # формат МПС
PKG_TYPE_WEBCONTROL = 400  # формат веб-формы управления

         
# маски преобраования времения из полученного пакета  ------------------------------------------------------------ #
PKG_M2M_PARSE_TIME_MASK = "%Y-%m-%dT%H:%M:%SZ"  # маска для пакетов от М2М-телематики
PKG_MPS_PARSE_TIME_MASK = "%Y-%m-%dT%H:%M:%S"   # маска для пакетов от МПС
PKG_M2M_HOURS_INC       = 4                     # шаг увеличения времени в пакете М2М

PKG_CDS_PARSE_TIME_MASK = "%d.%m.%Y %H:%M:%S"   # маска для пакетов от ЦДС
PKG_CDS_HOURS_INC       = 4                     # шаг увеличения времени в паекете ЦДС

# выделение типа блока ------------------------------------------------------------------------------------------- #
PKG_IDENT_TYPE_BLOCK_LEN = 3                    # количество символов в номере принимаемого объета
                                                # ,отвечающих за тип блока

# системные параметры -------------------------------------------------------------------------------------------- #
import sys
if sys.platform=='win32':SLASH = "\\"           # разделитель каталогов дял win
else:SLASH = "/"                                # разделитель каталогов для других ос 
LOG_DIR = "logs"                                # каталог для логов
M2M_RECIVE__BUFFER_SIZE     = 1536              # размер принимаемого буфера для протокола М2М - 100 Mb = 104857600

CDS_RECIVE__BUFFER_SIZE     = 1024              # размер принимаемого буфера для протокола ЦДС - 1Mb = 1048576
CDS_PKG_SIZE_TYPE_1         = 26                # размер пакета 1-го типа для протокла ЦДС
CDS_PKG_SIZE_TYPE_2         = 38                # размер пакета 2-го типа для протокла ЦДС

ASC_RECIVE__BUFFER_SIZE     = 1024              # размер принимаемого буфера для протокола ASC - 6 - 1Mb = 1048576
ASC_PKG_SIZE_TYPE_6         = 66                # размер пакета ASC - 6



# названия потоков ----------------------------------------------------------------------------------------------- #
ThredDBWriteOnLineName  = 'DBWriteOnLine'       # имя потока для записи ON-LINE данных в базу PROJECTS
ThredDBWriteBuffer      = 'DBWriteBuffer'       # имя потока для записи буфера данных в базу DATA
ThredGetDBObjects       = 'GetDBObjects'        # имя потока получения списка зарегистрированых в базе объектов
ThredDBSweeper          = 'DBSweeper'           # имя потока сборки мусора
ThredConnection         = 'CNT_%s_%d'           # имя потока входящего подключения


# буфера данных -------------------------------------------------------------------------------------------------- #
global DBObjectsList                            # список зарегистрированных в базе объектов
DBObjectsList=[]
global BufferObjects                            # буфер данных
BufferObjects=[]

global TGeoCoors
global TObject
global TRouteControl
global mainForm


class TGeoCoors():         # класс для описания координат
    LON = None                     # широта
    LAT = None                     # долгота
    def __init__(self, _lon = 0.0, _lat = 0.0):
        self.LON = _lon
        self.LAT = _lat

class TRouteControl():    # класс описания движения тс по маршруту  
    LastRoute               = None # маршрут
    LastStation             = None # Последняя остановка
    LastStationTime         = None # Время прохождения последней остановки
    PrevStation             = None # Предыдущая остановка
    PrevStationTime         = None # Время прохождения предыдущей остановки
    RouteLastTimeUpdate     = None # Последнее время обновления сведений о движении по маршруту
    RoutePrevTimeUpdate     = None # Предыдущее время обновления сведений о движении по маршруту
    
class TObject():           # класс для описания объекта
    Ids                     = None # ids
    Oid                     = None # код объекта
    Pid                     = None # код проекта
    Phone                   = None # номер телефона
    BlockNumber             = None # номер блока, если данных нет то -1
    BlockType               = None # тип блока, если данных нет то -1
    Speed                   = None # последняя скорость движения
    LastPoint               = None # последняя точка
    LastTime                = None # последенее время из пакета
    LastReciveTime          = None # время последнего обновления состояния объекта
    PrevReciveTime          = None # время предыдущего обновления состояния объекта
    isDB                    = True # наличие в базе(нужно только для удаления из буфера объектов удаленных из базы)
    CountRecivedPackaged    = 0    # количество полученных пакетов данных для объекта
    Route                   = None # Параметры движения по маршруту
    Provider                = None # Код устновщика
    
    def __init__(self,ids_,oid_,pid_,phone_,blocknumber_,blocktype_,_provider = None):
        self.Ids            = ids_
        self.Oid            = oid_
        self.Pid            = pid_
        self.Phone          = phone_
        self.BlockNumber    = blocknumber_
        self.BlockType      = blocktype_
        self.LastPoint      = TGeoCoors()
        self.Route          = None
        self.Provider       = _provider

    def Update(self, _LastTime = None, _LastLon = None, _LastLat = None, _LastSpeed = None):      
        try:
            import time
            import datetime
            
            _lt = None
            if  _LastTime == None:
                raise Exception ("Получена пустая дата-время")
            _lt = time.strptime(_LastTime, PKG_CDS_PARSE_TIME_MASK)
            
            to_up = (self.LastTime == None)
            if not to_up:
                
                _slt = time.strptime(self.LastTime, PKG_CDS_PARSE_TIME_MASK) 
                to_up = (_lt > _slt)
                
            if to_up:
                
                self.LastTime = _LastTime
                self.LastPoint.LON = _LastLon
                self.LastPoint.LAT = _LastLat
                self.Speed = _LastSpeed
                self.CountRecivedPackaged+=1
                self.PrevReciveTime=self.LastReciveTime
                self.LastReciveTime=datetime.datetime.now()
              
        except Exception as e:
            #print ("Ошибка обновления объекта:"+str(e))
            pass
        
        
    def UpdateRoute(self, routeId_, stationId_, stationTime_, _prevStationId, _prevStationTime):
        try:
            import datetime
            import time
            if self.Route == None:self.Route=TRouteControl()
            self.Route.LastRoute            = routeId_
            self.Route.LastStation          = stationId_
            self.Route.LastStationTime      = stationTime_
            self.Route.PrevStation          = _prevStationId
            self.Route.PrevStationTime      = _prevStationTime
            self.Route.RoutePrevTimeUpdate  = self.Route.RouteLastTimeUpdate
            self.Route.RouteLastTimeUpdate  = datetime.datetime.now()
        except Exception as e:
            #print ("Ошибка обновления сведений о маршруте:"+str(e))
            pass