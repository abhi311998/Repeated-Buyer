import time
import pandas as pd
import numpy as np

from Utility import *


def pipeline():
    print('For this process, it takes approximately 30 minutes. So sit back quitely while the process goes....')
    start_ = time.time()
    print('############################################################################################')
    # ----------------------------------------------------------------------------------------------------------- #
    # ----------------------------------------- PREPARING DATA FROM RAW ----------------------------------------- #
    # ----------------------------------------------------------------------------------------------------------- #

    start = time.time()
    print('Preparing data from raw...')
    print('Approximately, it takes: 145 seconds')

    # Preparaing user_log from data_format1
    user_info = pd.read_csv('data_format1/user_info_format1.csv')
    user_log = pd.read_csv('data_format1/user_log_format1.csv')
    user_log = pd.merge(user_info,user_log,on='user_id')
    del user_info
    user_log = user_log.rename(columns={'seller_id':'merchant_id'})
    user_log

    # ---------------------------------------------------------------------------------------------------------------- #

    # Preparing user-merchant-label triplet form format2
    train_format_2 = pd.read_csv('data_format2/train_format2.csv')
    test_format_2 = pd.read_csv('data_format2/test_format2.csv')
    df = pd.concat([train_format_2,test_format_2])
    del train_format_2
    del test_format_2
    df = df[['user_id','merchant_id','label']]
    df

    # ---------------------------------------------------------------------------------------------------------------- #

    df = pd.merge(user_log,df,on=['user_id','merchant_id'])
    del user_log
    df

    # ---------------------------------------------------------------------------------------------------------------- #

    # Dealing with null values in forllowing columns
    df.brand_id.fillna(0,inplace=True)
    df.age_range.fillna(0,inplace=True)
    df.gender.fillna(2,inplace=True)

    # ---------------------------------------------------------------------------------------------------------------- #

    # Adding more columns which are going to be used in analysis/feature generation
    # Date/Month column
    df['month']=df.time_stamp//100
    df['day'] = df.time_stamp%100

    # Age_gender column formation
    df['age_range'] = df['age_range'].astype(int)
    df['gender'] = df['gender'].astype(int)
    # Age_gender
    df['age_gender'] = df['age_range'] + (0.1 * df['gender'])

    # # Old pair reflects that u-m pair which had continued their trade even on sales day.
    df['old_um'] = [1 if x == -1 else 0 for x in df.label]


    ############################################################################################
    ############################################################################################
    # Normal day data/Sales day data
    nor_data = df[(df.label==-1) & (df.time_stamp!=1111)]
    sales_data = df[(df.label!=-1) | ((df.label==-1) & (df.time_stamp==1111))]

    print('Time taken:',time.time()-start)
    print('Done...')
    print('############################################################################################')
    # df


    # ----------------------------------------------------------------------------------------------------- #
    # ---------------------------- PREPARING DATA THAT WILL GO INTO THE MODEL ----------------------------- #
    # ----------------------------------------------------------------------------------------------------- #

    from FeatureEnggScripts import gender
    print('Creating gender behavioural data...')
    gender = gender.gender(df,nor_data,sales_data)
    print('############################################################################################')
    # gender

    # ---------------------------------------------------------------------------------------------------- #

    from FeatureEnggScripts import age_range
    print('Creating age_range behavioural data...')
    age_range = age_range.age_range(df,nor_data,sales_data)
    print('############################################################################################')
    # age_range

    # ---------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------- #

    from FeatureEnggScripts import user
    print('Creating user behavioural data...')
    # Adding gender/age of the user
    user_info = df[['user_id','gender','age_range']].drop_duplicates()
    # user_info
    user = user.user(df,nor_data,sales_data)

    # Merging gender/age raleated data with user
    user = pd.merge(user_info,user,on='user_id')
    user = pd.merge(user,gender,on='gender')
    user = pd.merge(user,age_range,on='age_range')
    del gender
    del age_range
    print('############################################################################################')
    # user

    # ---------------------------------------------------------------------------------------------------- #

    from FeatureEnggScripts import merchant
    print('Creating merchant behavioural data...')
    merchant = merchant.merchant(df,nor_data,sales_data)
    print('############################################################################################')
    # merchant

    # ---------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------- #

    print('############################################################################################')
    print('############################################################################################')
    print('############################################################################################')

    print('Preparing User-Merchant pair wise information...')
    print('Approximately: it takes 1500 seconds')
    start = time.time()

    # ------------------------------------------------------------------------------------------------------------ #

    from FeatureEnggScripts import mer_cat
    print('Creating merchant-cat related data...')
    mer_cat = mer_cat.mer_cat(df)
    # mer_cat
    mer_cat['#act_0_MC'] = mer_cat['#act_0_MC']/mer_cat['tot_acts_MC']
    mer_cat['#act_1_MC'] = mer_cat['#act_1_MC']/mer_cat['tot_acts_MC']
    mer_cat['#act_2_MC'] = mer_cat['#act_2_MC']/mer_cat['tot_acts_MC']
    mer_cat['#act_3_MC'] = mer_cat['#act_3_MC']/mer_cat['tot_acts_MC']
    print('############################################################################################')
    # mer_cat

    from FeatureEnggScripts import mer_brand
    print('Creating merchant-brand related data...')
    mer_brand = mer_brand.mer_brand(df)
    # mer_brand
    mer_brand['#act_0_MB'] = mer_brand['#act_0_MB']/mer_brand['tot_acts_MB']
    mer_brand['#act_1_MB'] = mer_brand['#act_1_MB']/mer_brand['tot_acts_MB']
    mer_brand['#act_2_MB'] = mer_brand['#act_2_MB']/mer_brand['tot_acts_MB']
    mer_brand['#act_3_MB'] = mer_brand['#act_3_MB']/mer_brand['tot_acts_MB']
    print('############################################################################################')
    # mer_brand

    # ------------------------------------------------------------------------------------------------------------- #

    from FeatureEnggScripts import user_cat
    print('Creating user-cat related data...')
    user_cat = user_cat.user_cat(df)
    # user_cat
    user_cat['#act_0_UC'] = user_cat['#act_0_UC']/user_cat['tot_acts_UC']
    user_cat['#act_1_UC'] = user_cat['#act_1_UC']/user_cat['tot_acts_UC']
    user_cat['#act_2_UC'] = user_cat['#act_2_UC']/user_cat['tot_acts_UC']
    user_cat['#act_3_UC'] = user_cat['#act_3_UC']/user_cat['tot_acts_UC']
    print('############################################################################################')
    # user_cat

    from FeatureEnggScripts import user_brand
    print('Creating user-brand related data...')
    user_brand = user_brand.user_brand(df)
    # user_brand
    user_brand['#act_0_UB'] = user_brand['#act_0_UB']/user_brand['tot_acts_UB']
    user_brand['#act_1_UB'] = user_brand['#act_1_UB']/user_brand['tot_acts_UB']
    user_brand['#act_2_UB'] = user_brand['#act_2_UB']/user_brand['tot_acts_UB']
    user_brand['#act_3_UB'] = user_brand['#act_3_UB']/user_brand['tot_acts_UB']
    print('############################################################################################')
    # user_brand

    # ------------------------------------------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------- #

    um = df[df.label!=-1][['user_id','merchant_id','label']].drop_duplicates()

    # User_Merchant_Cat
    print('User-Merchant-Category...')
    umc = pd.merge(um[['user_id','merchant_id']],user_cat,on='user_id')
    umc = pd.merge(umc,mer_cat,on=['merchant_id','cat_id'])
    umc.drop(['#days_click_UC','#days_pur_UC', '#buyers_MC'],axis=1,inplace=True)
    umc['sim_score_UMC'] = umc.apply(lambda x: sim_score(np.array(x[3:8]),np.array(x[8:13])),axis=1)
    # umc.to_csv('Data/umc_with_sim_score_without_agg.csv',index=False)
    # umc = pd.read_csv('data/umc_with_sim_score_without_agg.csv')
    umc1 = umc.groupby(['user_id','merchant_id']).agg({'M_mkt_share_C':'mean','M_user_share_C':'mean',\
                        'C_mkt_share_M':'mean', 'C_user_share_M':'mean','sim_score_UMC':'mean'}).\
                        rename(columns={'M_mkt_share_C':'M_mkt_share_mean_C','M_user_share_C':'M_user_share_mean_C',\
                        'C_mkt_share_M':'C_mkt_share_mean_M', 'C_user_share_M':'C_user_share_mean_M',\
                        'sim_score_UMC':'sim_score_mean_UMC'}).reset_index()
    umc2 = umc.groupby(['user_id','merchant_id']).agg({'M_mkt_share_C':'max','M_user_share_C':'max',\
                        'C_mkt_share_M':'max', 'C_user_share_M':'max','sim_score_UMC':'max'}).\
                        rename(columns={'M_mkt_share_C':'M_mkt_share_max_C','M_user_share_C':'M_user_share_max_C',\
                        'C_mkt_share_M':'C_mkt_share_max_M', 'C_user_share_M':'C_user_share_max_M',\
                        'sim_score_UMC':'sim_score_max_UMC'}).reset_index()
    umc = pd.merge(umc1,umc2,on=['user_id','merchant_id'])
    print('############################################################################################')
    # umc

    # User_Merchant_Brand
    print('User-Merchant-Brand...')
    umb = pd.merge(um[['user_id','merchant_id']],user_brand,on='user_id')
    umb = pd.merge(umb,mer_brand,on=['merchant_id','brand_id'])
    umb.drop(['#days_click_UB','#days_pur_UB', '#buyers_MB'],axis=1,inplace=True)

    umb['sim_score_UMB'] = umb.apply(lambda x: sim_score(np.array(x[3:8]),np.array(x[8:13])),axis=1)
    # umb.to_csv('Data/umb_with_sim_score_without_agg.csv',index=False)
    # umb = pd.read_csv('data/umb_with_sim_score_without_agg.csv')
    umb1 = umb.groupby(['user_id','merchant_id']).agg({'M_mkt_share_B':'mean','M_user_share_B':'mean',\
                        'B_mkt_share_M':'mean', 'B_user_share_M':'mean','sim_score_UMB':'mean'}).\
                        rename(columns={'M_mkt_share_B':'M_mkt_share_mean_B','M_user_share_B':'M_user_share_mean_B',\
                        'B_mkt_share_M':'B_mkt_share_mean_M', 'B_user_share_M':'B_user_share_mean_M',\
                        'sim_score_UMB':'sim_score_mean_UMB'}).reset_index()
    umb2 = umb.groupby(['user_id','merchant_id']).agg({'M_mkt_share_B':'max','M_user_share_B':'max',\
                        'B_mkt_share_M':'max', 'B_user_share_M':'max','sim_score_UMB':'max'}).\
                        rename(columns={'M_mkt_share_B':'M_mkt_share_max_B','M_user_share_B':'M_user_share_max_B',\
                        'B_mkt_share_M':'B_mkt_share_max_M', 'B_user_share_M':'B_user_share_max_M',\
                        'sim_score_UMB':'sim_score_max_UMB'}).reset_index()
    umb = pd.merge(umb1,umb2,on=['user_id','merchant_id'])
    print('############################################################################################')
    # umb

    # ------------------------------------------------------------------------------------------------------------- #

    print('Little more time...')
    umbc = pd.merge(umc,umb,on=['user_id','merchant_id'])
    # umbc.to_csv('data/umbc.csv',index=False)
    del umc
    del umb
    del user_brand
    del user_cat
    del mer_cat
    del mer_brand
    # umbc 

    ############################################################################################################
    ############################################################################################################

    # User-merchant pair actions related data
    from FeatureEnggScripts import user_mer
    user_mer = user_mer.user_mer(df)
    # user_mer

    user_mer = pd.merge(user_mer,umbc,on=['user_id','merchant_id'])
    del umbc
    # user_mer


    # --------------------------------------------------------------------------------------------------------- #
    # ----------------------------------------- PREPARING FINAL DATA ------------------------------------------ #
    # --------------------------------------------------------------------------------------------------------- #

    data = pd.merge(um,user,on='user_id')
    data = pd.merge(data,merchant,on='merchant_id')
    data = pd.merge(data,user_mer,on=['user_id','merchant_id'])
    del user
    del merchant
    del user_mer

    print('############################################################################################')
    print('############################################################################################')
    print('Overall time taken:',time.time()-start_)
    print('############################################################################################')
    print('############################################################################################')

    return data