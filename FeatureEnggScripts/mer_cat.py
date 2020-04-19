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
    
    print('Extracting info regarding cat...')
    # 1.1 #clicks, #add_cart, #purchase, #add_fav from a cat
    cat1 = df.groupby(['cat_id','action_type'])\
                    ['action_type'].count().to_frame().rename(columns={'action_type':'action_count'}).reset_index()

    cat1 = cat1.pivot_table(index=['cat_id'],columns=['action_type'],aggfunc=np.sum,fill_value=0)
    cat1 = pd.DataFrame(cat1.to_records())
    cat1.columns = ['cat_id','#act_0_C','#act_1_C','#act_2_C','#act_3_C']

    # -------------------------------------------------------------------------------------------------------------------- #
    
    # 1.2 Number of old repeated user associated with cat
    cat2 = df[df.label==-1].groupby(['cat_id']).agg({'user_id':'nunique','merchant_id':'nunique'}).\
                            reset_index().rename(columns={'user_id':'#old_buyer_C','merchant_id':'#mer_associated_C'})

    # -------------------------------------------------------------------------------------------------------------------- #
    cats = merge(cat1,cat2,'cat_id','outer')
    del cat1
    del cat2
    # cats
    
    # -------------------------------------------------------------------------------------------------------------------- #
    # -------------------------------------------------------------------------------------------------------------------- #
    return cats,merchant


def mer_cat(df):
    
    start = time.time()
    print('Approximately, it takes: 110 seconds')
    cat,merchant = man_(df)

    # 1. #clicks, #add_cart, #purchase, #add_fav
    mer_cat1 = df.groupby(['merchant_id','cat_id','action_type']).agg({'action_type':'count'}).\
                            rename(columns={'action_type':'action_count'}).reset_index()

    mer_cat1 = mer_cat1.pivot_table(index=['merchant_id','cat_id'],columns=['action_type'],\
                                                  aggfunc=np.sum,fill_value=0)
    mer_cat1 = pd.DataFrame(mer_cat1.to_records())
    mer_cat1.columns = ['merchant_id','cat_id','#act_0_MC','#act_1_MC','#act_2_MC','#act_3_MC']
    mer_cat1['tot_acts_MC'] = mer_cat1['#act_0_MC'] + mer_cat1['#act_1_MC'] + mer_cat1['#act_2_MC'] +\
                                    mer_cat1['#act_3_MC']

    print('Completed: 1 of 2...')
    # mer_cat1

    ################################################################################################################

    # 2. Calculating number of repeated buyers of the cat from the merchant
    mer_cat2 = df[df.label==-1].groupby(['merchant_id','cat_id']).agg({'user_id':'nunique'}).\
                        rename(columns={'user_id':'#buyers_MC'}).reset_index()
    print('Completed: 2 of 2...')
    # mer_cat2

    ################################################################################################################

    print('Few moments more...')
    mer_cat = merge(mer_cat1,mer_cat2,['merchant_id','cat_id'],'outer')

    del mer_cat1
    del mer_cat2
    
    ###############################################################################################################
    
    print('Updating mer_cat...')

    # 3. Calculating number of purchase from the cat & number of buyers of the cat from 'cat' & adding it to MC
    mer_cat = pd.merge(mer_cat,cat[['cat_id','#act_2_C','#old_buyer_C']],on='cat_id',how='outer')

    # 4. Calculating total number of purchase from the merchant & number of buyers of the cat from 'cat' & adding it to M
    mer_cat = pd.merge(mer_cat,merchant[['merchant_id','#act_2_M','#old_buyer_M']],on='merchant_id',how='outer')
    mer_cat.fillna(0,inplace=True)
    '''
    #act_2_MC : Number of purchase of the cat from the merchant
    #act_2_C  : Number of purchase of the cat
    #act_2_M  : Number of purchase of the merchant

    #Buyers_cat_Mer  : Number of buyers of the cat from the merchant 
    #Old_buyer_C : Number of buyers of the cat
    #Old_buyer_M     : Number of buyers of the merchant

    '''

    # 5. How important a cat is to a merchant.

    #     5.1 Merchant's market share on the cat.
    mer_cat['M_mkt_share_C'] = mer_cat['#act_2_MC']/mer_cat['#act_2_C']

    #     5.2 Merchant user share on the cat.
    mer_cat['M_user_share_C'] = mer_cat['#buyers_MC']/mer_cat['#old_buyer_C']


    # 6. How important a merchant is to a cat.

    #     6.1 cat's market share on the cat.
    mer_cat['C_mkt_share_M'] = mer_cat['#act_2_MC']/mer_cat['#act_2_M']


    #     6.2 cat's user share within the market.
    mer_cat['C_user_share_M'] = mer_cat['#buyers_MC']/mer_cat['#old_buyer_M']

    # --------------------------------------------------------------------------------------------------------------- #

    # Dropping unecessary column (Which are used from other tables)
    mer_cat = mer_cat.drop(columns = ['#act_2_C','#act_2_M','#old_buyer_C','#old_buyer_M'],axis=1)
#     mer_cat.replace([np.inf,-np.inf],np.nan,inplace=True)
    mer_cat.fillna(0,inplace=True)
    print(miss(mer_cat))
    # mer_cat

    print('Done...')
    end = time.time()
    print('Time taken:',(end - start),'seconds')
    return mer_cat
