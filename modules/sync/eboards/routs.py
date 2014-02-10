# -*- coding: utf-8 -*-

sel_src_sql = " SELECT ID_, NAME_, ROUTE_ACTIVE_ FROM ROUTS; "                    
sel_dst_sql = " SELECT ID_, NAME_, ROUTE_ACTIVE_ FROM ROUTS; "                        
ins_sql     = " INSERT INTO ROUTS (ID_, NAME_, ROUTE_ACTIVE_) VALUES (%s, '%s', %s); "
del_sql     = " DELETE FROM ROUTS WHERE ID_ = %d; " 
up_sql      = " UPDATE ROUTS SET  NAME_ = '%s', ROUTE_ACTIVE_ = %s WHERE ID_ = %s; "