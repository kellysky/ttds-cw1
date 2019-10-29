import re
from multiprocessing.dummy import Pool as ThreadPool

#do proxximity search
def proximity_input(search_string,words_dic):
    words=search_string.split()
    words_list=[]
    #find all the words of term in words
    for items in words:
        if items in words_dic:
                words_list.append(words_dic[items])
    #if term is a single word, return result
    if len(words_list)==1:
        result=[]
        for items in words_list[0].keys():
            result.append(items)
        return result
    elif len(words_list)==0:
        return "Can not search this term/words"
    #find the document which can contain both words
    key=[]
    index=[]
    for items in words_list:
        temp=items.keys()
        key.append(temp)
    index=key[0]
    for i in range(0,len(key)):
        index=list(set(key[i])&set(index))

    #caculate the distance between both words
    temp=[]
    doc_index={}
    word1={}
    word2={}
    result=[]
    for i in index:
        temp=[]
        word_pos1=words_list[0]
        words_pos2=words_list[1]
        temp=word_pos1[i].split()
        word1[i]=temp
        temp=words_pos2[i].split()
        word2[i]=temp
    for i in index:
        temp1=word1[i]
        temp2=word2[i]
        for items in temp2:
            if str(int(items)-1) in temp1:
                result.append(i)
    result=list(set(result))
    result.sort()
    #print(result)
    return result








