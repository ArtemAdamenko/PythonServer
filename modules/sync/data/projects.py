# -*- coding: utf-8 -*-

sel_src_sql = """  SELECT a.ID_, a.NAME_  FROM PROJECTS a; """
                    
sel_dst_sql = """  SELECT a.ID_, a.NAME_  FROM PROJECTS a;
                               """
ins_sql = """ INSERT INTO PROJECTS (ID_, NAME_)  VALUES (%s, '%s');
                               """
del_sql = " DELETE FROM PROJECTS WHERE ID_ = %d; " 

up_sql = """ UPDATE PROJECTS SET  NAME_ = '%s' WHERE ID_ = %s; """