import seaborn as sns
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
#read tables
df_customers=pd.read_csv('olist_customers_dataset.csv')
df_payment=pd.read_csv('olist_order_payments_dataset.csv')
df_order=pd.read_csv('olist_orders_dataset.csv')
df_items=pd.read_csv('olist_order_items_dataset.csv')
df_product=pd.read_csv('olist_products_dataset.csv')

df_customers.head(5)
df_order.head(5)
df_payment.head(5)

df_customers.columns
df_order.columns
df_payment.columns

#merge transactions 

df_customer_order=pd.merge(df_customers,df_order,how='inner',on='customer_id')
df_customer_order.columns

df_all_payment=pd.merge(df_customer_order, df_payment, how='inner', on='order_id')
df_all_item=pd.merge(df_all_payment, df_items,how='inner', on='order_id')
df_all=pd.merge(df_all_item,df_product,how='inner', on='product_id')
df_all.columns


#Last Situation of Data Visualization 
df_all.head(5)

#Data History 
#dataset structural information
df_all.info()
#only shows variables
df_all.dtypes
# =============================================================================
# describing the dataset
# =============================================================================
df_all.shape#rows and columns number
df_all.columns

df_all.describe().T

#EXAMINATION OF MISSING VALUES
df_all.isnull().values.any()

df_all.isnull().sum()

sns.pairplot(df_all)
# plotting state wise customer distribution
plt.figure(figsize=(15,8))
sns.countplot(x='customer_state', data=df_all)
plt.title('State Wise Customer Distribution')
plt.xlabel('State')
plt.ylabel('No. of Customers')

mean_installment=pd.DataFrame(df_all.groupby('customer_state',as_index=False)[['customer_state','payment_installments']].mean())

plt.figure(figsize=(15,8))
sns.barplot(x='customer_state',y='payment_installments' ,data=mean_installment)
plt.title('Mean of Installments')
plt.xlabel('Customer State')

# plotting the distribution of product name length
df_all['product_description_lenght']
plt.figure(figsize=(15,8))
sns.histplot(x='product_description_lenght', data=df_all)
plt.title('Distribution of Product Description Length')
plt.xlabel('Product Description Length')

# pair plot
sns.set(style="ticks", color_codes=True)
g = sns.pairplot(df_all[['product_photos_qty','product_name_lenght','product_description_lenght']],palette=['#2e4884','grey'])

#order_purchase_timestamp
df_timestamp=df_all.copy()
df_timestamp['date']=pd.to_datetime(df_all['order_purchase_timestamp'])
res = df_timestamp.set_index('date').groupby(pd.Grouper(freq='M'))['payment_value'].sum().reset_index()

plt.figure(figsize=(15,8))
sns.barplot(x='date',y='payment_value' ,data=res)
plt.title('Total Payment')
plt.xlabel('Date')

#i choose columns that should drop

# =============================================================================
# 'customer_unique_id','customer_zip_code_prefix','order_approved_at','order_delivered_carrier_date',
# 'order_delivered_customer_date','order_estimated_delivery_date','seller_id','shipping_limit_date',
# 'freight_value','product_weight_g',
# 'product_length_cm', 'product_height_cm', 'product_width_cm'

# =============================================================================
df_all.drop(['customer_unique_id','customer_zip_code_prefix','order_approved_at','order_delivered_carrier_date',
'order_delivered_customer_date','order_estimated_delivery_date','seller_id','shipping_limit_date',
'freight_value','product_weight_g',
'product_length_cm', 'product_height_cm', 'product_width_cm','order_item_id', 'product_id'],axis=1,inplace=True)

df_all.columns
df_all.reset_index(inplace=True)
df_all.describe()

df_all['customer_state'].unique()
customer_state_id=pd.DataFrame({'State_id':range(1,28),'State_Code':df_all['customer_state'].unique()})
customer_state_id


#merge for state_id
df_all=df_all.merge(customer_state_id,how='left',left_on='customer_state',right_on='State_Code')
df_all[['customer_state','State_Code','State_id']].head(30)

#drop 
df_all.drop(['State_Code','customer_state'],axis=1,inplace=True)

df_all.columns
#Correlation matrix and Heatmap
df_corr=pd.DataFrame(df_all.corr().loc[['payment_value'],:])
np.array(df_corr)
sns.heatmap(df_all.corr(),annot=True)

df_all.to_csv (r'C:\Users\Yuşa Çalık\Desktop\Bilge Adam Eğitim\AzureML\export_dataframe.csv', index = False, header=True)



customer_state_id.to_csv (r'C:\Users\Yuşa Çalık\Desktop\Bilge Adam Eğitim\AzureML\Customer_State_dataframe.csv', index = False, header=True)

