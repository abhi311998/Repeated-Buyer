import time
import pandas as pd
import numpy as np
from Utility import *

def user_mer(df):
    start = time.time()
    print('Approximately, it takes: 45 seconds')
    # action distribution b/w user & merchant
    user_mer1 = df[df.label!=-1].groupby(['user_id','merchant_id','action_type']).agg({'action_type':\
                                'count'}).rename(columns={'action_type':'action_count'}).reset_index()
    user_mer1 = user_mer1.pivot_table(index=['user_id','merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user_mer1 = pd.DataFrame(user_mer1.to_records())
    user_mer1.columns = ['user_id','merchant_id','#act_0_UM','#act_1_UM','#act_2_UM','#act_3_UM']
    user_mer1['tot_acts_UM'] = user_mer1['#act_0_UM'] + user_mer1['#act_1_UM'] + user_mer1['#act_2_UM'] + \
                                        user_mer1['#act_3_UM']
    user_mer1['p_c_ratio_UM'] = user_mer1['#act_2_UM']/user_mer1['#act_0_UM']
    # Filled with 1 because number of clicks matches number of purchase
    user_mer1.replace([np.inf,-np.inf],1,inplace=True)
    print('Completed: 1 of 5...')
    # user_mer1

    ####################################################################################################################

    # Number of items/cats/brands clicked/purchasd b/w user & mer
    user_mer2 = df[(df.label!=-1) & (df.action_type!=1)].groupby(['user_id','merchant_id','action_type'])\
                                                .agg({'item_id':'nunique','cat_id':'nunique','brand_id':'nunique'}).reset_index()
    user_mer2 = user_mer2.pivot_table(index=['user_id','merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user_mer2 = pd.DataFrame(user_mer2.to_records())
    user_mer2.columns = ['user_id','merchant_id','#brands_click_UM','#brands_pur_UM','#brands_fav_UM','#cats_click_UM',\
                         '#cats_pur_UM','#cats_fav_UM','#items_click_UM','#items_pur_UM','#items_fav_UM']

    user_mer2['brands_p_c_ratio_UM'] = user_mer2['#brands_pur_UM']/user_mer2['#brands_click_UM']
    user_mer2['cats_p_c_ratio_UM'] = user_mer2['#cats_pur_UM']/user_mer2['#cats_click_UM']
    user_mer2['items_p_c_ratio_UM'] = user_mer2['#items_pur_UM']/user_mer2['#items_click_UM']

    # Filled with 1 because number of clicks matches number of purchase
    user_mer2.replace([np.inf,-np.inf],1,inplace=True)
    print('Completed: 2 of 5...')
    # user_mer2

    ####################################################################################################################

    # Number of days clicked/purchasd b/w user & mer
    user_mer3 = df[(df.label!=-1)&(df.action_type!=1)].groupby(['user_id','merchant_id','action_type']).\
                    agg({'time_stamp':'nunique'}).rename(columns={'time_stamp':'#unique_days_action'}).reset_index()
    user_mer3 = user_mer3.pivot_table(index=['user_id','merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user_mer3 = pd.DataFrame(user_mer3.to_records())
    user_mer3.columns = ['user_id','merchant_id','#days_click_UM','#days_pur_UM','#days_fav_UM']

    user_mer3['days_p_c_ratio_UM'] = user_mer3['#days_pur_UM']/user_mer3['#days_click_UM']

    # Filled with 1 because number of clicks matches number of purchase
    user_mer3.replace([np.inf,-np.inf],1,inplace=True)
    print('Completed: 3 of 5...')
    # user_mer3

    ####################################################################################################################

    # User p_c ratio on sales day
    user_mer4 = user_mer1.groupby(['user_id']).agg({'p_c_ratio_UM':'mean'}).rename(columns=\
                                                    {'p_c_ratio_UM':'avg_p_c_ratio_user_UM'}).reset_index()
    print('Completed: 4 of 5...')
    # user_mer4

    ####################################################################################################################

    # Merchant's p_c ratio on sales day
    user_mer5 = user_mer1.groupby(['merchant_id']).agg({'p_c_ratio_UM':'mean'}).rename(columns=\
                                                    {'p_c_ratio_UM':'avg_p_c_ratio_mer_UM'}).reset_index()
    print('Completed: 5 of 5...')
    # user_mer5

    ####################################################################################################################

    print('Few moments more...')
    
    ####################################################################################################################
    ####################################################################################################################
    
    def user_mer_last_7_days_ratio(user_mer_last_7_days,start_date,feature_names):
        end_date =1111          # end_date
        user_mer_last = df[(df.label!=-1) & ((df.time_stamp>=start_date) & (df.time_stamp<end_date))].\
                            groupby(['user_id','merchant_id','action_type'])['action_type'].count().to_frame().\
                            rename(columns={'action_type':'action_count'}).reset_index()

        user_mer_last = user_mer_last.pivot_table(index=['user_id','merchant_id'],columns=['action_type'],\
                                                  aggfunc=np.sum,fill_value=0)
        user_mer_last = pd.DataFrame(user_mer_last.to_records())
        user_mer_last.columns = ['user_id','merchant_id','#action_0_last_N_days','#action_1_last_N_days',\
                                 '#action_3_last_N_days']

        # Adding purchase action columns with value 0
        user_mer_last['#action_2_last_N_days'] = 0
        user_mer_last = user_mer_last[['user_id','merchant_id','#action_0_last_N_days','#action_1_last_N_days',\
                                       '#action_2_last_N_days','#action_3_last_N_days']]

        user_mer_last['total_actions'] = user_mer_last['#action_0_last_N_days'] +\
                                         user_mer_last['#action_1_last_N_days'] +\
                                         user_mer_last['#action_2_last_N_days'] +\
                                         user_mer_last['#action_3_last_N_days']


        user_mer_last = pd.merge(user_mer_last,user_mer_last_7_days,on=['user_id','merchant_id'],how='outer')
        user_mer_last.fillna(0,inplace=True)

        user_mer_last['0'] = user_mer_last['#act_0_last_7']/user_mer_last['#action_0_last_N_days']
        user_mer_last['1'] = user_mer_last['#act_1_last_7']/user_mer_last['#action_1_last_N_days']
        user_mer_last['2'] = user_mer_last['#act_2_last_7']/user_mer_last['#action_2_last_N_days']
        user_mer_last['3'] = user_mer_last['#act_3_last_7']/user_mer_last['#action_3_last_N_days']
        user_mer_last['tot'] = user_mer_last['total_acts_last_7']/user_mer_last['total_actions']
        user_mer_last.drop(['#action_0_last_N_days','#action_1_last_N_days','#action_2_last_N_days',\
                            '#action_3_last_N_days','total_actions','#act_0_last_7','#act_1_last_7',\
                            '#act_2_last_7','#act_3_last_7', 'total_acts_last_7'],axis=1,inplace=True)
        user_mer_last.columns = feature_names
        return user_mer_last

    # -------------------------------------------------------------------------------------------------- #

    # Last one week activity
    user_mer_last_7_days = df[(df.label!=-1) & ((df.time_stamp>=1104) & (df.time_stamp<1111))].\
                                    groupby(['user_id','merchant_id','action_type'])['action_type'].count().\
                                    to_frame().rename(columns={'action_type':'action_count'}).reset_index()

    user_mer_last_7_days = user_mer_last_7_days.pivot_table(index=['user_id','merchant_id'],\
                                                columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user_mer_last_7_days = pd.DataFrame(user_mer_last_7_days.to_records())
    user_mer_last_7_days.columns=['user_id','merchant_id','#act_0_last_7','#act_1_last_7','#act_3_last_7']

    # Adding purchase action columns with value 0
    user_mer_last_7_days['#act_2_last_7'] = 0
    user_mer_last_7_days = user_mer_last_7_days[['user_id','merchant_id','#act_0_last_7','#act_1_last_7',\
                                                 '#act_2_last_7','#act_3_last_7']]

    user_mer_last_7_days['total_acts_last_7'] = user_mer_last_7_days['#act_0_last_7'] +\
                                                     user_mer_last_7_days['#act_1_last_7'] +\
                                                     user_mer_last_7_days['#act_2_last_7'] +\
                                                     user_mer_last_7_days['#act_3_last_7']
    user_mer_last_7_days

    # -------------------------------------------------------------------------------------------------- #

    user_mer11 = user_mer_last_7_days_ratio(user_mer_last_7_days,1011,['user_id','merchant_id',\
                                      'act_0_last_7_30_days_UM','act_1_last_7_30_days_UM',\
                         'act_2_last_7_30_days_UM','act_3_last_7_30_days_UM','tot_acts_last_7_30_days_UM'])

    user_mer22 = user_mer_last_7_days_ratio(user_mer_last_7_days,911,['user_id','merchant_id',\
                                      'act_0_last_7_60_days_UM','act_1_last_7_60_days_UM',\
                        'act_2_last_7_60_days_UM','act_3_last_7_60_days_UM','tot_acts_last_7_60_days_UM'])

    user_mer33 = user_mer_last_7_days_ratio(user_mer_last_7_days,511,['user_id','merchant_id',\
                                    'act_0_last_7_180_days_UM','act_1_last_7_180_days_UM',\
                        'act_2_last_7_180_days_UM','act_3_last_7_180_days_UM','tot_acts_last_7_180_days_UM'])

    del user_mer_last_7_days

    user_mer_last_7_days = pd.merge(user_mer11,user_mer22,on=['user_id','merchant_id'],how='outer')
    user_mer_last_7_days = pd.merge(user_mer_last_7_days,user_mer33,on=['user_id','merchant_id'],how='outer')

    del user_mer11
    del user_mer22
    del user_mer33

    um = df[df.label!=-1][['user_id','merchant_id','label']].drop_duplicates()
    user_mer_last_7_days = pd.merge(um[['user_id','merchant_id']],user_mer_last_7_days,\
                                    on=['user_id','merchant_id'],how='outer')
    '''
    Missing values
    tot_acts_last_7_180_days_UM    292697
    tot_acts_last_7_60_days_UM     302974
    act_0_last_7_180_days_UM       304017
    tot_acts_last_7_30_days_UM     308865
    act_0_last_7_60_days_UM        314268
    act_0_last_7_30_days_UM        319900
    act_3_last_7_180_days_UM       444090
    act_3_last_7_60_days_UM        448216
    act_3_last_7_30_days_UM        451301
    act_1_last_7_180_days_UM       516012
    act_1_last_7_60_days_UM        516125
    act_1_last_7_30_days_UM        516233
    act_2_last_7_30_days_UM        522341
    act_2_last_7_60_days_UM        522341
    act_2_last_7_180_days_UM       522341
    '''

    user_mer_last_7_days.fillna(0,inplace=True)
    user_mer_last_7_days
    
    ####################################################################################################################
    ####################################################################################################################

    user_mer = pd.merge(user_mer1,user_mer4,on='user_id')
    user_mer = pd.merge(user_mer,user_mer5,on='merchant_id')

    user_mer = pd.merge(user_mer,user_mer2,on=['user_id','merchant_id'])
    user_mer = pd.merge(user_mer,user_mer3,on=['user_id','merchant_id'])
    user_mer = pd.merge(user_mer,user_mer_last_7_days,on=['user_id','merchant_id'])
    del user_mer1
    del user_mer2
    del user_mer3
    del user_mer4
    del user_mer5
    del user_mer_last_7_days

    print('Done...')
    end = time.time()
    t1 = end-start
    print('Time taken:',(end - start),'seconds')
    
    ####################################################################################################################
    ####################################################################################################################
    return user_mer