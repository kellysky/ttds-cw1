import  xml.dom.minidom as xmldom
import  re
import pandas as  pd
import numpy as np
import  sys
sys.path.append("../../venv/labe03")
import tokenisation

#generate a matrix
def boolean_matrix(words,text,id):
   #define a two dimension matrix
   words_table = np.zeros([len(words),text.length],dtype=int)
   print('start loop')
    #iterate words to store its boolean value in matrix
   x=0
   for i in words:
       for y in range(0,text.length):
           line=text[y].firstChild.data.strip()
           line = line.split(" ")
           doc_id=id[y].firstChild.data.strip()
           if i in line:
                words_table[x][y]=1
           else:
                words_table[x][y]=0
       x=x+1
   print('loop end')
    #transpose the matrix to make the rows become doc id and the columns become words and store the matrix in dataframe
   words_table=np.transpose(words_table)
   df=pd.DataFrame(words_table,columns=words)
   print('start')
   df.to_json(r'../Export_DataFrame.json')
   print('complete')
   return df


