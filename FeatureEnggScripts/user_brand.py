import time
import pandas as pd
import numpy as np
from Utility import *

def user_brand(df):
    start = time.time()
    print('Approximately, it takes: 150 seconds')

    # 1 #clicks, #add_cart, #purchase, #add_fav
    user_brand1 = df.groupby(['user_id','brand_id','action_type'])['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()
    # user_brand1

    user_brand1 = user_brand1.pivot_table(index=['user_id','brand_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user_brand1 = pd.DataFrame(user_brand1.to_records())
    user_brand1.columns = ['user_id','brand_id','#act_0_UB','#act_1_UB','#act_2_UB','#act_3_UB']

    user_brand1['tot_acts_UB'] = user_brand1['#act_0_UB'] + user_brand1['#act_1_UB'] + user_brand1['#act_2_UB'] + user_brand1['#act_3_UB']

    print('Completed: 1 of 2')
    # user_brand1

    ################################################################################################################

    # 2 Number of days user is active for this brandegory apart from sales day (Click/Purchase)
    user_brand2 = df[(df.time_stamp!=1111) & (df.label==-1) & ((df.action_type==0) | (df.action_type==2))].\
                groupby(['user_id','brand_id','action_type']).agg({'time_stamp':'nunique'}).\
                rename(columns={'time_stamp':'#unique_days_action'}).reset_index()

    user_brand2 = user_brand2.pivot_table(index=['user_id','brand_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    user_brand2 = pd.DataFrame(user_brand2.to_records())
    user_brand2.columns = ['user_id','brand_id','#days_click_UB','#days_pur_UB']

    print('Completed: 1 of 2')
    # user_brand2

    ################################################################################################################

    print('Few moments more...')
    user_brand = merge(user_brand1,user_brand2,['user_id','brand_id'],'outer')

    del user_brand1
    del user_brand2

    print('Done...')
    end = time.time()
    print('Time taken:',(end - start),'seconds')
    return user_brand