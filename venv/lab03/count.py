import xlwt
from xlwt import Workbook

with open('../pg10_new.txt','r',encoding='utf-8') as f:
    readline = f. readline()
    #print(readline)
    word = []
    while readline:
        readline = readline.strip()
        word_list = readline.split(' ')
        #print(word_list)
        word.extend(word_list)
        readline = f.readline()
    dic = {}
    dic = dic.fromkeys(word)
    word_name = list(dic.keys())
    for i in word_name:
        dic[i] = word.count(i)
    del dic['']
    word_sort = {}
    word_sort =sorted(dic.items(),key=lambda d:d[1],reverse=True)
    #i=0
    # to create a excel file and write data into it
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet1')
    sheet1.write(0,0,"Words")
    sheet1.write(0,1,"Frequence")
    sheet1.write(0,2,"Rank")
    sheet1.write(0,3,"Result")
    i=1
    for x,y in word_sort:
        print(" %s, %d" %(x,y))
        sheet1.write(i,0,x)
        sheet1.write(i,1,y)
        sheet1.write(i,2,i)
        sheet1.write(i,3,i*y)
        i=i+1
    wb.save("../pg10_new.xls")