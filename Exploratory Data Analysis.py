#!/usr/bin/env python
# coding: utf-8

# Import Libraries 

# In[33]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set(color_codes=True)

import plotly.graph_objects as go
from datetime import datetime
import warnings 
warnings.filterwarnings('ignore')


# Collecting Data

# In[34]:


data= pd.read_csv("F:/Kaggle Data/Udemy Finance/udemy_output_All_Finance__Accounting_p1_p626.csv")
data


# Data Cleaning

# In[35]:


data.describe()


# In[36]:


data.drop(['id', 'url', 'num_published_practice_tests', 'discount_price__price_string',
          'price_detail__price_string', 'discount_price__currency', 'price_detail__currency'], axis=1, inplace=True)
data


# In[37]:


#rename

data = data.rename(columns={
    'is_paid':"paid", 'num_subscribers':"subscribers", 'is_wishlisted':"wishlisted",
    'num_published_lectures':"lectures", 'published_time':"publish", 'discount_price__amount':"d_amount",
    'price_detail__amount':"p_amount"
})
data.head()


# In[38]:



# data.isnull().sum().sort_values(ascending=False)
# data=data.dropna()


# In[39]:


data[data['d_amount'].isna()].head(5)


# In[40]:


data[data['p_amount'].isna()].head(5)


# Data Visualization 

# In[41]:


def get_three(col):
    print("Mean: ", np.mean(data[~data[col].isna()][col].to_list()))
    print("Median: ", np.median(data[~data[col].isna()][col].to_list()))
    print("Mod: ", stats.mode(data[~data[col].isna()][col].to_list())[0][0])
    
    plt.figure(figsize=(15,7))
    ax= sns.countplot(x=col, data=data)
    plt.xticks(rotation=90)
    plt.show()


# In[42]:


get_three("d_amount")
get_three("p_amount")


# In[43]:


plt.style.use('fivethirtyeight')
sns.distplot(data[~data['p_amount'].isna()]['p_amount'].to_list(), color='blue')
plt.show()


# In[44]:


# d_amount_nan_index = data[data['d_amount'].isna().index.to_list()]
# p_amount_nan_index= data[data['p_amount'].isna().index.to+list()]

# data.loc[d_amount_nan_index]=455.0
# data.loc[p_amount_nan_index] = 3200.0


# In[45]:


print("d_amount nan count :", data["d_amount"].isnull().sum())
print("p_amount nan count :", data["p_amount"].isnull().sum())


# In[46]:


plt.figure(figsize=(15,5))
sns.boxplot(x=data["subscribers"])


# In[47]:


for col in data.select_dtypes('float64').columns:
    plt.figure(figsize=(15,5))
    plt.title(col)
    sns.boxplot(x=data[col])


# In[48]:


for col in data.select_dtypes('int64').columns:
    plt.figure(figsize=(15,5))
    plt.title(col)
    sns.boxplot(x=data[col])


# In[49]:


print("for avg_rating: ", len(data[data['avg_rating'] > 5]))
print("for avg_rating_recent: ", len(data[data["avg_rating_recent"] > 5]))


# In[50]:


data['paid'].value_counts()


# In[51]:


data.drop(['paid'], axis=1, inplace=True)
data.drop(['wishlisted'], axis=1, inplace=True)


# In[52]:


data


# In[53]:


print('Max_num_reviews:', np.max(data['num_reviews'].to_list()))
print('Min_num_reviews:', np.min(data['num_reviews'].to_list()))
print('Mean_num_review:', np.mean(data['num_reviews'].to_list()))


# The creation and release dates of the courses are important to find out how long these courses were prepared by the course provider. But there is too much detail. The year, month and day will be sufficient. That's why we have to date conversion.
# 
# 

# In[54]:


data['created'] = pd.to_datetime(data['created'].to_list()).strftime('%m-%d-%Y').values
data['publish'] = pd.to_datetime(data['publish'].to_list()).strftime('%m-%d-%Y').values


# In[55]:


data


# Same creating columns od p_amoubnt, d_amount

# In[56]:


# for d_amount
print('Max d_amount:', np.max(data['d_amount'].to_list()))
print('Min d_amount:', np.min(data['d_amount'].to_list()))
print('Mean d_amount:', np.mean(data['d_amount'].to_list()))


# In[57]:


# for p_amount
print('Max p_amount:', np.max(data['p_amount'].to_list()))
print('Min p_amount:', np.min(data['p_amount'].to_list()))
print('Mean p_amount:', np.mean(data['p_amount'].to_list()))


# In[58]:


# 1 Indian Rupee = 0.014 Dolar
data['p_amount'] = round(data['p_amount']*0.014,2).to_list()
data['d_amount'] = round(data['d_amount']*0.014,2).to_list()


# In[59]:


data


# Top 10 Course find out

# In[60]:


data[['title', 'subscribers', 'avg_rating']]     .sort_values(by="subscribers", ascending=False)[0:10].set_index('title')     .style.format('{:.2f}', subset=['avg_rating']).background_gradient(cmap='Blues', subset=['avg_rating'])     .set_caption("Most Subscriber Courses")     .set_properties(padding='15px', border='2px solid white', width='170px')
    


# .

# In[61]:


data['rating_diff'] = data.avg_rating_recent = data.avg_rating


# In[62]:


data[data.subscribers > 10000][['title', 'subscribers', 'avg_rating', 'avg_rating_recent', 'rating_diff']]     .sort_values(by = 'rating_diff')[:10].set_index('title')     .style.format('{:.4f}', subset=['avg_rating', 'avg_rating_recent', 'rating_diff']).background_gradient(cmap='Blues', subset=['subscribers'])     .bar(align = 'mid', color=['#FCC0CB', '#90EE90'], subset=['rating_diff'])     .set_caption("Rating Changes")     .set_properties(padding='15px', border='2px solid white', width='170px')
    


# 1. Top 10 Subscriberd Courses

# In[63]:


df = data.sort_values(by="subscribers", ascending=False)
trace = go.Bar( x=df.subscribers[0:10],
              y = df.title[0:10],
              marker= dict(color=['gold','red', 'chocolate', 'coral', 'cornflowerblue',
            'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan']),orientation='h')

layout = dict(height=500,
              yaxis=dict(autorange="reversed"),
             title="Top 10 Subscriberd Courses",
                template = "plotly_dark")

fig = go.Figure(data=[trace], layout=layout)
fig.show()


# 2. Top 10 Most lectures Course

# In[64]:



df = data.sort_values(by="lectures", ascending=False)

trace = go.Bar( x=df.lectures[0:10],
              y = df.title[0:10],
              marker= dict(color=['gold','red', 'chocolate', 'coral', 'cornflowerblue',
            'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan']),orientation='h')

layout = dict(height=500,
              yaxis=dict(autorange="reversed"),
             title="Top 10 Most Lectures Courses",
                template = "plotly_dark")

fig = go.Figure(data=[trace], layout=layout)
fig.show()


# In[ ]:





# In[ ]:




