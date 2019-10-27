#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


# Reads food form
food = pd.read_csv("food.csv")

# Reads food_nutrient id pairing form
food_nutri = pd.read_csv("food_nutrient.csv")
food_nutri = food_nutri.drop(columns = ['min', 'max', 'median', 'footnote', 'min_year_acquired'])

# Reads food nutrients conversion
food_nutri_conv = pd.read_csv("food_nutrient_conversion_factor.csv")

# A USELESS FORM
food_nutri_src = pd.read_csv("food_nutrient_source.csv") 

# Nutrient form
nutri = pd.read_csv("Food Data/nutrient.csv")


# In[61]:


# Categories 
categ = pd.read_csv("food_category.csv")


# In[3]:


display(food_nutri.shape, food.shape)
len(food_nutri['fdc_id'].unique())
food_nutri.head()


# In[4]:


# Creates new column lower_name of lower letters
food['brand_name'] = food['description'].str.extract(pat = '([A-Z]{2,})*') 
food['lower_name'] = food['description'].str.extract(pat = '([^\d]+)') 
food['lower_name'] = food['lower_name'].str.strip().str.replace(r',$', '').str.lower()


# In[5]:


# TODO creates foodname
food['description_comma'] = food['description'] + ','
food['food_name'] = food['description_comma'].str.extract(pat = '[A-Z]{2,}\w(.*), \d')


# In[6]:


# Create food nutrient pairs with nutrient names 
food_nutri_pair = food_nutri[['fdc_id', 'nutrient_id', 'amount']]
food_nutri_pair = food_nutri_pair[food_nutri_pair['amount'] > 0.0]
food_nutri_pair['amount'] = np.round(food_nutri_pair['amount'], 2)
food_nutri_name = food_nutri_pair.merge(nutri[['id', 'name']], left_on = 'nutrient_id', right_on = 'id', how = 'left').drop(columns = ['id'])


# In[7]:


# food_nutri_name['list_name_amount']
food_nutri_name['name_amount'] = food_nutri_name[['name', 'amount']].values.tolist()
food_nutri_name['name_amount'].head()


# In[8]:


# Creates a dictionary of nutrients for each food item
food_nutri_dict = food_nutri_name.groupby('fdc_id')['name_amount'].agg(lambda s: dict(zip(s.map(lambda x: x[0]).tolist()
                                                                             , s.map(lambda y: y[1]).tolist())))

food_nutri_dict_df = pd.DataFrame({'nutrients': food_nutri_dict})
food_nutri_dict_df.head()


# In[9]:


display(food_nutri_dict.shape, food.shape)


# In[10]:


# Add the nutrients back to the food table
# Run this for only ONE TIME
food = food.merge(food_nutri_dict_df, left_on = 'fdc_id', right_on = 'fdc_id', how = 'left')


# In[11]:



food_json = food[['lower_name', 'nutrients']].set_index(food['fdc_id'])
# Export = food_json.to_json (r'/Users/daniel/Documents/College/FunnelFoods/food_nutrients.json', orient='index')


# In[12]:


# list of unique nutrients: nutri df
food_nutrient_info = food_json.rename(columns = {'lower_name': 'name'})
# Export = food_nutrient_info.to_csv(r'/Users/daniel/Documents/College/FunnelFoods/food_nutrients_dict.csv')


# In[13]:


food_nutri_id_pair = food_nutri[['fdc_id', 'nutrient_id']][food_nutri['amount'] > 0]
food_nutri_id_pair = food_nutri_id_pair.reset_index(drop = True)
# Export = food_nutri_id_pair.to_csv(r'/Users/daniel/Documents/College/FunnelFoods/food_nutrient_id_pair.csv')


# In[71]:


temp = food[~np.isnan(food['food_category_id'])]
food_categorizied_nutrients = temp[~temp['nutrients'].isnull()]
food_categorizied_nutrients.head()


# In[42]:


food_nutri_amount = food_nutri[['fdc_id', 'nutrient_id', 'amount']][food_nutri['amount'] > 0]
# Export = food_nutri_amount.to_csv(r'food_nutrient_amount.csv')


# In[58]:


len(food_categorizied_nutrients)


# In[68]:


food_categorized_nurtrients_w_name = food_categorizied_nutrients.merge(categ, left_on = 'food_category_id', right_on = 'id', how= 'left')[
    ['fdc_id', 'lower_name', 'nutrients','food_category_id', 'description_y', ]
        ].rename(columns = {
    'lower_name':'food_name', 
    'description_y':'category_name',
})


# In[69]:


food_categorized_nurtrients_w_name.head()


# In[70]:


# Export = food_categorized_nurtrients_w_name.to_csv(r'food_categorized_nurtrients_w_name.csv')


# In[ ]:




