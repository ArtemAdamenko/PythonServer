# -*- coding: utf-8 -*-

sel_src_sql = " SELECT a.NUMBER_, a.NAME_, a.LON_, a.LAT_, a.TIME_, a.ROUT_, a.CONTROL_ FROM BUS_STATIONS a; "
                    
sel_dst_sql = " SELECT a.NUMBER_, a.NAME_, a.LON_, a.LAT_, a.TIME_, a.ROUT_, a.CONTROL_ FROM BUS_STATIONS a; "
ins_sql     = " INSERT INTO BUS_STATIONS (NUMBER_, NAME_, LON_, LAT_, TIME_, ROUT_, CONTROL_) VALUES (%s, '%s', %s , %s, %s, %s, %s);"
del_sql     = " DELETE FROM BUS_STATIONS WHERE IDS_ = %d; " 
up_sql = """ UPDATE OBJECTS  
                        SET 
                         NAME_ = '%s'
                        , OBJ_ID_ = %s
                        , PROJ_ID_ = %s
                        , LAST_TIME_ = %s
                        , LAST_LON_ = %s
                        , LAST_LAT_ = %s
                        , LAST_SPEED_ = %s
                        , LAST_STATION_ = %s
                        , LAST_STATION_TIME_ = %s
                        , LAST_ROUT_ = %s
                        , CAR_BRAND_ = %s
                     
                     WHERE IDS_ = %s;
                               """