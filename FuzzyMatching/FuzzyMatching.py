#!/usr/bin/env python
# coding: utf-8

# In[1]:


import difflib
import re
import numpy as np
import pandas as pd
import ast
from fuzzywuzzy import fuzz 

import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


# Reads the food with 6,000 rows
with open("../Reference and Datasets/foodList.txt") as f:
    foodList = f.read().splitlines()
    
# Reads the large food data with 200,000 rows
food_nutrient_large = pd.read_csv('../NutrientData/Food Data/food_nutrients_dict.csv')

# Reads categorized food with 16,000 rows
food_categ = pd.read_csv('../NutrientData/food_categorized_nurtrients_w_name.csv')


# In[3]:


# Clean up foodList
temp = list(filter(lambda x: x not in ['baby', 'producer', 'red', '85% lean', 'baked', 'leg','greater than 3% juice', 'family style'
                                      ,'polish', 'greek', 'on the border', 'tlc', 'low calorie', 'milk producer', 'producer milk', 'green', 'grade'], foodList))
foodList = temp


# In[4]:


# Creates a series of food_names with comma, for regex extracting purposes
food_comma = food_categ['food_name'] + ','

# Extracts the food's generic names 
food_categ['generic'] = food_comma.str.extract(r'^([^,]*),')[0]


# In[5]:


# Get rid of commas, colons, and other special characters 
food_clean_name = food_categ['food_name'].str.replace(r'[^a-zA-Z0-9 ]', "").str.replace(r' +', ' ')


# In[6]:


# Compiles a list of foodnames with 200k data and with 16k data respectively
foodlist_large = food_nutrient_large['name'].tolist()
foodlist_categ = food_clean_name.tolist()
foodlist_generic = food_categ['generic'].tolist()


# In[7]:


foodlist_generic


# In[8]:


# RegEx generator to match with decimals surrounded by indices
regexp = re.compile(r'^[^a-z]+\d\.\d')
findFoodName = re.compile("([^\.]+) \d+\.")


# In[9]:


# sample receipts. Input 4 works the best.
inp_one = [ '1805 University AVe. 2.53', 'Berkeley CA 94703 2.53', 'Store # 186 (510) 204-9074 2.53', 'UPEN 8:0OAM 10 9:0OPM DAILY 2.53', '21 SEASONI NG SALUE 2,202 2.53', '0 SUNFL OWER 2.53', 'SEA SALI FINE CRYSTALS 26.502 2.53', 'SOURDOUGT BATARD 2.53', 'GRAPES GREEN SEEDI ESS 2LB 2.53', 'BIRTHDAY CARO 2.53', 'BBQ CUT SALMON 2.53', 'SLCD SAL AMI PPRED COLUMUS 2.53', 'ORCANTC CHICKL TENDERS 2.53', 'PECORTNO ROMAW 2.53', 'SPICE INO BIACK PEPPER 207 2.53', '8.0 2.53', '5.75 2.53', '1.99 2.53', '3.49 2.53', '5.49 2.53', '1.38 2.53', 'EGGS EXIRA LARGE CAGE FRE BRU 2.53', 'BACON ABr UNCURED DAY RUBBED 2.53', 'POTATO RUSSET EACH 2.53', '@ 0.69/A 2.53', '2EA 2.53', 'AVDCADO EACH HASS 2.53', '@1.59/EA 2.53', '0.98 2.53', 'A- LAR 1C EACIH A9/t) UNCA 2.53', '0.49/EA 2.53', 'IRSH KFRRYOOD UNSA I 2.53', '2LA 2.53', 'BUTTLR 2.53', 'BuftA EACII 2.53' ]
inp_two = [ 'LIUR TED 2.53','Regular Price 2.53','Card Savings 2.53','6.49 S 2.53','8.49 2.53','2.00- 2.53','SEAFOOD 2.53','SALMON ATLANTIC 2.53','SMOKED SALMON LOX 2.53','13.98 S 2.53','9.99 S 2.53','PRODUCE 2.53','1 2.53','QTY 2.53','CUCUMBERS 2.53','1.00 S 2.53','0.39 1b @ $1.99 /lb 2.53','WT 2.53','0.78 S 2.53','RED ROMA TOMATOES 2.53','3.99 S 2.53','SWT YOUNG COCONUT 2.53','BOK CHOY BABY 2.53','GINGER ROOT 2.53','0.51 lb @ $2.99 /1b 2.53','1.52 S 2.53','WT 2.53','0.10 lb @ $3.99 /lb 2.53','0.40 S 2.53','3.98 S 2.53','WT 2.53','2 QTY PORTABELLA 2.53','0.21 lb @ $2.99 /lb 2.53','WT 2.53','0.63 S 2.53','6.99 S 2.53','SHALLOTS 2.53','0 ORGNC GAPES RED 2.53','1.68 Ib @ $0.99 /1b 2.53','WT 2.53','1.66 S 2.53','ORG BANANAS 2.53','DELI 2.53','6.80 2.53','PORT SALUT WHEEL 2.53' ]
inp_three = [ 'GROCERY 2.53','99 S 2.53','HIME SUSHI NOR1 2.53','549 2.53','O50- 2.53','Regular Price 2.53','Card Savings 2.53','DYNASTY RICE 5 LB 2.53','KASHI CRL GOLEA 2.53','Regular Price 2.53','Card Savings 2.53','2 QTY DE CECCO 8 2.53','KIKKOMAN GRGNC SO 2.53','Regular Price 2.53','Card Savings 2.53','PANDA EXPRESS MNDR 2.53','Resular Price 2.53','Card Savinss 2.53','MARINONNECRN R 2.53','LUNDBERG RTCE HT 2.53','LUNDBERG RICE 2.53','GROCERY COUPON 2.53','Resular Price 2.53','Card Savinas 2.53','0TY MP PRENIUN 2.53','1195 2.53','395 S 2.53','4.99 2.53','1.00- 2.53','2.95 S 2.53','3.99 2.53','1.00- 2.53','350S 2.53','0.01 2.53','0.0t- 2.53','NP TONAT0 ASIL 2.53','200S 2.53','GROCERY 2.53' ]
inp_four = [ 'PRODUCE 2.53','MSHRM PORTABE! LO 2.53','S FARMS SPACH 2.53','Regular Price 2.53','Card Savings 2.53','2 QTY CANTALQUPE 2.53','Regular 2.53','Card Savings 2.53','3.99 c 2.53','1.99 2.53','0.32- 2.53','Price 2.53','5.98 2.53','0.98- 2.53','O. 66 lb @ $i.49 /lb 2.53','JUt 30 YLW ONIONS 2.53','GREEN SDLSS GRAPES 2.53','CABBAGE SAVOY 2.53','GINGER ROOT 2.53','0.98 2.53','7.71 2.53','5.63 2.53','WT 2.53','WT 2.53','WT 2.53','2.58 lb @ $2 99 /lb 2.53','2.83 lb @ $1..99 /lb 2.53','0.41 lb @ $3.99 /1b 2.53','1.00 lb @ $2.99 /1b 2.53','1.64 2.53','WT 2.53','TOMATOES ON VINE 2.53','RASPBERRIES RED 2.53','WT 2.53','2.99 2.53','6.9: 2.53','5.99 2.53','0 ORGNC SWEET CORN 2.53','1 QTY 2.53','0 ORGNC MSHRH LIHTE 2.53','0 ORGNC FRESH HERB 2.53','3.50 2.53','5.00 2.53','ADDITIONAL DISCOUNTS 2.53','5.0 2.53','BASKET $5 OFf 0un Brands 2.53' ]


