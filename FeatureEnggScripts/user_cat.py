import time
import pandas as pd
import numpy as np
from Utility import *

def user_cat(df):
    start = time.time()
    print('Approximately, it takes: 100 seconds')

    # 1 #clicks, #add_cart, #purchase, #add_fav
    user_cat1 = df.groupby(['user_id','cat_id','action_type'])['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()
    # user_cat1

    user_cat1 = user_cat1.pivot_table(index=['user_id','cat_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user_cat1 = pd.DataFrame(user_cat1.to_records())
    user_cat1.columns = ['user_id','cat_id','#act_0_UC','#act_1_UC','#act_2_UC','#act_3_UC']

    user_cat1['tot_acts_UC'] = user_cat1['#act_0_UC'] + user_cat1['#act_1_UC'] + user_cat1['#act_2_UC'] + user_cat1['#act_3_UC']

    print('Completed: 1 of 2')
    # user_cat1

    ################################################################################################################

    # 2 Number of days user is active for this category apart from sales day (Click/Purchase)
    user_cat2 = df[(df.time_stamp!=1111) & (df.label==-1) & ((df.action_type==0) | (df.action_type==2))][['user_id','cat_id','action_type','time_stamp']].drop_duplicates()
    user_cat2 = user_cat2.groupby(['user_id','cat_id','action_type'])['time_stamp'].count().to_frame().rename(columns={'time_stamp':'#unique_days_action'}).reset_index()
    user_cat2

    user_cat2 = user_cat2.pivot_table(index=['user_id','cat_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user_cat2 = pd.DataFrame(user_cat2.to_records())
    user_cat2.columns = ['user_id','cat_id','#days_click_UC','#days_pur_UC']

    print('Completed: 1 of 2')
    # user_cat2

    ################################################################################################################

    print('Few moments more...')
    user_cat = merge(user_cat1,user_cat2,['user_id','cat_id'],'outer')

    del user_cat1
    del user_cat2

    print('Done...')
    end = time.time()
    print('Time taken:',(end - start),'seconds')
    return user_cat