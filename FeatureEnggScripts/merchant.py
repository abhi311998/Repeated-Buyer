import time
import pandas as pd
import numpy as np
from Utility import *

def merchant(df,nor_data,sales_data):
    start = time.time()
    print('Merchant_normal_data...')
    print('Approximately, it takes: 300 seconds')

    # Action_type count
    merchant1 = nor_data.groupby(['merchant_id','action_type'])['action_type'].count().to_frame().\
                    rename(columns={'action_type':'action_count'}).reset_index()

    merchant1 = merchant1.pivot_table(index=['merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    merchant1 = pd.DataFrame(merchant1.to_records())
    merchant1.columns = ['merchant_id','#act_0_nor_M','#act_1_nor_M','#act_2_nor_M','#act_3_nor_M']

    merchant1['tot_acts_nor_M'] = merchant1['#act_0_nor_M'] + merchant1['#act_1_nor_M'] + merchant1['#act_2_nor_M'] +\
                                    merchant1['#act_3_nor_M']

    print('Completed: 1 of 13...')
    # merchant1

    ##################################################################################################################

    # Number of unique items/brands/cats being clicked/purchased by buyer by old merchant in the overall period
    merchant2 = nor_data[(nor_data.action_type==0) | (nor_data.action_type==2)].groupby(['merchant_id','action_type']).\
                agg({'item_id':'nunique','cat_id':'nunique','brand_id':'nunique'}).reset_index()
    merchant2 = merchant2.pivot_table(index=['merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    merchant2 = pd.DataFrame(merchant2.to_records())
    merchant2.columns = ['merchant_id','#brands_click_nor_M','#brands_pur_nor_M','#cats_click_nor_M','#cats_pur_nor_M',\
                             '#items_click_nor_M','#items_pur_nor_M']

    print('Completed: 2 of 13...')
    # merchant2

    ################################################################################################################

    # 1.4 Number of days merchant is active apart from nor day (Click/Purchase)
    merchant3 = nor_data[(nor_data.action_type==0) | (nor_data.action_type==2)].groupby(['merchant_id','action_type']).\
                agg({'time_stamp':'nunique'}).rename(columns={'time_stamp':'#unique_days_action'}).reset_index()

    merchant3 = merchant3.pivot_table(index=['merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    merchant3 = pd.DataFrame(merchant3.to_records())
    merchant3.columns = ['merchant_id','#days_click_nor_M','#days_pur_nor_M']

    print('Completed: 3 of 13...')
    # merchant3

    ################################################################################################################

    merchant_nor = merge(merchant1,merchant2,'merchant_id','outer')
    merchant_nor = merge(merchant_nor,merchant3,'merchant_id','outer')

    del merchant1
    del merchant2
    del merchant3

    merchant_nor['#act_0_nor_M'] = merchant_nor['#act_0_nor_M']/merchant_nor['tot_acts_nor_M']
    merchant_nor['#act_1_nor_M'] = merchant_nor['#act_1_nor_M']/merchant_nor['tot_acts_nor_M']
    merchant_nor['#act_2_nor_M'] = merchant_nor['#act_2_nor_M']/merchant_nor['tot_acts_nor_M']
    merchant_nor['#act_3_nor_M'] = merchant_nor['#act_3_nor_M']/merchant_nor['tot_acts_nor_M']

    merchant_nor['brands_p_c_ratio_nor_M'] = merchant_nor['#brands_pur_nor_M']/merchant_nor['#brands_click_nor_M']
    merchant_nor['cats_p_c_ratio_nor_M'] = merchant_nor['#cats_pur_nor_M']/merchant_nor['#cats_click_nor_M']
    merchant_nor['items_p_c_ratio_nor_M'] = merchant_nor['#items_pur_nor_M']/merchant_nor['#items_click_nor_M']
    merchant_nor['days_p_c_ratio_nor_M'] = merchant_nor['#days_pur_nor_M']/merchant_nor['#days_click_nor_M']


    # Replacing it with 1 because for purchase, there must be a click earlier
    merchant_nor['brands_p_c_ratio_nor_M'].replace([np.inf, -np.inf], 1,inplace=True)
    merchant_nor['cats_p_c_ratio_nor_M'].replace([np.inf, -np.inf], 1,inplace=True)
    merchant_nor['items_p_c_ratio_nor_M'].replace([np.inf, -np.inf], 1,inplace=True)
    merchant_nor['days_p_c_ratio_nor_M'].replace([np.inf, -np.inf], 1,inplace=True)

    # merchant_nor
    
    ################################################################################################################
    ################################################################################################################

    print('Merchant_sales_data...')

    # Action_type count
    merchant1 = sales_data.groupby(['merchant_id','action_type'])['action_type'].count().to_frame().\
                    rename(columns={'action_type':'action_count'}).reset_index()

    merchant1 = merchant1.pivot_table(index=['merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    merchant1 = pd.DataFrame(merchant1.to_records())
    merchant1.columns = ['merchant_id','#act_0_sales_M','#act_1_sales_M','#act_2_sales_M','#act_3_sales_M']

    merchant1['tot_acts_sales_M'] = merchant1['#act_0_sales_M'] + merchant1['#act_1_sales_M'] + merchant1['#act_2_sales_M'] +\
                                    merchant1['#act_3_sales_M']

    print('Completed: 4 of 13...')
    # merchant1

    ##################################################################################################################

    # Number of unique items/brands/cats being clicked/purchased by buyer by old merchant in the overall period
    merchant2 = sales_data[(sales_data.action_type==0) | (sales_data.action_type==2)].groupby(['merchant_id','action_type']).\
                agg({'item_id':'nunique','cat_id':'nunique','brand_id':'nunique'}).reset_index()
    merchant2 = merchant2.pivot_table(index=['merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    merchant2 = pd.DataFrame(merchant2.to_records())
    merchant2.columns = ['merchant_id','#brands_click_sales_M','#brands_pur_sales_M','#cats_click_sales_M','#cats_pur_sales_M',\
                             '#items_click_sales_M','#items_pur_sales_M']

    print('Completed: 5 of 13...')
    # merchant2

    ################################################################################################################

    # 1.4 Number of days merchant is active apart from sales day (Click/Purchase)
    merchant3 = sales_data[(sales_data.action_type==0) | (sales_data.action_type==2)].groupby(['merchant_id','action_type']).\
                agg({'time_stamp':'nunique'}).rename(columns={'time_stamp':'#unique_days_action'}).reset_index()

    merchant3 = merchant3.pivot_table(index=['merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    merchant3 = pd.DataFrame(merchant3.to_records())
    merchant3.columns = ['merchant_id','#days_click_sales_M','#days_pur_sales_M']

    print('Completed: 6 of 13...')
    # merchant3

    ################################################################################################################

    merchant_sales = merge(merchant1,merchant2,'merchant_id','outer')
    merchant_sales = merge(merchant_sales,merchant3,'merchant_id','outer')

    del merchant1
    del merchant2
    del merchant3

    merchant_sales['#act_0_sales_M'] = merchant_sales['#act_0_sales_M']/merchant_sales['tot_acts_sales_M']
    merchant_sales['#act_1_sales_M'] = merchant_sales['#act_1_sales_M']/merchant_sales['tot_acts_sales_M']
    merchant_sales['#act_2_sales_M'] = merchant_sales['#act_2_sales_M']/merchant_sales['tot_acts_sales_M']
    merchant_sales['#act_3_sales_M'] = merchant_sales['#act_3_sales_M']/merchant_sales['tot_acts_sales_M']

    merchant_sales['brands_p_c_ratio_sales_M'] = merchant_sales['#brands_pur_sales_M']/merchant_sales['#brands_click_sales_M']
    merchant_sales['cats_p_c_ratio_sales_M'] = merchant_sales['#cats_pur_sales_M']/merchant_sales['#cats_click_sales_M']
    merchant_sales['items_p_c_ratio_sales_M'] = merchant_sales['#items_pur_sales_M']/merchant_sales['#items_click_sales_M']
    merchant_sales['days_p_c_ratio_sales_M'] = merchant_sales['#days_pur_sales_M']/merchant_sales['#days_click_sales_M']


    # Replacing it with 1 because for purchase, there must be a click earlier
    merchant_sales['brands_p_c_ratio_sales_M'].replace([np.inf, -np.inf], 1,inplace=True)
    merchant_sales['cats_p_c_ratio_sales_M'].replace([np.inf, -np.inf], 1,inplace=True)
    merchant_sales['items_p_c_ratio_sales_M'].replace([np.inf, -np.inf], 1,inplace=True)
    merchant_sales['days_p_c_ratio_sales_M'].replace([np.inf, -np.inf], 1,inplace=True)

    # merchant_sales
    
    ################################################################################################################
    ################################################################################################################

    print('Merchant_other_related_data...')
    # Number of unique old/new merchants with which buyer has made a trade
    merchant1 = df.groupby(['merchant_id','old_um']).agg({'user_id':'nunique'}).reset_index()
    merchant1 = merchant1.pivot_table(index=['merchant_id'],columns=['old_um'],aggfunc=np.sum,fill_value=0)
    merchant1 = pd.DataFrame(merchant1.to_records())
    merchant1.columns = ['merchant_id','#new_buyer_M','#old_buyer_M']
    merchant1['new_old_buyer_ratio_M'] = merchant1['#new_buyer_M']/merchant1['#old_buyer_M']
    merchant1.replace([np.inf,-np.inf],np.nan,inplace=True)

    print('Completed: 7 of 13...')
    # merchant1

    ################################################################################################################

    # Month wise distribution of actions of merchants
    merchant2 = df.groupby(['merchant_id','month','action_type'])['action_type'].count().to_frame().rename(columns=\
                                                                        {'action_type':'act_count'}).reset_index()

    merchant2 = merchant2.pivot_table(index=['merchant_id','month'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    merchant2 = pd.DataFrame(merchant2.to_records())
    merchant2.columns = ['merchant_id','month','#act_0_M','#act_1_M','#act_2_M','#act_3_M']

    merchant2 = merchant2.pivot_table(index=['merchant_id'],columns=['month'],aggfunc=np.sum,fill_value=0)
    merchant2 = pd.DataFrame(merchant2.to_records())
    # merchant5.columns = ['merchant_id','action_type','May','Jun','Jul','Aug','Sep','Oct','Nov']

    merchant2.columns = ['merchant_id','May_act_0_M','Jun_act_0_M','Jul_act_0_M','Aug_act_0_M'\
                     ,'Sep_act_0_M','Oct_act_0_M','Nov_act_0_M',\
                     'May_act_1_M','Jun_act_1_M','Jul_act_1_M','Aug_act_1_M'\
                     ,'Sep_act_1_M','Oct_act_1_M','Nov_act_1_M',\
                    'May_act_2_M','Jun_act_2_M','Jul_act_2_M','Aug_act_2_M'\
                     ,'Sep_act_2_M','Oct_act_2_M','Nov_act_2_M',\
                    'May_act_3_M','Jun_act_3_M','Jul_act_3_M','Aug_act_3_M'\
                     ,'Sep_act_3_M','Oct_act_3_M','Nov_act_3_M']

    print('Completed: 8 of 13...')
    # merchant2

    ##################################################################################################################

    # new buyers of merchant on sales day
    # old buyers of merchant on sales day
    merchant3 = df[df.time_stamp==1111].groupby(['merchant_id','old_um']).agg({'user_id':'nunique'}).reset_index()
    merchant3 = merchant3.pivot_table(index=['merchant_id'],columns=['old_um'],aggfunc=np.sum,fill_value=0)
    merchant3 = pd.DataFrame(merchant3.to_records())
    merchant3.columns = ['merchant_id','#new_buyers_sales_day_M','#old_buyers_sales_day_M']
    merchant3['new_old_buyers_sales_day_ratio_M'] = merchant3['#new_buyers_sales_day_M']/merchant3['#old_buyers_sales_day_M']
    merchant3.replace([np.inf,-np.inf],np.nan,inplace=True)
    # merchant3
    print('Completed: 9 of 13...')

    ################################################################################################################

    # Average p_c ratio of merchant
    merchant4 = df[(df.label==-1) & ((df.action_type==0) | (df.action_type==2))].groupby(['merchant_id','user_id',\
                'action_type']).agg({'action_type':'count'}).rename(columns={'action_type':'action_count'}).reset_index()

    merchant4 = merchant4.pivot_table(index=['merchant_id','user_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    merchant4 = pd.DataFrame(merchant4.to_records())
    merchant4.columns = ['merchant_id','user_id','avg_act_0_M','avg_act_2_M']
    merchant4['avg_p_c_ratio_M'] = merchant4['avg_act_2_M']/merchant4['avg_act_0_M']
    merchant4.replace([np.inf, -np.inf], 1,inplace=True)
    merchant4 = merchant4[merchant4.avg_p_c_ratio_M!=0].groupby(['merchant_id']).agg({'avg_act_0_M':'mean','avg_act_2_M':'mean',\
                                            'avg_p_c_ratio_M':'mean'}).reset_index()
    # merchant4
    print('Completed: 10 of 13...')

    ####################################################################################################################

    merchant5 = df[(df.time_stamp==1111) & (df.action_type==2)].groupby(['merchant_id','old_um']).agg({'action_type':'count'}).\
                            reset_index()
    merchant5 = merchant5.pivot_table(index=['merchant_id'],columns=['old_um'],aggfunc=np.sum,fill_value=0)
    merchant5 = pd.DataFrame(merchant5.to_records())
    merchant5.columns = ['merchant_id','#pur_new_buyers_M','#pur_old_buyers_M']
    merchant5['p_ratio_old_new_buyers_M'] = merchant5['#pur_old_buyers_M']/merchant5['#pur_new_buyers_M']
    # merchant5
    print('Completed: 11 of 13...')

    ####################################################################################################################

    # Last 7 days activity vs 30/60/180

    # start_date: start_date_for_interval_to_be_checked
    # feature_names: features to be named

    def merchant_last_7_days_ratio(merchant_last_7_days,start_date,feature_names):
        end_date =1111          # end_date
        merchant_last = df[(df.time_stamp>=start_date) & (df.time_stamp<end_date)].groupby(['merchant_id','action_type'])\
                    ['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()

        merchant_last = merchant_last.pivot_table(index=['merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
        merchant_last = pd.DataFrame(merchant_last.to_records())
        merchant_last.columns = ['merchant_id','#action_0_last_N_days','#action_1_last_N_days','#action_2_last_N_days',\
                                         '#action_3_last_N_days']

        merchant_last['total_actions'] = merchant_last['#action_0_last_N_days'] + merchant_last['#action_1_last_N_days']\
                                            + merchant_last['#action_2_last_N_days'] + merchant_last['#action_3_last_N_days']

        merchant_last = merge(merchant_last,merchant_last_7_days,'merchant_id','outer')
        merchant_last.fillna(0,inplace=True)
        merchant_last['0'] = merchant_last['#action_0_last_7']/merchant_last['#action_0_last_N_days']
        merchant_last['1'] = merchant_last['#action_1_last_7']/merchant_last['#action_1_last_N_days']
        merchant_last['2'] = merchant_last['#action_2_last_7']/merchant_last['#action_2_last_N_days']
        merchant_last['3'] = merchant_last['#action_3_last_7']/merchant_last['#action_3_last_N_days']
        merchant_last['tot'] = merchant_last['total_actions_y']/merchant_last['total_actions_x']
        merchant_last.drop(['#action_0_last_N_days','#action_1_last_N_days','#action_2_last_N_days','#action_3_last_N_days',\
                'total_actions_x','#action_0_last_7', '#action_1_last_7', '#action_2_last_7',\
                '#action_3_last_7', 'total_actions_y'],axis=1,inplace=True)
        merchant_last.columns = feature_names
        return merchant_last

    # -------------------------------------------------------------------------------------------------------------- #


    # Last one week activity
    merchant_last_7_days = df[(df.time_stamp>=1104) & (df.time_stamp<1111)].groupby(['merchant_id','action_type'])\
                         ['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()

    merchant_last_7_days = merchant_last_7_days.pivot_table(index=['merchant_id'],columns=['action_type'],\
                                                        aggfunc=np.sum,fill_value=0)
    merchant_last_7_days = pd.DataFrame(merchant_last_7_days.to_records())
    merchant_last_7_days.columns = ['merchant_id','#action_0_last_7','#action_1_last_7','#action_2_last_7','#action_3_last_7']
    merchant_last_7_days['total_actions'] = merchant_last_7_days['#action_0_last_7'] + merchant_last_7_days['#action_1_last_7']\
                                        + merchant_last_7_days['#action_2_last_7'] + merchant_last_7_days['#action_3_last_7']
    merchant_last_7_days

    # -------------------------------------------------------------------------------------------------------------- #

    merchant11 = merchant_last_7_days_ratio(merchant_last_7_days,1011,['merchant_id','act_0_last_7_30_days_M','act_1_last_7_30_days_M',\
                    'act_2_last_7_30_days_M','act_3_last_7_30_days_M','tot_act_last_7_30_days_M'])

    merchant22 = merchant_last_7_days_ratio(merchant_last_7_days,911,['merchant_id','act_0_last_7_60_days_M','act_1_last_7_60_days_M',\
                    'act_2_last_7_60_days_M','act_3_last_7_60_days_M','tot_act_last_7_60_days_M'])

    merchant33 = merchant_last_7_days_ratio(merchant_last_7_days,511,['merchant_id','act_0_last_7_180_days_M','act_1_last_7_180_days_M',\
                    'act_2_last_7_180_days_M','act_3_last_7_180_days_M','tot_act_last_7_180_days_M'])

    del merchant_last_7_days
    merchant_last_7_days = pd.merge(merchant11,merchant22,on='merchant_id',how='outer')
    merchant_last_7_days = pd.merge(merchant_last_7_days,merchant33,on='merchant_id',how='outer')

    del merchant11
    del merchant22
    del merchant33
    print('Completed: 12 of 13...')
    # merchant_last_7_days

    ################################################################################################################

    merchant_other = merge(merchant1,merchant3,'merchant_id','outer')
    merchant_other = merge(merchant_other,merchant4,'merchant_id','outer')
    merchant_other = merge(merchant_other,merchant5,'merchant_id','outer')
    merchant_other = merge(merchant_other,merchant_last_7_days,'merchant_id','outer')
    merchant_other = merge(merchant_other,merchant2,'merchant_id','outer')

    del merchant1
    del merchant2
    del merchant3
    del merchant4
    del merchant5
    del merchant_last_7_days
    print('Completed: 13 of 13...')

    # merchant_other
    
    ################################################################################################################
    ################################################################################################################
    
    # Similarity scores of merchant_nor & merchant_sales data
    mer = pd.merge(merchant_nor,merchant_sales,on='merchant_id',how='outer')
    mer.fillna(0,inplace=True)  # b'coz they are not active
    mer
    mer['sim_score_nor_sales_M'] = mer.apply(lambda x: sim_score\
                                                (np.array(x[1:18]),np.array(x[18:])),axis=1)
    mer
    merchant = pd.merge(merchant_nor,merchant_sales,on='merchant_id',how='outer')
    merchant = pd.merge(merchant,merchant_other,on='merchant_id',how='outer')
    merchant = pd.merge(merchant,mer[['merchant_id','sim_score_nor_sales_M']],on='merchant_id',how='outer')
    del mer
    # merchant
    
    print('Done...')
    end = time.time()
    print('Time taken:',(end - start),'seconds')
    return merchant
    ################################################################################################################
    ################################################################################################################