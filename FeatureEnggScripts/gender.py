import time
import pandas as pd
import numpy as np
from Utility import *

def gender(df,nor_data,sales_data):
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

    #                                         NORMAL DATA OF GENDER

    start = time.time()
    print('Approximately, it takes: 120 seconds')

    # 1.1 #clicks, #add_cart, #purchase, #add_fav from a gender
    gender1 = nor_data.groupby(['user_id','gender','action_type']).agg({'action_type':'count'}).\
                rename(columns={'action_type':'avg_act_count'}).reset_index()
    gender1 = calculate_avg_feature(gender1,['gender','action_type'],['gender','action_type','avg_act_count_G'])

    gender1 = gender1.pivot_table(index=['gender'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    gender1 = pd.DataFrame(gender1.to_records())
    gender1.columns = ['gender', '#act_0_nor_G','#act_1_nor_G','#act_2_nor_G','#act_3_nor_G']

    gender1['tot_acts_nor_G'] = gender1['#act_0_nor_G'] + gender1['#act_1_nor_G'] + \
                gender1['#act_2_nor_G'] + gender1['#act_3_nor_G']
    print('Completed: 1 of 5...')
    # gender1

    ################################################################################################################

    # avg p_c ratio of gender for a brands, cats, item
    gender2 = nor_data[(nor_data.action_type==0) | (nor_data.action_type==2)].groupby(['user_id','gender',\
                'action_type']).agg({'item_id':'nunique','cat_id':'nunique','brand_id':'nunique'}).reset_index()

    gender2 = gender2.pivot_table(index=['user_id','gender'],columns=['action_type'],aggfunc=np.sum,\
                                          fill_value=0)
    gender2 = pd.DataFrame(gender2.to_records())
    gender2.columns = ['user_id','gender','#brands_click_nor_G','#brands_pur_nor_G','#cats_click_nor_G',\
                        '#cats_pur_nor_G', '#items_click_nor_G','#items_pur_nor_G']

    gender2['brands_p_c_ratio_nor_G'] = gender2['#brands_pur_nor_G']/gender2['#brands_click_nor_G']
    gender2['cats_p_c_ratio_nor_G'] = gender2['#cats_pur_nor_G']/gender2['#cats_click_nor_G']
    gender2['items_p_c_ratio_nor_G'] = gender2['#items_pur_nor_G']/gender2['#items_click_nor_G']

    gender2['brands_p_c_ratio_nor_G'].replace([np.inf, -np.inf], np.nan,inplace=True)
    gender2['cats_p_c_ratio_nor_G'].replace([np.inf, -np.inf], np.nan,inplace=True)
    gender2['items_p_c_ratio_nor_G'].replace([np.inf, -np.inf], np.nan,inplace=True)

    gender2.fillna(gender2.mean(),inplace=True)

    gender2 = gender2.groupby(['gender']).agg({'brands_p_c_ratio_nor_G':'mean','cats_p_c_ratio_nor_G':\
                                'mean','items_p_c_ratio_nor_G':'mean'}).reset_index()

    print('Completed: 2 of 5...')
    # gender2


    ################################################################################################################

    gender_nor = merge(gender1,gender2,'gender','outer')
    del gender1
    del gender2
    # gender_nor

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    #                                         SALES DATA OF GENDER

    # 1.1 #clicks, #add_cart, #purchase, #add_fav from a gender
    gender1 = sales_data.groupby(['user_id','gender','action_type']).agg({'action_type':'count'}).\
                rename(columns={'action_type':'avg_act_count'}).reset_index()
    gender1 = calculate_avg_feature(gender1,['gender','action_type'],['gender','action_type','avg_act_count_G'])

    gender1 = gender1.pivot_table(index=['gender'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    gender1 = pd.DataFrame(gender1.to_records())
    gender1.columns = ['gender', '#act_0_sales_G','#act_1_sales_G','#act_2_sales_G','#act_3_sales_G']

    gender1['tot_acts_sales_G'] = gender1['#act_0_sales_G'] + gender1['#act_1_sales_G'] + \
                gender1['#act_2_sales_G'] + gender1['#act_3_sales_G']
    print('Completed: 3 of 5...')
    # gender1

    ################################################################################################################

    # avg p_c ratio of gender for a brands, cats, item
    gender2 = sales_data[(sales_data.action_type==0) | (sales_data.action_type==2)].groupby(['user_id','gender',\
                'action_type']).agg({'item_id':'nunique','cat_id':'nunique','brand_id':'nunique'}).reset_index()

    gender2 = gender2.pivot_table(index=['user_id','gender'],columns=['action_type'],aggfunc=np.sum,\
                                          fill_value=0)
    gender2 = pd.DataFrame(gender2.to_records())
    gender2.columns = ['user_id','gender','#brands_click_sales_G','#brands_pur_sales_G','#cats_click_sales_G',\
                        '#cats_pur_sales_G', '#items_click_sales_G','#items_pur_sales_G']

    gender2['brands_p_c_ratio_sales_G'] = gender2['#brands_pur_sales_G']/gender2['#brands_click_sales_G']
    gender2['cats_p_c_ratio_sales_G'] = gender2['#cats_pur_sales_G']/gender2['#cats_click_sales_G']
    gender2['items_p_c_ratio_sales_G'] = gender2['#items_pur_sales_G']/gender2['#items_click_sales_G']

    gender2['brands_p_c_ratio_sales_G'].replace([np.inf, -np.inf], np.nan,inplace=True)
    gender2['cats_p_c_ratio_sales_G'].replace([np.inf, -np.inf], np.nan,inplace=True)
    gender2['items_p_c_ratio_sales_G'].replace([np.inf, -np.inf], np.nan,inplace=True)

    gender2.fillna(gender2.mean(),inplace=True)

    gender2 = gender2.groupby(['gender']).agg({'brands_p_c_ratio_sales_G':'mean','cats_p_c_ratio_sales_G':\
                                'mean','items_p_c_ratio_sales_G':'mean'}).reset_index()

    print('Completed: 4 of 5...')
    # gender2


    ################################################################################################################

    gender_sales = merge(gender1,gender2,'gender','outer')

    del gender1
    del gender2
    # gender_sales

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    # Number of users in this gender
    gender3 = df.groupby(['gender']).agg({'user_id':'nunique','merchant_id':'nunique'}).\
            rename(columns={'user_id':'#users_G','merchant_id':'#mer_G'}).reset_index()
    print('Completed: 5 of 5...')
    # gender3

    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    print('Few moments more...')
    gender = pd.merge(gender3,gender_nor,on='gender')
    gender = pd.merge(gender,gender_sales,on='gender')
    print('Done...')
    end = time.time()
    print('Time taken:',(end - start),'seconds')
    return gender