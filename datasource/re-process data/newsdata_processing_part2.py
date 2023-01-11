
# coding: utf-8

# In[16]:


import json


# In[17]:


#function used to get first sentence of a paragraph (stop at first '.')
def get_first_sentence(content):
    contentList = content.split('.' + ' ')
    return contentList[0]
#get_first_sentence(' Turkey and Russia signed an agreement on Monday for the construction of a major undersea gas pipeline and vowed to seek common ground on the war in Syria, accelerating a normalization in ties nearly a year after Turkey shot down a Russian warplane. Turkish President Tayyip Erdogan hosted Russia’s Vladimir Putin at an   villa in Istanbul for talks which touched on energy deals, trade and tourism ties, defense and the conflict in Syria, where the two leaders back opposing sides. ”Today has been a full day with President Putin of discussing   relations . .. I have full confidence that the normalization of   ties will continue at a fast pace,” Erdogan told a joint news conference. The warming relations between NATO member Turkey and Russia comes as both countries are dealing with troubled economies and strained ties with the West.  Putin said Moscow had decided to lift a ban on some food products from Turkey, imposed after the Turks shot down a Russian fighter jet near the Syrian border last November, and that both leaders had agreed to work toward the   normalization of bilateral ties. They signed a deal on the TurkStream undersea gas pipeline, which will allow Moscow to strengthen its position in the European gas market and cut energy supplies via Ukraine, the main route for Russian energy into Europe.  The plan for TurkStream emerged after Russia dropped plans to build the South Stream pipeline to Bulgaria due to opposition from the European Union, which is trying to reduce its dependence on Russian gas. Erdogan also said plans for a   nuclear power plant in Turkey would be accelerated. Time lost on the Akkuyu project because of strained relations would be made up, he said. In 2013, Russia’s state nuclear corporation Rosatom won a $20 billion contract to build four reactors in what was to become Turkey’s first nuclear plant, but construction was halted after the downing of the Russian jet. DEEP DIVISIONS ON SYRIA Putin received Erdogan in a   palace outside his home city of St Petersburg in August, when the two leaders, both powerful figures   to dissent, announced plans for an acceleration in trade and energy ties.')


# In[18]:


# the following code processed 'categorized_news_data.json' in categorize news_bayes file
#the outputted file will later be combined with 'categorized_news_part1.json'
result_list = []
with open('categorized_news_data_line.json','r',encoding='utf-8') as f:
    for line in f.readlines():
        newline=json.loads(line)
        g={}
        #rename keys in dict
        for d in newline:
            g[d]=newline[d]
            if d not in ["","id", "year", "month", "publication", "Phrasenostopword"]:
                g[d]=newline[d]
        #delete unneeded keys
        del g[""]
        del g["id"]
        del g["year"]
        del g["month"]
        del g["publication"]
        del g["Phrasenostopword"]
        # only keep news data after 2017-00-00
        result_list.append(g)
    #print(result_list[0])
    #print(type(result_list)
    #summarize 'content', no longer display the whole news article
    for dictElement in result_list:
        dictElement['content'] = get_first_sentence(dictElement['content'])
    print(result_list[20000])
    


# In[19]:


with open('categorized_news_part2.json', 'w') as f:
    json.dump(result_list, f)


# In[20]:


print(len(result_list))

