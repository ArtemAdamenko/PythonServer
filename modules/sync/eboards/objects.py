# -*- coding: utf-8 -*-

sel_src_sql = " SELECT a.IDS_, a.NAME_, a.LAST_TIME_, a.LAST_LON_, a.LAST_LAT_, a.LAST_SPEED_, a.LAST_STATION_, a.LAST_STATION_TIME_, a.LAST_ROUT_, a.CAR_BRAND_ FROM OBJECTS a; "                    
sel_dst_sql = " SELECT a.IDS_, a.NAME_, a.LAST_TIME_, a.LAST_LON_, a.LAST_LAT_, a.LAST_SPEED_, a.LAST_STATION_, a.LAST_STATION_TIME_, a.LAST_ROUT_, a.CAR_BRAND_ FROM OBJECTS a;  "                        
ins_sql     = """ INSERT INTO OBJECTS (IDS_, NAME_, LAST_TIME_, LAST_LON_, LAST_LAT_, LAST_SPEED_, LAST_STATION_, LAST_STATION_TIME_, LAST_ROUT_, CAR_BRAND_)
                    VALUES (%s, '%s', %s, %s, %s, %s, %s, %s, %s, %s); """
del_sql     = " DELETE FROM OBJECTS WHERE IDS_ = %d; " 
up_sql      = """ UPDATE OBJECTS SET  
    NAME_ = '%s'
    , LAST_TIME_ = %s
    , LAST_LON_ = %s
    , LAST_LAT_ = %s
    , LAST_SPEED_ = %s
    , LAST_STATION_ = %s
    , LAST_STATION_TIME_ = %s
    , LAST_ROUT_ = %s
    , CAR_BRAND_ = %s
 WHERE IDS_ = %s; """