# -*- coding: utf-8 -*-

sel_src_sql = """  SELECT 
                            a.ID_
                            , a.NAME_
                            , a.TYPE1_PLANNED_
                            , a.TYPE2_PLANNED_
                            , a.TYPE3_PLANNED_
                            , a.TYPE4_PLANNED_
                            , a.RACE1_PLANNED_
                            , a.RACE2_PLANNED_
                            , a.RACE3_PLANNED_
                            , a.RACE4_PLANNED_
                            , a.TYPE1_PLANNED_HOL_
                            , a.TYPE2_PLANNED_HOL_
                            , a.TYPE3_PLANNED_HOL_
                            , a.TYPE4_PLANNED_HOL_
                            , a.RACE1_PLANNED_HOL_
                            , a.RACE2_PLANNED_HOL_
                            , a.RACE3_PLANNED_HOL_
                            , a.RACE4_PLANNED_HOL_
                            , a.TYPE5_PLANNED_
                            , a.TYPE6_PLANNED_
                            , a.RACE5_PLANNED_
                            , a.RACE6_PLANNED_
                            , a.TYPE5_PLANNED_HOL_
                            , a.TYPE6_PLANNED_HOL_
                            , a.RACE5_PLANNED_HOL_
                            , a.RACE6_PLANNED_HOL_
                            , a.ROUTE_ACTIVE_
                        FROM ROUTS a; """
                    
sel_dst_sql = """  SELECT 
                            a.ID_
                            , a.NAME_
                            , a.TYPE1_PLANNED_
                            , a.TYPE2_PLANNED_
                            , a.TYPE3_PLANNED_
                            , a.TYPE4_PLANNED_
                            , a.RACE1_PLANNED_
                            , a.RACE2_PLANNED_
                            , a.RACE3_PLANNED_
                            , a.RACE4_PLANNED_
                            , a.TYPE1_PLANNED_HOL_
                            , a.TYPE2_PLANNED_HOL_
                            , a.TYPE3_PLANNED_HOL_
                            , a.TYPE4_PLANNED_HOL_
                            , a.RACE1_PLANNED_HOL_
                            , a.RACE2_PLANNED_HOL_
                            , a.RACE3_PLANNED_HOL_
                            , a.RACE4_PLANNED_HOL_
                            , a.TYPE5_PLANNED_
                            , a.TYPE6_PLANNED_
                            , a.RACE5_PLANNED_
                            , a.RACE6_PLANNED_
                            , a.TYPE5_PLANNED_HOL_
                            , a.TYPE6_PLANNED_HOL_
                            , a.RACE5_PLANNED_HOL_
                            , a.RACE6_PLANNED_HOL_
                            , a.ROUTE_ACTIVE_
                        FROM ROUTS a; """
                        
ins_sql = """ INSERT INTO ROUTS (ID_
                                , NAME_
                                , TYPE1_PLANNED_
                                , TYPE2_PLANNED_
                                , TYPE3_PLANNED_
                                , TYPE4_PLANNED_
                                , RACE1_PLANNED_
                                , RACE2_PLANNED_
                                , RACE3_PLANNED_
                                , RACE4_PLANNED_
                                , TYPE1_PLANNED_HOL_
                                , TYPE2_PLANNED_HOL_
                                , TYPE3_PLANNED_HOL_
                                , TYPE4_PLANNED_HOL_
                                , RACE1_PLANNED_HOL_
                                , RACE2_PLANNED_HOL_
                                , RACE3_PLANNED_HOL_
                                , RACE4_PLANNED_HOL_
                                , TYPE5_PLANNED_
                                , TYPE6_PLANNED_
                                , RACE5_PLANNED_
                                , RACE6_PLANNED_
                                , TYPE5_PLANNED_HOL_
                                , TYPE6_PLANNED_HOL_
                                , RACE5_PLANNED_HOL_
                                , RACE6_PLANNED_HOL_
                                , ROUTE_ACTIVE_)
              VALUES (%s, '%s',  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); 
              """
del_sql = " DELETE FROM ROUTS WHERE ID_ = %d; " 
up_sql = """ UPDATE ROUTS  
                        SET 
                                  NAME_ = '%s'
                                , TYPE1_PLANNED_ = %s
                                , TYPE2_PLANNED_ = %s
                                , TYPE3_PLANNED_ = %s
                                , TYPE4_PLANNED_ = %s
                                , RACE1_PLANNED_ = %s
                                , RACE2_PLANNED_ = %s
                                , RACE3_PLANNED_ = %s
                                , RACE4_PLANNED_ = %s
                                , TYPE1_PLANNED_HOL_ = %s
                                , TYPE2_PLANNED_HOL_ = %s
                                , TYPE3_PLANNED_HOL_ = %s
                                , TYPE4_PLANNED_HOL_ = %s
                                , RACE1_PLANNED_HOL_ = %s
                                , RACE2_PLANNED_HOL_ = %s
                                , RACE3_PLANNED_HOL_ = %s
                                , RACE4_PLANNED_HOL_ = %s
                                , TYPE5_PLANNED_ = %s
                                , TYPE6_PLANNED_ = %s
                                , RACE5_PLANNED_ = %s
                                , RACE6_PLANNED_ = %s
                                , TYPE5_PLANNED_HOL_ = %s
                                , TYPE6_PLANNED_HOL_ = %s
                                , RACE5_PLANNED_HOL_ = %s
                                , RACE6_PLANNED_HOL_ = %s
                                , ROUTE_ACTIVE_ = %s
                     
                     WHERE ID_ = %s;
                               """