# In[10]:


# Finds the best match of the food item on the receipt from the database. Outputs a list of dictionaries.

all_scores = []
def matchReceipt(inp):  
    food = []
    for line in inp:
        if regexp.search(line):
            if findFoodName.search(line):
                words = findFoodName.search(line).group(0)
                bestRatio = 0
                pos = 0
                name = ""
                for i, f in enumerate(foodlist_categ):
                    r = fuzz.token_set_ratio(words, f)
                    if r > bestRatio:
                        pos = i
                        name = f
                        bestRatio = r
                if bestRatio > 50:
                    d = food_categ.loc[pos, 'nutrients']
                    gen = food_categ.loc[pos, 'generic']
                    food.append([words, name, gen, ast.literal_eval(d)])  
    return food


# In[11]:


def advanceMatchReceipt(inp):
    final = []
    clean_orig_pair = {}
    for line in inp:
        if regexp.search(line):
            if findFoodName.search(line):
                orig = findFoodName.search(line).group(0)
                bestRatio = 0
                name = ""
                for i, f in enumerate(foodList):
                    r = fuzz.token_set_ratio(orig, f)
                    if r > bestRatio:
                        name = f
                        bestRatio = r
                if bestRatio > 65:
                    clean_orig_pair[name] = [orig, bestRatio]
    for clean in clean_orig_pair.keys():
        bestRatio = 0
        pos = 0
        name = ""
        for i, f in enumerate(foodlist_categ):
            r = fuzz.token_set_ratio(clean, f)*0.5 + fuzz.token_set_ratio(clean_orig_pair[clean][0], f)*0.5
            if r > bestRatio:
                pos = i
                name = f
                bestRatio = r
        if bestRatio > 60:
            d = food_categ.loc[pos, 'nutrients']
            nutri = ast.literal_eval(d)
            final.append([clean_orig_pair[clean][0], clean, name, nutri])
    return final 


# In[12]:


advanceMatchReceipt(inp_two)


# In[13]:


matchReceipt(inp_two)


# In[14]:


#         for w in words:
#             r = 0
#             pos = 0
#             name = ""
#             for i, f in enumerate(foodlist_categ):
#                 s = difflib.SequenceMatcher(lambda x: x == ".", w.lower(), f)
#                 if s.ratio() > r:
#                     r = s.ratio()
#                     pos = i
#                     name = f
#             if r > 0.7:
#                 d = food_categ.loc[pos, 'nutrients']
#                 food.append((name, ast.literal_eval(d)))   

