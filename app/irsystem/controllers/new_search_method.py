from collections import defaultdict
from collections import Counter
import json
import math
import string
import time
import numpy as np
import os
from nltk.tokenize import TreebankWordTokenizer


treebank_tokenizer = TreebankWordTokenizer()


def build_inverted_index(newsList):
    n = len(newsList)
    result = dict()
    for i in range(n):
        wc = dict()
        for word in newsList[i]['tokens']:
            wc[word] = wc.setdefault(word, 0)+1
        for word, count in wc.items():
            result.setdefault(word, []).append((i, count))
    return result


def boolean_search(query_word, excluded_word, inverted_index):
    query_word = query_word.lower()
    excluded_word = excluded_word.lower()
    M = []
    A, B = [], []
    for doc_id, count in inverted_index[query_word]:
        if count > 0:
            A.append(doc_id)
    for doc_id, count in inverted_index[excluded_word]:
        if count > 0:
            B.append(doc_id)
    i, j = 0, 0
    while i < len(A) and j < len(B):
        if A[i] == B[j]:
            i += 1
            j += 1
        else:
            if A[i] < B[j]:
                M.append(A[i])
                i += 1
            else:
                j += 1
    if i <= len(A) - 1:
        for k in range(i, len(A)):
            M.append(A[i])
    return M


def compute_idf(inv_idx, n_docs, min_df=15, max_df_ratio=0.90):
    idf = dict()
    for word, tuples in inv_idx.items():
        df_word = len(tuples)
        df_ratio = df_word / n_docs
        if min_df > df_word or max_df_ratio < df_ratio:
            continue
        idf[word] = np.log2(n_docs / (1 + df_word))
    return idf


def compute_doc_norms(index, idf, n_docs):
    norms = np.zeros(n_docs)
    for word, idf_score in idf.items():
        for doc_id, count in index[word]:
            norms[doc_id] += (count * idf_score) ** 2
    return np.sqrt(norms)


def index_search(query, index, idf, doc_norms, tokenizer=treebank_tokenizer):
    tok_q = tokenizer.tokenize(query.lower())

    query_tf = dict()
    for word in tok_q:
        query_tf[word] = query_tf.setdefault(word, 0) + 1

    index_dict = dict()
    for word in index:
        index_dict[word] = dict()
        for doc_id, count in index[word]:
            index_dict[word][doc_id] = count

    result = []
    for doc_id in range(len(doc_norms)):
        qnorm = 0
        dotprod = 0
        for word in query_tf.keys():
            if word not in idf:
                continue
            query_tfidf = query_tf[word] * idf[word]
            doc_tfidf = index_dict[word].get(doc_id, 0) * idf[word]
            qnorm += query_tfidf ** 2
            dotprod += query_tfidf * doc_tfidf
        qnorm = np.sqrt(qnorm)
        denom = doc_norms[doc_id] * qnorm
        score = (dotprod / denom) if denom != 0 else 0
        result.append((score, doc_id))

    result = sorted(result, key=lambda x: x[0], reverse=True)
    return result
