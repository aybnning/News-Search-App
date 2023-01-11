
# coding: utf-8

# In[33]:


import json


# In[46]:


result_list = []
with open('News_Category_Dataset_train.json','r',encoding='utf-8') as f:
    for line in f.readlines():
        #print(line )
        newline=json.loads(line)
        g={}
        #rename keys in dict
        #"headline" to "title", "authors" to“author”, "link" to “url”, "short_description" to "content"
        for d in newline:
            if d=="headline":
                g["title"]=newline[d]
            elif d == "authors":
                g["author"] = newline[d]
            elif d == "link":
                g["url"] = newline[d]
            elif d == "short_description":
                g["content"] =  newline[d]
            else:
                g[d]=newline[d]
            if d not in ["","id", "year", "month", "publication", "Phrasenostopword"]:
                g[d]=newline[d]
        del g["headline"]
        del g["authors"]
        del g["link"]
        del g["short_description"]
        # only keep news data after 2017-00-00
        if g["date"] > '2017-00-00':
            result_list.append(g)
    print(result_list[0:5])


# In[47]:


with open('categorized_news_part1.json', 'w') as f:
    json.dump(result_list, f)

