import time
import pandas as pd
import numpy as np
from Utility import *

def age_range(df,nor_data,sales_data):
    # Function for calculating average of a feature.
    # Function for calculating average of a feature.
    def calculate_avg_feature(table,feature_to_work_on,column_names,print_log=False):
        list_ = []
        first_iter_var = table[feature_to_work_on[0]].unique()
        for g in first_iter_var:
            temp_1 = table[table[feature_to_work_on[0]]==g]
            second_iter_var = temp_1[feature_to_work_on[1]].unique()
            for act in second_iter_var:
                l2 = []
                l = table[(table[feature_to_work_on[0]]==g) & (table[feature_to_work_on[1]]==act)].avg_act_count
                l2.append(g)
                l2.append(act)
    #             l2.append(len(l))
                l2.append(np.mean(l))
                if print_log:
                    print(l2)
                list_.append(l2)
                del l2
        return pd.DataFrame(list_,columns=column_names)

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    #                                         NORMAL DATA OF AGE_RANGE

    start = time.time()
    print('Approximately, it takes: 120 seconds')

    # 1.1 #clicks, #add_cart, #purchase, #add_fav from a age_range
    age_range1 = nor_data.groupby(['user_id','age_range','action_type']).agg({'action_type':'count'}).\
                rename(columns={'action_type':'avg_act_count'}).reset_index()
    age_range1 = calculate_avg_feature(age_range1,['age_range','action_type'],['age_range','action_type','avg_act_count_A'])

    age_range1 = age_range1.pivot_table(index=['age_range'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    age_range1 = pd.DataFrame(age_range1.to_records())
    age_range1.columns = ['age_range', '#act_0_nor_A','#act_1_nor_A','#act_2_nor_A','#act_3_nor_A']

    age_range1['tot_acts_nor_A'] = age_range1['#act_0_nor_A'] + age_range1['#act_1_nor_A'] + \
                age_range1['#act_2_nor_A'] + age_range1['#act_3_nor_A']
    print('Completed: 1 of 5...')
    # age_range1

    ################################################################################################################

    # avg p_c ratio of age_range for a brands, cats, item
    age_range2 = nor_data[(nor_data.action_type==0) | (nor_data.action_type==2)].groupby(['user_id','age_range',\
                'action_type']).agg({'item_id':'nunique','cat_id':'nunique','brand_id':'nunique'}).reset_index()

    age_range2 = age_range2.pivot_table(index=['user_id','age_range'],columns=['action_type'],aggfunc=np.sum,\
                                          fill_value=0)
    age_range2 = pd.DataFrame(age_range2.to_records())
    age_range2.columns = ['user_id','age_range','#brands_click_nor_A','#brands_pur_nor_A','#cats_click_nor_A',\
                        '#cats_pur_nor_A', '#items_click_nor_A','#items_pur_nor_A']

    age_range2['brands_p_c_ratio_nor_A'] = age_range2['#brands_pur_nor_A']/age_range2['#brands_click_nor_A']
    age_range2['cats_p_c_ratio_nor_A'] = age_range2['#cats_pur_nor_A']/age_range2['#cats_click_nor_A']
    age_range2['items_p_c_ratio_nor_A'] = age_range2['#items_pur_nor_A']/age_range2['#items_click_nor_A']

    age_range2['brands_p_c_ratio_nor_A'].replace([np.inf, -np.inf], np.nan,inplace=True)
    age_range2['cats_p_c_ratio_nor_A'].replace([np.inf, -np.inf], np.nan,inplace=True)
    age_range2['items_p_c_ratio_nor_A'].replace([np.inf, -np.inf], np.nan,inplace=True)

    age_range2.fillna(age_range2.mean(),inplace=True)

    age_range2 = age_range2.groupby(['age_range']).agg({'brands_p_c_ratio_nor_A':'mean','cats_p_c_ratio_nor_A':\
                                'mean','items_p_c_ratio_nor_A':'mean'}).reset_index()

    print('Completed: 2 of 5...')
    # age_range2


    ################################################################################################################

    age_range_nor = merge(age_range1,age_range2,'age_range','outer')
    del age_range1
    del age_range2
    # age_range_nor

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    #                                         SALES DATA OF AGE_RANGE

    # 1.1 #clicks, #add_cart, #purchase, #add_fav from a age_range
    age_range1 = sales_data.groupby(['user_id','age_range','action_type']).agg({'action_type':'count'}).\
                rename(columns={'action_type':'avg_act_count'}).reset_index()
    age_range1 = calculate_avg_feature(age_range1,['age_range','action_type'],['age_range','action_type','avg_act_count_A'])

    age_range1 = age_range1.pivot_table(index=['age_range'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    age_range1 = pd.DataFrame(age_range1.to_records())
    age_range1.columns = ['age_range', '#act_0_sales_A','#act_1_sales_A','#act_2_sales_A','#act_3_sales_A']

    age_range1['tot_acts_sales_A'] = age_range1['#act_0_sales_A'] + age_range1['#act_1_sales_A'] + \
                age_range1['#act_2_sales_A'] + age_range1['#act_3_sales_A']
    print('Completed: 3 of 5...')
    # age_range1

    ################################################################################################################

    # avg p_c ratio of age_range for a brands, cats, item
    age_range2 = sales_data[(sales_data.action_type==0) | (sales_data.action_type==2)].groupby(['user_id','age_range',\
                'action_type']).agg({'item_id':'nunique','cat_id':'nunique','brand_id':'nunique'}).reset_index()

    age_range2 = age_range2.pivot_table(index=['user_id','age_range'],columns=['action_type'],aggfunc=np.sum,\
                                          fill_value=0)
    age_range2 = pd.DataFrame(age_range2.to_records())
    age_range2.columns = ['user_id','age_range','#brands_click_sales_A','#brands_pur_sales_A','#cats_click_sales_A',\
                        '#cats_pur_sales_A', '#items_click_sales_A','#items_pur_sales_A']

    age_range2['brands_p_c_ratio_sales_A'] = age_range2['#brands_pur_sales_A']/age_range2['#brands_click_sales_A']
    age_range2['cats_p_c_ratio_sales_A'] = age_range2['#cats_pur_sales_A']/age_range2['#cats_click_sales_A']
    age_range2['items_p_c_ratio_sales_A'] = age_range2['#items_pur_sales_A']/age_range2['#items_click_sales_A']

    age_range2['brands_p_c_ratio_sales_A'].replace([np.inf, -np.inf], np.nan,inplace=True)
    age_range2['cats_p_c_ratio_sales_A'].replace([np.inf, -np.inf], np.nan,inplace=True)
    age_range2['items_p_c_ratio_sales_A'].replace([np.inf, -np.inf], np.nan,inplace=True)

    age_range2.fillna(age_range2.mean(),inplace=True)

    age_range2 = age_range2.groupby(['age_range']).agg({'brands_p_c_ratio_sales_A':'mean','cats_p_c_ratio_sales_A':\
                                'mean','items_p_c_ratio_sales_A':'mean'}).reset_index()

    print('Completed: 4 of 5...')
    # age_range2


    ################################################################################################################

    age_range_sales = merge(age_range1,age_range2,'age_range','outer')

    del age_range1
    del age_range2
    # age_range_sales

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    # Number of users in this age_range
    age_range3 = df.groupby(['age_range']).agg({'user_id':'nunique','merchant_id':'nunique'}).\
            rename(columns={'user_id':'#users_A','merchant_id':'#mer_A'}).reset_index()
    print('Completed: 5 of 5...')
    # age_range3

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    print('Few moments more...')
    age_range = pd.merge(age_range3,age_range_nor,on='age_range')
    age_range = pd.merge(age_range,age_range_sales,on='age_range')
    print('Done...')
    end = time.time()
    print('Time taken:',(end - start),'seconds')
    return age_range

