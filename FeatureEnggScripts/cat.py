import time
import pandas as pd
import numpy as np
from Utility import *

def cat(df):
    start = time.time()
    print('Approximately, it takes: 40 seconds')

    # 1.1 #clicks, #add_cart, #purchase, #add_fav from a cat
    cat1 = df[(df.label==-1) & (df.time_stamp!=1111)].groupby(['cat_id','action_type'])['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()

    cat1 = cat1.pivot_table(index=['cat_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    cat1 = pd.DataFrame(cat1.to_records())
    cat1.columns = ['cat_id','#act_0_C','#act_1_C','#act_2_C','#act_3_C']
    cat1['tot_acts_C'] = cat1['#act_0_C'] + cat1['#act_1_C'] + cat1['#act_2_C'] + cat1['#act_3_C']
    # cat1['#act_0_C'] = cat1['#act_0_C']/cat1['tot_acts_C']
    # cat1['#act_1_C'] = cat1['#act_1_C']/cat1['tot_acts_C']
    # cat1['#act_2_C'] = cat1['#act_2_C']/cat1['tot_acts_C']
    # cat1['#act_3_C'] = cat1['#act_3_C']/cat1['tot_acts_C']
    # cat1.drop('tot_acts_C',axis=1,inplace=True)

    print('Completed: 1 of 2')
    # cat1

    ################################################################################################################

    # 1.2 Number of old repeated user associated with cat
    cat2 = df[(df.label==-1) & (df.time_stamp!=1111)].groupby(['cat_id']).agg({'user_id':'nunique','merchant_id':'nunique'}).reset_index().\
                        rename(columns={'user_id':'#old_buyer_C','merchant_id':'#mer_associated_C'})
    print('Completed: 2 of 2')
    # cat2

    ################################################################################################################

    print('Few moments more...')
    cat = merge(cat1,cat2,'cat_id','outer')

    del cat1
    del cat2

    print('Done...')
    end = time.time()
    print('Time taken:',(end - start),'seconds')
    return cat