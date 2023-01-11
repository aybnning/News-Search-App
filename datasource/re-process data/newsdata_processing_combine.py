
# coding: utf-8

# In[14]:


import json


# In[15]:


#the following code combines 'categorized_news_part1.json' and 'categorized_news_part2.json'
with open('categorized_news_part1.json', 'r') as df1:
    data1 = json.load(df1)
with open('categorized_news_part2.json', 'r') as df2:
    data2 = json.load(df2)
data = data1 + data2
print(data[0])


# In[16]:


with open('categorized_news.json', 'w') as df:
    json.dump(data, df)


# In[17]:


print(len(data))

