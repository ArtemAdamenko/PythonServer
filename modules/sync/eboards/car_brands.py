# -*- coding: utf-8 -*-

sel_src_sql = " SELECT a.CB_ID_, a.CB_NAME_, a.CAR_TYPE_ID_ FROM CAR_BRAND a; "                    
sel_dst_sql = " SELECT a.CB_ID_, a.CB_NAME_, a.CAR_TYPE_ID_ FROM CAR_BRAND a; "                        
ins_sql     = " INSERT INTO CAR_BRAND (CB_ID_, CB_NAME_, CAR_TYPE_ID_) VALUES (%s, '%s', %s); "
del_sql     = " DELETE FROM CAR_BRAND WHERE CB_ID_ = %d; " 
up_sql      = " UPDATE CAR_BRAND SET  CB_NAME_ = '%s', CAR_TYPE_ID_ = %s WHERE CB_ID_ = %s; "