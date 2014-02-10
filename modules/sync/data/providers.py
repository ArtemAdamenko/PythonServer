# -*- coding: utf-8 -*-

sel_src_sql = " SELECT a.ID_, a.NAME_ FROM PROVIDERS a ORDER BY a.id_ asc;"
                    
sel_dst_sql = "SELECT a.ID_, a.NAME_ FROM PROVIDERS a ORDER BY a.id_ asc;"

ins_sql = " INSERT INTO PROVIDERS (ID_, NAME_)  VALUES (%s, '%s')"
del_sql = " DELETE FROM PROVIDERS WHERE ID_ = %d; " 
up_sql = " UPDATE PROVIDERS SET NAME_ = '%s'  WHERE ID_ = %s;"