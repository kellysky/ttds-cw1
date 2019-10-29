import xml.dom.minidom as xmldom
import re
import json

#generate the inverted list
def proximity_index(words,text,id):
    r_words="[( ) ' ']+"
    words_dic={}
    for x in words:
         words_dic[x]={}

    #iterate the documents and find the position for every character
    for j in range(0,text.length):
            line=text[j].firstChild.data.strip()
            line=line.split()
            doc_id=id[j].firstChild.data.strip()
            x=1
            for i in range(0,len(line)):
                if line[i] in words:
                    index={}
                    index=words_dic[line[i]]
                    if doc_id in index:
                        content=''
                        content=index[doc_id]
                        content=content+'  '+str(i+1)
                        index[doc_id]=content
                    else:
                        index[doc_id]=str(i+1)
                    words_dic[line[i]]=index

    #write into txt
    with open('../index_file.txt','w',encoding='utf-8') as f:
        for i in range(0,len(words_dic)):
            f.write(words[i]+':')
            f.write('\n')
            index=words_dic[words[i]]
            content=''
            for item in index.items():
                content=str(item)
                content=re.sub(r_words,' ',content)
                content=re.sub("[,]",':',content)
                f.write('        ')
                f.write(content)
                f.write('\n')

    #write into json
    with open('../index_file.json','w',encoding='utf-8') as g:
        json.dump(words_dic,g)
    return words_dic



