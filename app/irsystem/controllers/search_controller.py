import nltk
from werkzeug import ClosingIterator
from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os
import re
from collections import Counter
import math
import string

# add import
import json
from nltk.tokenize import TreebankWordTokenizer
import string
from collections import defaultdict
from collections import Counter
import numpy as np
import pickle
from app.irsystem.controllers.redditRequest import getRedditData, top_five, getRedditResult
from app.irsystem.controllers.new_search_method import build_inverted_index, compute_idf, compute_doc_norms, index_search

project_name = "Go!News"
net_id = "Simon Huang (mh954), Beining Yang(by258), Zhiqian Ma(zm79), Xirui He(xh358)"

dir_path = os.path.dirname(os.path.realpath(__file__))
jsonPath = dir_path+'/../../../datasource/categorized_news.json'

with open(jsonPath, "r") as f:
    newsList = json.load(f)

dir_path = os.path.dirname(os.path.realpath(__file__))
picklePath = dir_path+'/../../../datasource/subredditList.pkl'
with open(picklePath, 'rb') as f:
    subredditList = pickle.load(f)


def getClosestSubreddit(query, subredditList=subredditList):
    minimum_dist = 10000
    minimum_name = ""
    for i in range(len(subredditList)):
        name = subredditList[i]
        dist = levenshteinDistanceDP(name, query)
        if dist == 0:
            return name
        if dist < minimum_dist:
            minimum_dist = dist
            minimum_name = name
    return minimum_name


def levenshteinDistanceDP(token1, token2):
    """
    acknowledgement: https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/

    Return: Edit distance of two tokens
    """
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1
    return distances[len(token1)][len(token2)]


treebank_tokenizer = TreebankWordTokenizer()
for news in newsList:
    news['tokens'] = treebank_tokenizer.tokenize(news['title'].lower())
inv_idx = build_inverted_index(newsList)
idf = compute_idf(inv_idx, len(newsList),
                  min_df=15,
                  max_df_ratio=0.9)
inv_idx = {key: val for key, val in inv_idx.items()
           if key in idf}
doc_norms = compute_doc_norms(inv_idx, idf, len(newsList))


def getComments(keyword):
    """
    get the comments from most popular posts about the topic
    """
    data = getRedditResult(keyword=keyword)
    return data


def remove_symbols(strInput):
    if strInput != None:
        del_estr = string.punctuation + string.digits  # ASCII
        replace = " "*len(del_estr)
        tran_tab = str.maketrans(del_estr, replace)
        strOutput = strInput.translate(tran_tab)
    else:
        strOutput = strInput
    return strOutput
#print(remove_symbols('WORLD_NEWS'))
#print(remove_symbols(None))

def getNone(strInput):
    return None

@irsystem.route('/', methods=['GET'])
def search():
    #get frontend checkbox result
    query = request.args.get('search')
    POLITICS = request.args.get('POLITICS')
    ENTERTAINMENT = request.args.get('ENTERTAINMENT')
    WORLD_NEWS = request.args.get('WORLD_NEWS')
    COMEDY = request.args.get('COMEDY')
    HEALTHY_LIVING = request.args.get('HEALTHY_LIVING')
    WELLNESS = request.args.get('WELLNESS')
    SPORTS = request.args.get('SPORTS')
    MEDIA = request.args.get('MEDIA')

    
    categoryList = [POLITICS, ENTERTAINMENT, remove_symbols(WORLD_NEWS), COMEDY, remove_symbols(HEALTHY_LIVING), WELLNESS, SPORTS, MEDIA]
    #print(categoryList)

    if not query:
        reddit = []
        data = []
        context = dict()
        output_message = ''
    else:
        srName = getClosestSubreddit(query, subredditList)
        output_message = query
        redditResult = getComments(srName)

        newsRank = index_search(query, inv_idx, idf, doc_norms)
        newsResult = []

        for score, doc_id in newsRank:
            if categoryList == [None, None, None, None, None, None, None, None]:
                newsResult.append(
                    (newsList[doc_id]['title'], newsList[doc_id]['url'], round(score, 2)))
            if newsList[doc_id]['category'] in categoryList:
                newsResult.append(
                    (newsList[doc_id]['title'], newsList[doc_id]['url'], round(score, 2)))
            if len(newsResult) == 10:
                break

        context = {
            'reddit': redditResult,
            'news': newsResult
        }

    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, context=context, categoryList=categoryList)
