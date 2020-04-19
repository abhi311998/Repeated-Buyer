import time
import pandas as pd
import numpy as np
from Utility import *

def man_(df):
    # -------------------------------------------------------------------------------------------------------------------- #
    # -------------------------------------------------------------------------------------------------------------------- #
    
    print('Extracting info about merchant...')
    # 2.1 #clicks, #add_cart, #purchase, #add_fav from a merchant
    merchant1 = df.groupby(['merchant_id','action_type'])\
                    ['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()

    merchant1 = merchant1.pivot_table(index=['merchant_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    merchant1 = pd.DataFrame(merchant1.to_records())
    merchant1.columns = ['merchant_id','#act_0_M','#act_1_M','#act_2_M','#act_3_M']

    # -------------------------------------------------------------------------------------------------------------------- #
    # Number of old user related to merchant
    merchant2 = df[df.label==-1].groupby(['merchant_id']).agg({'user_id':'nunique'}).\
                rename(columns={'user_id':'#old_buyer_M'}).reset_index()

    # -------------------------------------------------------------------------------------------------------------------- #
    merchant = merge(merchant1,merchant2,'merchant_id','outer')
    del merchant1
    del merchant2
    # merchant
    # -------------------------------------------------------------------------------------------------------------------- #
    # -------------------------------------------------------------------------------------------------------------------- #
    
    print('Extracting info regarding brand...')
    # 1.1 #clicks, #add_cart, #purchase, #add_fav from a brand
    brand1 = df.groupby(['brand_id','action_type'])\
                    ['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()

    brand1 = brand1.pivot_table(index=['brand_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    brand1 = pd.DataFrame(brand1.to_records())
    brand1.columns = ['brand_id','#act_0_B','#act_1_B','#act_2_B','#act_3_B']

    # -------------------------------------------------------------------------------------------------------------------- #
    
    # 1.2 Number of old repeated user associated with brand
    brand2 = df[df.label==-1].groupby(['brand_id']).agg({'user_id':'nunique','merchant_id':'nunique'}).\
                            reset_index().rename(columns={'user_id':'#old_buyer_B','merchant_id':'#mer_associated_B'})

    # -------------------------------------------------------------------------------------------------------------------- #
    brands = merge(brand1,brand2,'brand_id','outer')
    del brand1
    del brand2
    # brands
    
    # -------------------------------------------------------------------------------------------------------------------- #
    # -------------------------------------------------------------------------------------------------------------------- #
    return brands,merchant


def mer_brand(df):
    
    start = time.time()
    print('Approximately, it takes: 100 seconds')
    brands,merchant = man_(df)

    # 1. #clicks, #add_cart, #purchase, #add_fav
    mer_brand1 = df.groupby(['merchant_id','brand_id','action_type']).agg({'action_type':'count'}).\
                            rename(columns={'action_type':'action_count'}).reset_index()

    mer_brand1 = mer_brand1.pivot_table(index=['merchant_id','brand_id'],columns=['action_type'],\
                                                  aggfunc=np.sum,fill_value=0)
    mer_brand1 = pd.DataFrame(mer_brand1.to_records())
    mer_brand1.columns = ['merchant_id','brand_id','#act_0_MB','#act_1_MB','#act_2_MB','#act_3_MB']
    mer_brand1['tot_acts_MB'] = mer_brand1['#act_0_MB'] + mer_brand1['#act_1_MB'] + mer_brand1['#act_2_MB'] +\
                                    mer_brand1['#act_3_MB']

    print('Completed: 1 of 2...')
    # mer_brand1

    ################################################################################################################

    # 2. Calculating number of repeated buyers of the brand from the merchant
    mer_brand2 = df[df.label==-1].groupby(['merchant_id','brand_id']).agg({'user_id':'nunique'}).\
                        rename(columns={'user_id':'#buyers_MB'}).reset_index()
    print('Completed: 2 of 2...')
    # mer_brand2

    ################################################################################################################

    print('Few moments more...')
    mer_brand = merge(mer_brand1,mer_brand2,['merchant_id','brand_id'],'outer')

    del mer_brand1
    del mer_brand2
    
    ###############################################################################################################
    
    print('Updating mer_brand...')

    # 3. Calculating number of purchase from the brand & number of buyers of the brand from 'brand' & adding it to MC
    mer_brand = pd.merge(mer_brand,brands[['brand_id','#act_2_B','#old_buyer_B']],on='brand_id',how='outer')

    # 4. Calculating total number of purchase from the merchant & number of buyers of the brand from 'brand' & adding it to M
    mer_brand = pd.merge(mer_brand,merchant[['merchant_id','#act_2_M','#old_buyer_M']],on='merchant_id',how='outer')
    mer_brand.fillna(0,inplace=True)
    '''
    #act_2_MB : Number of purchase of the brand from the merchant
    #act_2_B  : Number of purchase of the brand
    #act_2_M  : Number of purchase of the merchant

    #Buyers_brand_Mer  : Number of buyers of the brand from the merchant 
    #Old_buyer_B : Number of buyers of the brand
    #Old_buyer_M     : Number of buyers of the merchant

    '''

    # 5. How important a brand is to a merchant.

    #     5.1 Merchant's market share on the brand.
    mer_brand['M_mkt_share_B'] = mer_brand['#act_2_MB']/mer_brand['#act_2_B']

    #     5.2 Merchant user share on the brand.
    mer_brand['M_user_share_B'] = mer_brand['#buyers_MB']/mer_brand['#old_buyer_B']


    # 6. How important a merchant is to a brand.

    #     6.1 brand's market share on the brand.
    mer_brand['B_mkt_share_M'] = mer_brand['#act_2_MB']/mer_brand['#act_2_M']


    #     6.2 brand's user share within the market.
    mer_brand['B_user_share_M'] = mer_brand['#buyers_MB']/mer_brand['#old_buyer_M']

    # --------------------------------------------------------------------------------------------------------------- #

    # Dropping unecessary column (Which are used from other tables)
    mer_brand = mer_brand.drop(columns = ['#act_2_B','#act_2_M','#old_buyer_B','#old_buyer_M'],axis=1)
#     mer_brand.replace([np.inf,-np.inf],np.nan,inplace=True)
    mer_brand.fillna(0,inplace=True)      # cos there will be no mkt share or user share later.
    print(miss(mer_brand))
    # mer_brand

    print('Done...')
    end = time.time()
    print('Time taken:',(end - start),'seconds')
    return mer_brand
