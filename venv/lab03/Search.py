import sys
sys.path.append('../../venv/lab03')
import  BooleanSearch
import PhraseSearch
import tokenisation
import Proximity
import ProximitySearch
import TFIDF
import BooleanMatrix
import pandas as  pd
import numpy as np
import json
from nltk.stem import PorterStemmer
import re

#to tokenzisation for term
def term_tokenisation(terms):
    terms=terms.split()
    r_not_letter = '[^a-zA-Z0-9]+'
    ps = PorterStemmer()
    stop_words = []
    with open("../englishST.txt", 'r', encoding='utf-8') as e:
        line = e.readline()
        while line:
            line = line.strip()
            line = line.split()
            stop_words.extend(line)
            line = e.readline()
    line=''
    words=['AND','NOT','OR']
    line=''
    for i in range(0,len(terms)):
        if terms[i] not in words:
            terms[i]=re.sub(r_not_letter, ' ', terms[i])
            terms[i]=terms[i].lower()
            #print(terms[i])
            if terms[i] not in stop_words:
                terms[i]=ps.stem(terms[i])
                line=line+terms[i]+" "
        else:
            line=line+terms[i]+" "
    print(line)
    return line

#deal with the mixed search situation
def mixed_search(search_string,df,words_dic,id):
    string1=''
    string2=''
    temp=''
    operate=''
    num=0
    flag=1;
    line = search_string.split()
    words_list = ['AND', 'NOT', 'OR']
    for i in range(0,len(line)):
        if line[i] not in words_list:
            temp=temp+line[i]+" "
        elif line[i+1] in words_list:
            string1=temp
            if i>1:
                flag=1;
            operate=line[i]+" "+line[i+1]
            num=i+2
            break
        else:
            string1 = temp
            if i > 1:
                flag = 1;
            operate = line[i]
            num = i + 1
            break

    for i in  range(num,len(line)):
        string2=string2+line[i]+' '
    if flag==1:
        result1=ProximitySearch.proximity_input(term_tokenisation(string1),words_dic)
        #result2=BooleanSearch.boolean_input(term_tokenisation(string2),df,id)
        result2 = ProximitySearch.proximity_input(term_tokenisation(string2), words_dic)
    elif flag==0:
        result1 = ProximitySearch.proximity_input(term_tokenisation(string2), words_dic)
        #result2 = BooleanSearch.boolean_input(term_tokenisation(string1), df, id)
        result2 = ProximitySearch.proximity_input(term_tokenisation(string1), words_dic)

    if operate=='OR':
         list1= list(set(result1).union(set(result2)))
         list1.sort()
         return list1
    elif operate=='AND':
         print(string1+' '+string2)
         print(result1)
         print(result2)
         #list2=list(set(result1)&set(result2))
         list2=[i for i in result2 if i in result1]
         list2.sort()
         return list2
    elif operate=='AND NOT':
        print('AND NOT')
        print(string1+'  '+string2)
        print(result1)
        print(result2)
        #list2 = list(set(result1).difference(set(result2)))
        list2= [i for i in result1 if i not in result2]
        list2.sort()
        return list2




def readRankedFile(filename,filepath):
    list=[]
    with open(filepath+filename,"r",encoding='utf-8') as f:
        line=f.readline()
        while line:
            line=line.split()
            text=''
            for i in range(1,len(line)):
                text=text+line[i]+" "
            list.append(text)
            line=f.readline()
    return list

def decide_Search(search_string,words_dic,id,df):
    line=[]
    num=''
    words_list= ['AND', 'NOT', 'OR']
    words=''
    word1=''
    word2=''
    search=search_string.split()
    for item in search:
        line.append(item)
    print(line)
    print(search_string[0])
    if search_string[0]=='#':
        i=1
        while search_string[i] !='(':
            num=num+search_string[i]
            i=i+1
        i=i+1
        while search_string[i]!=',':
            word1=word1+search_string[i]
            i=i+1
        i=i+1
        while search_string[i]!=')':
            word2=word2+search_string[i]
            i=i+1
        words=word1+" "+word2
        print('phrase search')
        print(words)
        return PhraseSearch.phrase_input(term_tokenisation(words),words_dic,int(num))

    #line=search_string.split()
    pos=0
    for i in range(0,len(line)):
        if line[i] not in words_list:
                pos=pos+1
        else:
            if pos >=2:
                print(search_string)
                print('mixed search')
                return mixed_search(search_string,df,words_dic,id)
                print(search_string)
            else:
                pos=0

    for item in words_list:
        if item in line:
            return BooleanSearch.boolean_input(term_tokenisation(search_string),df,id)
    return ProximitySearch.proximity_input(term_tokenisation(search_string),words_dic)




if __name__=="__main__":
    words,text, id = tokenisation.preprocessing('trec.5000.xml', 'DOCNO', 'TEXT','HEADLINE')
    Proximity.proximity_index(words, text, id)
    df=BooleanMatrix.boolean_matrix(words, text,id)

    with open('../index_file.json','r',encoding='utf-8') as f:
        words_dic=json.loads(f.read())

    df=' '
    with open('../../CW1collection/queries.boolean.txt','r') as f:
        line=f.readline()
        while line:
            line=line.split()
            content=''
            for i in range(1,len(line)):
                content=content+line[i]+" "
            list=decide_Search(content,words_dic,id,df)
            with open('../results.boolean.txt','a') as g:
                for item in list:
                    g.write(line[0]+" "+'0'+' '+item+" "+"0"+" "+"1"+" "+"0")
                    g.write('\n')
            line=f.readline()
