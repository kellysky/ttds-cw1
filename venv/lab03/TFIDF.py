import math
import sys
sys.path.append('../../venv/lab03')
import Search
import tokenisation
import json
import Proximity

def tf_idf_input(string_list,words_dic,text,id):
    dicTF_IDF={}
    dicTF={}
    dicDF={}
    tf_list=[]
    order_list=[]

    for j in range(0,len(string_list)):
        search_string=Search.term_tokenisation(string_list[j])
        search_string=search_string.split()
        #caculate the tf value
        for item in search_string:
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
        #caculate the final value
        for k in  range(0,text.length):
            doc_id = id[k].firstChild.data.strip()
            for item in search_string:
                    tf_list=dicTF[item]
                    text_line=text[k].firstChild.data.strip()
                    text_line=text_line.split()
                    if tf_list[k]>0:
                        num=(1+math.log10(tf_list[k]))*math.log10(text.length/dicDF[item])
                        temp=temp+num
            dicTF_IDF[doc_id]=temp
            temp=0
        res=sorted(dicTF_IDF.items(),key=lambda d:d[1],reverse=True)
        print(res)
        order_list.append(res)

    #write into txt
    with open("../tfidf.results.txt",'w',encoding='utf-8') as f:
        for i in range(0,len(order_list)):
            order_dic=order_list[i]
            j=1
            for item in order_dic:
                f.write(str(i+1)+" "+"0"+" ")
                f.write(item[0])
                f.write(" ")
                f.write(str(item[1]))
                f.write(" "+"0"+"\n")
                if j==1:
                    break
                else:
                    j=j+1


if __name__=="__main__":
    content=[]
    content=Search.readRankedFile("queries.lab3.txt","../../collections/")
    words, text, id = tokenisation.preprocessing('trec.sample.xml', 'DOCNO', 'TEXT', 'HEADLINE')
    #Proximity.proximity_index(words, text, id)
    with open('../index_file.json','r',encoding='utf-8') as f:
        words_dic=json.loads(f.read())
    tf_idf_input(content,words_dic,text,id)


