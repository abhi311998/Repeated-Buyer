# Repeated-Buyer
*Internship Project*

There is an E-Commerce website which hosts a Sales Day on 11 Nov and to attract new buyers towards the merchant
We need to predict the probability that the new buyer would purchase items from the same merchants again within 6 months


## Overview
Large business-to-consumer (B2C) e-commerce websites, such as Amazon and Alibaba, often run nationwide sales promotions on special days like Black Friday and Double 11 (Singles’ Day). Merchants offer great discounts to lure new customers. Merchants acquire new customers during these events. However, most new customers are one-time deal hunters, and promotions to them usually do not generate a return on investment (ROI) as expected by merchants. Therefore, merchants need to identify potential loyal ones from these new customers, so as to conduct targeted advertisements (and promotions) towards them to lower the promotion cost. It is difficult for any individual merchant to identify it's potential loyal customers as it has little information on its new customers. B2C e-commerce websites instead have the clickstream data and purchase history of all the customers at all the merchants on their platforms. Thus, they can learn the preferences and habits of the new customers from their historical data, and then predict how likely a new customer will buy again from the same merchant.

Click-stream data of 6 months are provided starting from 5 May to 11 Nov (which is the sales day).

## Why repeat buyers?
Well, mainly there are following 6 reasons why the companies focus more on customer loyalty and they spending much for this:
1. Acquisition of new buyers takes more effort and cost as compared to the retention of existing buyers for a merchant.
2. Loyal buyers are supposed to buy items from the merchant regularly and also in more amounts than that by the new buyers.
3. Selling new products to the existing buyer is easier as compared to that to new buyers because loyal buyers do not have trust issues with the merchant.
4. Promotion or marketing cost is comparatively low for loyal buyers with respect to the new buyers.
5. Loyal buyers are already much familiar with the services of the merchant so it helps the merchant to minimise their service cost.
6. Loyal buyers tend to give positive feedback of the products to other buyers which helps in improving the brand value of the merchant.

## Business Understanding of the problem
For any E-commerce website, it is not only the buyers who are i n the focus of getting good deals, but also the merchants who sell their product, otherwise merchants will not sell products on the online platform. So, the focus is to get a profitable customer for the merchant. However, getting a profitable customer is often difficult. Acquiring new customers & making a profit out of their first sale i s almost difficult because of promotion costs incurred by the merchants. The key idea is to persuade that customer to buy again, and again. It is the second (or repeat) sale that a customer gives you that is profitable. This is because it shows that the customer is happy with your business and wants to continue trading with you. It is often said that it is five to ten times cheaper to keep a customer than to get a new one.

## Approach
In the problem, the buyer behaviour and merchant behaviour are focused based on their preferences in brands and categories. More than 250 features are generated which are their in FeatureEngineeringScript folder. The features are built one by one based on profiles. The data is generated from the pipline.py file. And then fed to different models.
The maximum AUC score is 0.69 on test set and 0.72 on train set using Light GBM.
