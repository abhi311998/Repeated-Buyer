import time
import pandas as pd
import numpy as np
from Utility import *

def user(df,nor_data,sales_data):
    # User
    ## User's nor data
    start = time.time()
#                                                   USER NORMAL DATA
    print('Approximately, it takes: 300 seconds')
    print('User_normal_data...')

    # Action_type count
    user1 = nor_data.groupby(['user_id','action_type'])['action_type'].count().to_frame().\
                    rename(columns={'action_type':'action_count'}).reset_index()

    user1 = user1.pivot_table(index=['user_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user1 = pd.DataFrame(user1.to_records())
    user1.columns = ['user_id','#act_0_nor_U','#act_1_nor_U','#act_2_nor_U','#act_3_nor_U']

    user1['tot_acts_nor_U'] = user1['#act_0_nor_U'] + user1['#act_1_nor_U'] + user1['#act_2_nor_U'] +\
                                    user1['#act_3_nor_U']

    print('Completed: 1 of 13...')
    # user1

    ##################################################################################################################

    # Number of unique items/brands/cats being clicked/purchased by buyer by old merchant in the overall period
    user2 = nor_data[(nor_data.action_type==0) | (nor_data.action_type==2)].groupby(['user_id','action_type']).\
                agg({'item_id':'nunique','cat_id':'nunique','brand_id':'nunique'}).reset_index()
    user2 = user2.pivot_table(index=['user_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user2 = pd.DataFrame(user2.to_records())
    user2.columns = ['user_id','#brands_click_nor_U','#brands_pur_nor_U','#cats_click_nor_U','#cats_pur_nor_U',\
                             '#items_click_nor_U','#items_pur_nor_U']

    print('Completed: 2 of 13...')
    # user2

    ################################################################################################################

    # 1.4 Number of days user is active apart from nor day (Click/Purchase)
    user3 = nor_data[(nor_data.action_type==0) | (nor_data.action_type==2)].groupby(['user_id','action_type']).\
                agg({'time_stamp':'nunique'}).rename(columns={'time_stamp':'#unique_days_action'}).reset_index()

    user3 = user3.pivot_table(index=['user_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user3 = pd.DataFrame(user3.to_records())
    user3.columns = ['user_id','#days_click_nor_U','#days_pur_nor_U']

    print('Completed: 3 of 13...')
    # user3

    ################################################################################################################

    user_nor = merge(user1,user2,'user_id','outer')
    user_nor = merge(user_nor,user3,'user_id','outer')

    del user1
    del user2
    del user3

    user_nor['#act_0_nor_U'] = user_nor['#act_0_nor_U']/user_nor['tot_acts_nor_U']
    user_nor['#act_1_nor_U'] = user_nor['#act_1_nor_U']/user_nor['tot_acts_nor_U']
    user_nor['#act_2_nor_U'] = user_nor['#act_2_nor_U']/user_nor['tot_acts_nor_U']
    user_nor['#act_3_nor_U'] = user_nor['#act_3_nor_U']/user_nor['tot_acts_nor_U']

    user_nor['brands_p_c_ratio_nor_U'] = user_nor['#brands_pur_nor_U']/user_nor['#brands_click_nor_U']
    user_nor['cats_p_c_ratio_nor_U'] = user_nor['#cats_pur_nor_U']/user_nor['#cats_click_nor_U']
    user_nor['items_p_c_ratio_nor_U'] = user_nor['#items_pur_nor_U']/user_nor['#items_click_nor_U']
    user_nor['days_p_c_ratio_nor_U'] = user_nor['#days_pur_nor_U']/user_nor['#days_click_nor_U']


    # Replacing it with 1 because for purchase, there must be a click earlier
    user_nor['brands_p_c_ratio_nor_U'].replace([np.inf, -np.inf], 1,inplace=True)
    user_nor['cats_p_c_ratio_nor_U'].replace([np.inf, -np.inf], 1,inplace=True)
    user_nor['items_p_c_ratio_nor_U'].replace([np.inf, -np.inf], 1,inplace=True)
    user_nor['days_p_c_ratio_nor_U'].replace([np.inf, -np.inf], 1,inplace=True)

    # user_nor

    ################################################################################################################
    ################################################################################################################


#                                                   USER SALES DATA
    print('User_sales_data...')

    # Action_type count
    user1 = sales_data.groupby(['user_id','action_type'])['action_type'].count().to_frame().\
                    rename(columns={'action_type':'action_count'}).reset_index()

    user1 = user1.pivot_table(index=['user_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user1 = pd.DataFrame(user1.to_records())
    user1.columns = ['user_id','#act_0_sales_U','#act_1_sales_U','#act_2_sales_U','#act_3_sales_U']

    user1['tot_acts_sales_U'] = user1['#act_0_sales_U'] + user1['#act_1_sales_U'] + user1['#act_2_sales_U'] +\
                                    user1['#act_3_sales_U']

    print('Completed: 4 of 13...')
    # user1

    ##################################################################################################################

    # Number of unique items/brands/cats being clicked/purchased by buyer by old merchant in the overall period
    user2 = sales_data[(sales_data.action_type==0) | (sales_data.action_type==2)].groupby(['user_id','action_type']).\
                agg({'item_id':'nunique','cat_id':'nunique','brand_id':'nunique'}).reset_index()
    user2 = user2.pivot_table(index=['user_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user2 = pd.DataFrame(user2.to_records())
    user2.columns = ['user_id','#brands_click_sales_U','#brands_pur_sales_U','#cats_click_sales_U','#cats_pur_sales_U',\
                             '#items_click_sales_U','#items_pur_sales_U']

    print('Completed: 5 of 13...')
    # user2

    ################################################################################################################

    # 1.4 Number of days user is active apart from sales day (Click/Purchase)
    user3 = sales_data[(sales_data.action_type==0) | (sales_data.action_type==2)].groupby(['user_id','action_type']).\
                agg({'time_stamp':'nunique'}).rename(columns={'time_stamp':'#unique_days_action'}).reset_index()

    user3 = user3.pivot_table(index=['user_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user3 = pd.DataFrame(user3.to_records())
    user3.columns = ['user_id','#days_click_sales_U','#days_pur_sales_U']

    print('Completed: 6 of 13...')
    # user3

    ################################################################################################################

    user_sales = merge(user1,user2,'user_id','outer')
    user_sales = merge(user_sales,user3,'user_id','outer')

    del user1
    del user2
    del user3

    user_sales['#act_0_sales_U'] = user_sales['#act_0_sales_U']/user_sales['tot_acts_sales_U']
    user_sales['#act_1_sales_U'] = user_sales['#act_1_sales_U']/user_sales['tot_acts_sales_U']
    user_sales['#act_2_sales_U'] = user_sales['#act_2_sales_U']/user_sales['tot_acts_sales_U']
    user_sales['#act_3_sales_U'] = user_sales['#act_3_sales_U']/user_sales['tot_acts_sales_U']

    user_sales['brands_p_c_ratio_sales_U'] = user_sales['#brands_pur_sales_U']/user_sales['#brands_click_sales_U']
    user_sales['cats_p_c_ratio_sales_U'] = user_sales['#cats_pur_sales_U']/user_sales['#cats_click_sales_U']
    user_sales['items_p_c_ratio_sales_U'] = user_sales['#items_pur_sales_U']/user_sales['#items_click_sales_U']
    user_sales['days_p_c_ratio_sales_U'] = user_sales['#days_pur_sales_U']/user_sales['#days_click_sales_U']


    # Replacing it with 1 because for purchase, there must be a click earlier
    user_sales['brands_p_c_ratio_sales_U'].replace([np.inf, -np.inf], 1,inplace=True)
    user_sales['cats_p_c_ratio_sales_U'].replace([np.inf, -np.inf], 1,inplace=True)
    user_sales['items_p_c_ratio_sales_U'].replace([np.inf, -np.inf], 1,inplace=True)
    user_sales['days_p_c_ratio_sales_U'].replace([np.inf, -np.inf], 1,inplace=True)

    # user_sales

    ################################################################################################################
    ################################################################################################################

#                                                   USER OTHER DATA
    
    print('User_other_data...')
    
    # Number of unique old/new merchants with which buyer has made a trade
    user1 = df.groupby(['user_id','old_um']).agg({'merchant_id':'nunique'}).reset_index()
    user1 = user1.pivot_table(index=['user_id'],columns=['old_um'],aggfunc=np.sum,fill_value=0)
    user1 = pd.DataFrame(user1.to_records())
    user1.columns = ['user_id','#new_mer_U','#old_mer_U']
    user1['new_old_mer_ratio_U'] = user1['#new_mer_U']/user1['#old_mer_U']
    user1.replace([np.inf,-np.inf],np.nan,inplace=True)

    print('Completed: 7 of 13...')
    # user1

    ################################################################################################################

    # Month wise distribution of actions of users
    user2 = df.groupby(['user_id','month','action_type'])['action_type'].count().to_frame().rename(columns=\
                                                                        {'action_type':'act_count'}).reset_index()

    user2 = user2.pivot_table(index=['user_id','month'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user2 = pd.DataFrame(user2.to_records())
    user2.columns = ['user_id','month','#act_0_U','#act_1_U','#act_2_U','#act_3_U']

    user2 = user2.pivot_table(index=['user_id'],columns=['month'],aggfunc=np.sum,fill_value=0)
    user2 = pd.DataFrame(user2.to_records())
    # user5.columns = ['user_id','action_type','May','Jun','Jul','Aug','Sep','Oct','Nov']

    user2.columns = ['user_id','May_act_0_U','Jun_act_0_U','Jul_act_0_U','Aug_act_0_U'\
                     ,'Sep_act_0_U','Oct_act_0_U','Nov_act_0_U',\
                     'May_act_1_U','Jun_act_1_U','Jul_act_1_U','Aug_act_1_U'\
                     ,'Sep_act_1_U','Oct_act_1_U','Nov_act_1_U',\
                    'May_act_2_U','Jun_act_2_U','Jul_act_2_U','Aug_act_2_U'\
                     ,'Sep_act_2_U','Oct_act_2_U','Nov_act_2_U',\
                    'May_act_3_U','Jun_act_3_U','Jul_act_3_U','Aug_act_3_U'\
                     ,'Sep_act_3_U','Oct_act_3_U','Nov_act_3_U']

    print('Completed: 8 of 13...')
    # user2

    ##################################################################################################################

    # new merchants of user on sales day
    # old merchants of user on sales day
    user3 = df[df.time_stamp==1111].groupby(['user_id','old_um']).agg({'merchant_id':'nunique'}).reset_index()
    user3 = user3.pivot_table(index=['user_id'],columns=['old_um'],aggfunc=np.sum,fill_value=0)
    user3 = pd.DataFrame(user3.to_records())
    user3.columns = ['user_id','#new_mer_sales_day_U','#old_mer_sales_day_U']
    user3['new_old_mer_sales_day_ratio_U'] = user3['#new_mer_sales_day_U']/user3['#old_mer_sales_day_U']
    user3.replace([np.inf,-np.inf],np.nan,inplace=True)
    # user3
    print('Completed: 9 of 13...')

    ################################################################################################################

    # Average p_c ratio of user
    user4 = df[(df.label==-1) & ((df.action_type==0) | (df.action_type==2))].groupby(['user_id','merchant_id',\
                'action_type']).agg({'action_type':'count'}).rename(columns={'action_type':'action_count'}).reset_index()

    user4 = user4.pivot_table(index=['user_id','merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user4 = pd.DataFrame(user4.to_records())
    user4.columns = ['user_id','merchant_id','avg_act_0_U','avg_act_2_U']
    user4['avg_p_c_ratio_U'] = user4['avg_act_2_U']/user4['avg_act_0_U']
    user4.replace([np.inf, -np.inf], 1,inplace=True)
    user4 = user4[user4.avg_p_c_ratio_U!=0].groupby(['user_id']).agg({'avg_act_0_U':'mean','avg_act_2_U':'mean',\
                                            'avg_p_c_ratio_U':'mean'}).reset_index()
    # user4
    print('Completed: 10 of 13...')

    ####################################################################################################################

    user5 = df[(df.time_stamp==1111) & (df.action_type==2)].groupby(['user_id','old_um']).agg({'action_type':'count'}).\
                            reset_index()
    user5 = user5.pivot_table(index=['user_id'],columns=['old_um'],aggfunc=np.sum,fill_value=0)
    user5 = pd.DataFrame(user5.to_records())
    user5.columns = ['user_id','#pur_new_mer_U','#pur_old_mer_U']
    user5['p_ratio_old_new_mer_U'] = user5['#pur_old_mer_U']/user5['#pur_new_mer_U']
    # user5
    print('Completed: 11 of 13...')

    ####################################################################################################################

    # Last 7 days activity vs 30/60/180 activity

    # start_date: start_date_for_interval_to_be_checked
    # feature_names: features to be named

    def user_last_7_days_ratio(user_last_7_days,start_date,feature_names):
        end_date =1111          # end_date
        user_last = df[(df.time_stamp>=start_date) & (df.time_stamp<end_date)].groupby(['user_id','action_type'])\
                    ['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()

        user_last = user_last.pivot_table(index=['user_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
        user_last = pd.DataFrame(user_last.to_records())
        user_last.columns = ['user_id','#action_0_last_N_days','#action_1_last_N_days','#action_2_last_N_days',\
                                         '#action_3_last_N_days']

        user_last['total_actions'] = user_last['#action_0_last_N_days'] + user_last['#action_1_last_N_days']\
                                            + user_last['#action_2_last_N_days'] + user_last['#action_3_last_N_days']

        user_last = merge(user_last,user_last_7_days,'user_id','outer')
        user_last.fillna(0,inplace=True)
        user_last['0'] = user_last['#action_0_last_7']/user_last['#action_0_last_N_days']
        user_last['1'] = user_last['#action_1_last_7']/user_last['#action_1_last_N_days']
        user_last['2'] = user_last['#action_2_last_7']/user_last['#action_2_last_N_days']
        user_last['3'] = user_last['#action_3_last_7']/user_last['#action_3_last_N_days']
        user_last['tot'] = user_last['total_actions_y']/user_last['total_actions_x']
        user_last.drop(['#action_0_last_N_days','#action_1_last_N_days','#action_2_last_N_days','#action_3_last_N_days',\
                'total_actions_x','#action_0_last_7', '#action_1_last_7', '#action_2_last_7',\
                '#action_3_last_7', 'total_actions_y'],axis=1,inplace=True)
        user_last.columns = feature_names
        return user_last

    # -------------------------------------------------------------------------------------------------------------- #


    # Last one week activity
    user_last_7_days = df[(df.time_stamp>=1104) & (df.time_stamp<1111)].groupby(['user_id','action_type'])\
                         ['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()

    user_last_7_days = user_last_7_days.pivot_table(index=['user_id'],columns=['action_type'],\
                                                        aggfunc=np.sum,fill_value=0)
    user_last_7_days = pd.DataFrame(user_last_7_days.to_records())
    user_last_7_days.columns = ['user_id','#action_0_last_7','#action_1_last_7','#action_2_last_7','#action_3_last_7']
    user_last_7_days['total_actions'] = user_last_7_days['#action_0_last_7'] + user_last_7_days['#action_1_last_7']\
                                        + user_last_7_days['#action_2_last_7'] + user_last_7_days['#action_3_last_7']
    user_last_7_days

    # -------------------------------------------------------------------------------------------------------------- #

    user11 = user_last_7_days_ratio(user_last_7_days,1011,['user_id','act_0_last_7_30_days_U','act_1_last_7_30_days_U',\
                    'act_2_last_7_30_days_U','act_3_last_7_30_days_U','tot_act_last_7_30_days_U'])

    user22 = user_last_7_days_ratio(user_last_7_days,911,['user_id','act_0_last_7_60_days_U','act_1_last_7_60_days_U',\
                    'act_2_last_7_60_days_U','act_3_last_7_60_days_U','tot_act_last_7_60_days_U'])

    user33 = user_last_7_days_ratio(user_last_7_days,511,['user_id','act_0_last_7_180_days_U','act_1_last_7_180_days_U',\
                    'act_2_last_7_180_days_U','act_3_last_7_180_days_U','tot_act_last_7_180_days_U'])

    del user_last_7_days
    user_last_7_days = pd.merge(user11,user22,on='user_id',how='outer')
    user_last_7_days = pd.merge(user_last_7_days,user33,on='user_id',how='outer')

    del user11
    del user22
    del user33
    print('Completed: 12 of 13...')
    # user_last_7_days

    ################################################################################################################

    user_other = merge(user1,user3,'user_id','outer')
    user_other = merge(user_other,user4,'user_id','outer')
    user_other = merge(user_other,user5,'user_id','outer')
    user_other = merge(user_other,user_last_7_days,'user_id','outer')
    user_other = merge(user_other,user2,'user_id','outer')

    del user1
    del user2
    del user3
    del user4
    del user5
    del user_last_7_days

    # user_other


    ################################################################################################################
    ################################################################################################################

    # Similarity scores of user_nor & user_sales data
    usr = pd.merge(user_nor,user_sales,on='user_id',how='outer')
    usr.fillna(0,inplace=True)  # b'coz they are not active

    usr['sim_score_nor_sales_U'] = usr.apply(lambda x: sim_score(np.array(x[1:18]),np.array(x[18:])),axis=1)
    usr

    user = pd.merge(user_nor,user_sales,on='user_id',how='outer')
    user = pd.merge(user,user_other,on='user_id',how='outer')
    user = pd.merge(user,usr[['user_id','sim_score_nor_sales_U']],on='user_id',how='outer')
    del usr
    print('Completed: 13 of 13...')
    # user

    ################################################################################################################
    ################################################################################################################
    
    print('Done...')
    end = time.time()
    print('Time taken:',(end - start),'seconds')
    return user
    ################################################################################################################
    ################################################################################################################