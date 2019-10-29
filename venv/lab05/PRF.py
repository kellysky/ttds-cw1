import sys
sys.path.append('../../venv/lab03')
import tokenisation
import string,re
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import xml.dom.minidom as xmldom
import json
import Search
import math


def prf(text,id,term_id):
    doc=[]
    with open('../tfidf.results.txt','r') as f:
        line=f.readline()
        while line:
            line=line.split()
            if line[0]==term_id:
                doc.append(line[2])
            line=f.readline()
    print(doc)
    doc_content=''
    for i in range(0,len(doc)):
        for j in range(0,id.length):
            if doc[i] in id[j].firstChild.data:
                doc_content=doc_content+" "+text[j].firstChild.data

    doc_content=doc_content.split()
    words_list=list(set(doc_content))

    with open('../index_file.json','r',encoding='utf-8') as f:
        words_dic=json.loads(f.read())
    dicTF_IDF={}
    dicTF={}
    dicDF={}
    tf_list=[]
    order_list=[]
    tf={}
    # #caculate the tf value
    # for item in words_list:
    #     num=0
    #     for i in doc_content:
    #         if i==item:
    #             num=num+1
    #             tf[item]=num


     #caculate the tf value
    for item in words_list:
        doc_word=words_dic[item]
        dicDF[item]=len(doc_word)
        tf_list=[]
        for i in  range(0,text.length):
            doc_id=id[i].firstChild.data.strip()
            if doc_id in doc_word.keys():
                line=doc_word[doc_id].split()
                tf_list.append(len(line))
            else:
                tf_list.append(0)
        dicTF[item]=tf_list
    temp=0
    tf['tax']=18
    print(tf['tax'])
    print(dicDF['tax'])
    #caculate the final value
    for item in words_list:
        for k in range(0,text.length):
               doc_id = id[k].firstChild.data.strip()
               tf_list=dicTF[item]
               text_line=text[k].firstChild.data.strip()
               text_line=text_line.split()
               if tf_list[k]>0:
                   num=(1+math.log10(tf_list[k]))*math.log10(text.length/dicDF[item])
                   temp=temp+num
        #dicTF_IDF[item]=(1 + math.log10(tf[item])) * math.log10(text.length / dicDF[item])
        if item=='tax':
            print(dicTF['tax'])
            print(dicDF[item])
            dicTF_IDF[item]=temp
            print(dicTF_IDF[item])
        dicTF_IDF[item]=temp
        temp=0
    res=sorted(dicTF_IDF.items(),key=lambda d:d[1],reverse=True)
    print(res)
    order_list.append(res)




if __name__=="__main__":
    words, text, id = tokenisation.preprocessing('trec.sample.xml', 'DOCNO', 'TEXT', 'HEADLINE')
    prf(text,id,'1')
