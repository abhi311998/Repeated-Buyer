import time
import pandas as pd
import numpy as np
from Utility import *

def brand(df):
    start = time.time()
    print('Last time, it takes: 40 seconds')

    # 1.1 #clicks, #add_cart, #purchase, #add_fav from a brand
    brand1 = df[(df.label==-1) & (df.time_stamp!=1111)].groupby(['brand_id','action_type'])['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()

    brand1 = brand1.pivot_table(index=['brand_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    brand1 = pd.DataFrame(brand1.to_records())
    brand1.columns = ['brand_id','#act_0_B','#act_1_B','#act_2_B','#act_3_B']
    brand1['tot_acts_B'] = brand1['#act_0_B'] + brand1['#act_1_B'] + brand1['#act_2_B'] + brand1['#act_3_B']
    # brand1['#act_0_B'] = brand1['#act_0_B']/brand1['tot_acts_B']
    # brand1['#act_1_B'] = brand1['#act_1_B']/brand1['tot_acts_B']
    # brand1['#act_2_B'] = brand1['#act_2_B']/brand1['tot_acts_B']
    # brand1['#act_3_B'] = brand1['#act_3_B']/brand1['tot_acts_B']
    # brand1.drop('tot_acts_B',axis=1,inplace=True)

    print('Completed: 1 of 2')
    # brand1

    ################################################################################################################

    # 1.2 Number of old repeated user associated with brand
    brand2 = df[(df.label==-1) & (df.time_stamp!=1111)].groupby(['brand_id']).agg({'user_id':'nunique','merchant_id':'nunique'}).reset_index().\
                        rename(columns={'user_id':'#old_buyer_B','merchant_id':'#mer_associated_B'})
    print('Completed: 2 of 2')
    # brand2

    ################################################################################################################

    print('Few moments more...')
    brand = merge(brand1,brand2,'brand_id','outer')

    del brand1
    del brand2

    print('Done...')
    end = time.time()
    print('Time taken:',(end - start),'seconds')
    return brand