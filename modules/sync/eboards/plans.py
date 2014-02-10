# -*- coding: utf-8 -*-

sel_src_sql = """  SELECT 
                    a.ID_
                    , a.DATE_
                    , a.ROUT_ID_
                    , a.TYPE1_PLANNED_
                    , a.TYPE2_PLANNED_
                    , a.TYPE3_PLANNED_
                    , a.TYPE4_PLANNED_
                    , a.RACE1_PLANNED_
                    , a.ACTIVE_
                    , a.RACE2_PLANNED_
                    , a.RACE3_PLANNED_
                    , a.RACE4_PLANNED_
                    , a.TYPE5_PLANNED_
                    , a.TYPE6_PLANNED_
                    , a.RACE5_PLANNED_
                    , a.RACE6_PLANNED_
                    , a.PROJ_ID_
                    FROM PLANS a; """
                    
sel_dst_sql = """  SELECT 
                    a.ID_
                    , a.TIME_
                    , a.ROUT_ID_
                    , a.TYPE1_PLANNED_
                    , a.TYPE2_PLANNED_
                    , a.TYPE3_PLANNED_
                    , a.TYPE4_PLANNED_
                    , a.RACE1_PLANNED_
                    , a.ACTIVE_
                    , a.RACE2_PLANNED_
                    , a.RACE3_PLANNED_
                    , a.RACE4_PLANNED_
                    , a.TYPE5_PLANNED_
                    , a.TYPE6_PLANNED_
                    , a.RACE5_PLANNED_
                    , a.RACE6_PLANNED_
                    , a.PROJ_ID_
                    FROM PLANS a;
                                                   """
ins_sql = """ INSERT INTO PLANS (ID_
                                , TIME_
                                , ROUT_ID_
                                , TYPE1_PLANNED_
                                , TYPE2_PLANNED_
                                , TYPE3_PLANNED_
                                , TYPE4_PLANNED_
                                , RACE1_PLANNED_
                                , ACTIVE_
                                , RACE2_PLANNED_
                                , RACE3_PLANNED_
                                , RACE4_PLANNED_
                                , TYPE5_PLANNED_
                                , TYPE6_PLANNED_
                                , RACE5_PLANNED_
                                , RACE6_PLANNED_
                                , PROJ_ID_)
            VALUES (%s, %s,  %s,  %s,  %s,  %s,  %s,  %s, %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s, %s);
                               """
del_sql = " DELETE FROM PLANS WHERE ID_ = %d; " 

up_sql = """ UPDATE PLANS  
                        SET 
                                TIME_ = %s
                                , ROUT_ID_ = %s
                                , TYPE1_PLANNED_ = %s
                                , TYPE2_PLANNED_ = %s
                                , TYPE3_PLANNED_ = %s
                                , TYPE4_PLANNED_ = %s
                                , RACE1_PLANNED_ = %s
                                , ACTIVE_ = %s
                                , RACE2_PLANNED_ = %s
                                , RACE3_PLANNED_ = %s
                                , RACE4_PLANNED_ = %s
                                , TYPE5_PLANNED_ = %s
                                , TYPE6_PLANNED_ = %s
                                , RACE5_PLANNED_ = %s
                                , RACE6_PLANNED_ = %s
                                , PROJ_ID_ = %s
                     
                     WHERE ID_ = %s;
                               """