import string,re
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import xml.dom.minidom as xmldom
import json
#nltk.download('stopwords')


def preprocessing(filename,dom1,dom2,dom3):

    # to get the element in the target xml file
     xml_file = xmldom.parse('../../collections/'+filename);

     root =xml_file.documentElement


     id=root.getElementsByTagName(dom1)

     head=root.getElementsByTagName(dom3)

     text=root.getElementsByTagName(dom2)

    # to merge the headline into the xml's doc content
     text_content=''
     for i in  range(0,text.length):
         text_content=head[i].firstChild.data
         text_content=text_content+text[i].firstChild.data
         text[i].firstChild.data=text_content

    # define a regular expression . remove all characters except numbers 0-9 and a-z
     r_not_letter = '[^a-zA-Z0-9]+'

     ps = PorterStemmer()

    #read the stopwords file and write into a list
     stop_words=[]
     with open("../englishST.txt",'r',encoding='utf-8') as e:
         line = e.readline()
         while line:
              line = line.strip()
              line = line.split()
              stop_words.extend(line)
              line = e.readline()

     #remove all punctuations and change uppercase to lowercase
     words_list=[]
     for i in range(0,text.length) :
              line = text[i].firstChild.data
              line = line.lower()
              line = re.sub(r_not_letter,' ', line)
              line = line.lower()
              #text[i].firstChild.data=line
              words = line.split();
              line = ""
              #remove all stopwords from xml's content and stem all words
              for r in words:
                    if not r in stop_words:
                            r = ps.stem(r)
                            words_list.append(r)
                            line += r
                            line += " "
              text[i].firstChild.data = line

    #remove redundant words
     words_list=list(set(words_list))

    #write all processed words into file
     with open("../pg10_new.txt",'w',encoding='utf-8') as g:
         for items in words_list:
             g.write(items)
             g.write('\n')

     with open("../words_list.json",'w',encoding='utf-8') as f:
            json.dump(words_list,f)

     return words_list,text,id



#+preprocessing('trec.sample.xml', 'DOCNO', 'TEXT','HEADLINE')