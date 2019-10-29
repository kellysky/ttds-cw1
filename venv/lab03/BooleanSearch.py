import sys
sys.path.append('../../venv/lab03')
import tokenisation
import BooleanMatrix
import Proximity
import pandas as pd
import numpy as np
import ProximitySearch
import json


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items)==0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        if not self.isEmpty():
            return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

#read the term and caculate the matrix
def boolean_input(search_string,df,id):
    print(search_string)
    with open('../index_file.json', 'r', encoding='utf-8') as f:
         words_dic=json.loads(f.read())

    temp=[]
    result=[]
    s=Stack()
    line=search_string.strip().split()
    i=len(line)-1
    while i!=-1:
        s.push(line[i])
        i=i-1
    words=s.pop()
    last_words=''
    s.push(words)
    #print(df[words])
    #df['temp_result']=df[words]
    result=words_dic[words].keys()
    #pop the element in stack and caculate the matrix , store the result in a new column named temp_result
    while s.isEmpty()==False:
        last_words=words
        words=s.pop()
        #print(words)
        if (words=='AND'):
            temp=s.pop()
            if (temp!='NOT'):
                result=list(set(result).intersection(words_dic[temp].keys()))
                temp_result=[]
            elif (temp =='NOT'):
                temp=s.pop()
                result=list(set(result).difference(set(words_dic[temp].keys())))
        elif (words=='NOT'):
            temp=s.pop()
            result = list(set(result).difference(set(words_dic[temp].keys())))
        elif (words=='OR'):
            temp=s.pop()
            result = list(set(result).intersection(set(words_dic[temp].keys())))

    result.sort()
    return result



