# -*- coding: utf-8 -*-

sel_src_sql = " SELECT a.CT_ID_, a.NAME_, a.SHORT_NAME_ FROM CAR_TYPE_ a; "                    
sel_dst_sql = " SELECT a.CT_ID_, a.NAME_, a.SHORT_NAME_ FROM CAR_TYPE_ a; "                        
ins_sql     = " INSERT INTO CAR_TYPE_ (CT_ID_, NAME_, SHORT_NAME_) VALUES (%s, '%s', '%s'); "
del_sql     = " DELETE FROM CAR_TYPE_ WHERE CT_ID_ = %d; " 
up_sql      = " UPDATE CAR_TYPE_ SET  NAME_ = '%s', SHORT_NAME_ = '%s' WHERE CT_ID_ = %s; "