import re
from nltk.stem import PorterStemmer
import xml.etree.ElementTree as ET
from collections import Counter
import math
import collections
import os
import Search

rankFile = '../tfidf.results.txt'
xmlFile = '../../collections/trec.sample.xml'
stopwordsFile = '../englishST.txt'

dict_doc_content = {}
#invertFullIndex=Search.readFullIndex()
n =1000
def removStopWord(low_data_word):
    with open(stopwordsFile, 'r', encoding='UTF-8') as fstop:
        stopWord = fstop.read()
        stopWordList = stopWord.split("\n")
        stopDic = {}
        word_stop = []
        for word in stopWordList:
            stopDic[word] = 1
        for word in low_data_word:
            if word in stopDic:
                continue
            else:
                word_stop.append(word)
        return word_stop

def get_doc_id(n_d, start_id, end_id):
    doc_list = []
    with open(rankFile, 'r', encoding='UTF-8') as rf:
        data = rf.readlines()
        for id in range(start_id, end_id+1):
            count = n_d
            for line in data:
                if(count==0):
                    break
                line_list = line.split()
                if line_list[0] == str(id):
                    doc_list.append(line_list[2])
                    count -= 1
    for i in doc_list:
        dict_doc_content[i] = []
    return doc_list

def get_doc_content(doc_list):
    doc_content = []
    stemmer = PorterStemmer()
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    flag = 0
    for child in root.iter('DOC'):
        for item in child.getiterator():
            if item.tag == 'DOCNO':
                id = item.text
                if id in doc_list:
                    flag = 2
            if flag > 0:
                if item.tag == 'HEADLINE' or item.tag == 'TEXT':
                    flag -= 1
                    line_cutpun = re.sub(r'[^\w\s]', ' ', item.text)
                    low_line_cutpun = [x.lower() for x in line_cutpun.split()]
                    stop_line = removStopWord(low_line_cutpun)
                    for word in stop_line:
                        final_word = stemmer.stem(word)
                        dict_doc_content[id].append(final_word)
                        doc_content.append(final_word)

    return doc_content

def get_tf(term, doc_content):
    count = 0
    print(term)
    print(doc_content)
    for terms in doc_content:
        if term==terms:
            count+=1
    if term == 'tax':
        print(count)
    return count

def cal_tfidf(term, doc_list):
    score = 0
    for id in doc_list:
        tf = get_tf(term, dict_doc_content[id])
        print(tf)
        print('tf')
        if tf== 0:
            continue
        df = Search.getDF(invertFullIndex, term)
        if term == 'tax':
            print(df)
        score += (1+math.log(tf, 10)) * math.log(n/df, 10)
    return score



if __name__ == '__main__':
    dict_score = {}
    ids = get_doc_id(1,1,1)
    print(ids)
    term_list = get_doc_content(ids)
    print(term_list)
    print((1 + math.log(18, 10)) * math.log(n / 187, 10))
    for term in term_list:
        dict_score[term] = 0
    for term in term_list:
        dict_score[term]+=cal_tfidf(term,ids)
    items = dict_score.items()
    p = sorted(items,key=lambda d: d[1], reverse = False)
    print(p)
    # for i in range(0,6):
    #     print(dict_score.keys()[i])
