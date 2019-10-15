
# coding: utf-8

# In[1]:


import difflib


# In[2]:


foodList = open("/Users/wenlonghuang/GoogleDrive/funnel/foodList.txt")
foodList = foodList.readlines()
for i in range(len(foodList)):
    foodList[i] = foodList[i][:-1]


# In[3]:


def examineDecimal(line, dot_idx):
    if dot_idx != len(line) - 1:
        try:
            int(line[dot_idx + 1])
            return True
        except:
            return False
    return False



def containsDecimal(line):
    results = []
    try:
        dot_indices = [i for i, x in enumerate(line) if x == "."]
        # print(dot_indices)
        for idx in dot_indices:
            results.append(examineDecimal(line, idx))
        # print(results)
        return any(results)
    except:
        return False


# In[4]:


results = []
inp = ['Subtotal : $1.95', 'Cooker. $1.95', 'APpLEea 2.1', 'so pee edi ce sald aan hee paxew Uebel er nla', 'Date: 11/14/18, 9:06 PM',
       'Order# 3913644', 'Se (510) 843-5252', 'wn berkeley, CA 94704', 's; 2300 College Ave.']
for line in inp:
    if containsDecimal(line):
        words = line.split(' ')
        for w in words:
            close_matches = difflib.get_close_matches(w.lower(), foodList, n=1, cutoff=0.7)
            if close_matches:
                results.append(close_matches[0])


# In[5]:


results

