import  re

#to phrase search
def phrase_input(search_string,words_dic,gap):
    words = search_string.split()
    words_list = []
    for items in words:
        if items in words_dic:
            words_list.append(words_dic[items])
    #when phrase words is just a single word
    if len(words_list) == 1:
        return words_list
    elif len(words_list) == 0:
        return "Can not search this term/words"
    key = []
    index = []
    for items in words_list:
        temp = items.keys()
        key.append(temp)
    index = key[0]
    for i in range(0, len(key)):
        index = list(set(key[i]) & set(index))
    #find the document which contains both words
    temp = []
    result=[]
    doc_index = {}
    for i in index:
        temp = []
        for items in words_list:
            line = items[i]
            temp.append(line)
            doc_index[i] = temp
    #caculate the distance between both words
    result = []
    for i in index:
        line=doc_index[i];
        line1=line[0].split()
        line2=line[1].split()
        for items in  line1:
            for k in line2:
                if (abs(int(k)-int(items))<=gap):
                        result.append(i)
    result = list(set(result))
    result.sort()
    return result