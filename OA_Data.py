#coding=utf-8
"""
Spyder Editor

This is a temporary script file.
"""

import re

import csv


from bs4 import BeautifulSoup


def trans():
    st = ""
    cou = 0
    with open("C:\\Users\\tiaze\\Desktop\\oa机型配置\\OA\\20180329.txt","r") as f:
        for i in f.readlines():
            if("START" in i):
                continue
            if("END" in i):  
                with open("C:\\Users\\tiaze\\Desktop\\oa机型配置\\OA"+str(cou)+".html","w") as f1:
                    rst = st.split('\n')
                    del rst[0]
                    del rst[-2:]
                    f1.write('\n'.join(rst))
                    cou+=1
                st = ""
                continue
            st += i
    return cou

def trans1(i, dic, key,flag):
    st = ""

    for j in i.find_all("td"):
            
            for k in j.stripped_strings:
                st += k
            st = u'%s'%st
    value = ""
    if(flag == 1):  
        st = st.replace('\n','')
        pattern = re.compile(r'(、|（|\.)(.*)(）|：|:)')
        value = pattern.search(st).group(2)
    else:
        st = st.replace('\n','')
        value = st
    dic[key] = value


def trans2(i, dic):

    tdc = 0
    key = ""
    value = ""
    for j in i.find_all("td"):
        tdc += 1
        st = ""
        for k in j.stripped_strings:
            st += k
        if(tdc % 2 == 1):
            st = st.replace('\n','')
            st = st.replace(u'■','1')
            st = st.replace(u'□','0')
            key = st
        elif(tdc % 2 == 0):
            st = st.replace('\n','')
            st = st.replace(u'■','1')
            st = st.replace(u'□','0')
            value =  st
            dic[key] = value


def trans3(i, dic):

        tdc = 0
        key = ""
        value = ""
        for j in i.find_all("td"):
            tdc += 1
            st = ""
            for k in j.stripped_strings:
                st += k
            if(tdc % 3 == 1):
                st = st.replace('\n','')
                key = st
            elif(tdc % 3 == 2):
                value =  st.replace('\n','')
            else:
                dic[key] = value
        dic[key] = value


def trans4(i, dic):

        key = ""
        value = ""
        for j in i.find_all("td"):
            cou = 0
            for k in j.stripped_strings:
               if(cou % 2 == 0):
                   '''
                   pattern = re.compile(ur'■')
                   if pattern.match(k):
                       value = 1
                       '''
                   k = k.replace(u'■','1')
                   k = k.replace(u'□','0')
                   value = k.replace('\n','')
               elif(cou % 2 == 1):
                   key = k.replace('\n','')
                   dic[key] = value  
               cou += 1

def trans5(i, dic):

        tdc = 0
        key = ""
        value = ""
        for j in i.find_all("td"):
            
            st = ""
            for k in j.stripped_strings:
                st += k
            if(tdc == 0):
                continue
            elif(tdc % 2 == 1):
                st = st.replace('\n','')
                key = st
            elif(tdc % 2 == 0 and tdc != 0):
                st = st.replace('\n','')
                value =  st
                dic[key] = value
            tdc += 1
        dic[key] = value


def trans0(i, dic):

        value = ""
        for j in i.find_all("td"):
            st = ""
            for k in j.stripped_strings:
                st += k
        
        st = st.replace('\n','')
        
        pattern = re.compile(r'(■[^■□]*|□[^■□]*)')
        value = pattern.findall(u'%s'%st)
        for i in value:
            i = i.replace(u'■','1')
            i = i.replace(u'□','0')
            key = i[1:].replace('\n','')
            value = i[0:1].replace('\n','')
            dic[key] = value


def collect(i, key_t):

        st = ""
        for j in i.find_all("td"):
                for k in j.stripped_strings:
                    st += k
        st = st.replace('\n','')
        pattern = re.compile(r'(、|（|\.)(.*)(）|：|:)')
        value = pattern.search(u'%s'%st).group(2)
        key_t[0] = value


def options(i, dic, key):

        cou = 0
        for j in i.find_all("td"):
            cou += 1
            if(j.string):
                dic[key] = cou 


def level(i, dic, trc, plist):

        st = ""
        for j in i.find_all("td"):
                for k in j.stripped_strings:
                    st += k+'|'
        st = st.replace('\n','')
        if(trc==(plist[1]+1)):
            dic[u"定位"] = st
        elif(trc==(plist[1]+3)):
            dic[u"等级"] = st


def pos(i, dic, trc):

        st = ""
        for j in i.find_all("td"):
                for k in j.stripped_strings:
                    st += k
        st = st.replace('\n','')
        pattern = re.compile(r'([A-Z]|[一二三四五六七])(、|（|\.)(.*)(）|：|:)')
        st = u'%s'%st
        
        if pattern.match(st):
            key = pattern.match(st).group(1) + pattern.match(st).group(3)
            dic[key] = trc

def match(i, dic, trc, plist):
    
    if(trc in {1}):
        trans1(i, dic, u"字段"+str(trc),1)
    elif(trc in plist):
        return 
    elif(trc in {plist[0]+1}):
        key_t = [u"产品来源"]
        trans1(i, dic, key_t[0],0)
    elif(trc in {plist[1]+1,plist[1]+3}):
        level(i, dic, trc, plist)
    elif(trc in {plist[5]-4,plist[5]-2,plist[5]-1}):
        trans3(i, dic)
    elif(trc in {plist[1]+2,plist[1]+4}):
        options(i, dic, u"字段"+str(trc))
    elif(trc in {plist[6]+1,plist[6]+2,plist[6]+3,plist[6]+5,plist[11]+1}):
        trans5(i, dic)
    elif(trc in {plist[7]+1,plist[7]+2,plist[7]+3,plist[7]+4,plist[7]+5,plist[7]+6}):
        trans4(i, dic)
    elif(trc in {plist[10]+1}):
        trans0(i, dic)
    else:
        trans2(i,dic)
    

def read(filen):
    trc = 0
    soup = BeautifulSoup(open(filen),'html.parser',from_encoding='gbk')
    dic = {}
    pdic = {}
    for i in soup.find_all("tr"):
        trc += 1
        pos(i, pdic, trc)
        
    plist = list(pdic.values())
    plist = sorted(plist)

    trc = 0
    for i in soup.find_all("tr"):
        trc += 1
        match(i, dic, trc, plist)
        
    return dic
   # dataframe = pd.DataFrame.from_dict(dic,orient='index').T
   # dataframe.to_csv("C:\\Users\\HP\\Desktop\\OA\\temp.csv",index=False,sep=',',encoding="utf-8")
    
    #for key, value in dic.items():
    #    print 'key is %s,value is %s'%(key, value)
    #1139 1350           
if __name__ == '__main__':
    csvFile=open("c:\\users\\tiaze\\desktop\\oapeizhi\\OA\\resultnew.csv","a")
    field = set()
    
    name = "C:\\Users\\tiaze\\Desktop\\oapeizhi\\OA\\1518.html"
    dic = read(name)
    field = field | set(dic.keys())
    dict_writer = csv.DictWriter(csvFile,field)
    dict_writer.writeheader()
    dic2 = read(name)
    dict_writer.writerow(dic2)
    csvFile.close()
    '''cou = trans()
    csvFile = open("C:\\Users\\tiaze\\Desktop\\oa机型配置\\OA\\resultnew.csv","a")
    field = set()
    for i in range(1516,1521):
       try:
           name = "C:\\Users\\tiaze\\Desktop\\oa机型配置\\OA\\%d.html"%i
           dic = read(name)
           field = field | set(dic.keys())
       except Exception as e:
           print (e)
           print ('%d'%i+'====')
           
    dict_writer = csv.DictWriter(csvFile,field)
    dict_writer.writeheader()
    for i in range(1516,1521):
       try:
           name = "C:\\Users\\tiaze\\Desktop\\oa机型配置\\OA\\%d.html"%i
           dic = read(name)
           dict_writer.writerow(dic)
       except Exception as e:
           print (e)
           print (i)
    csvFile.close()
    print("the program is done running")'''
    '''filen="C:\\Users\\tiaze\\Desktop\\oapeizhi\\OA\\1518.html"
    soup = BeautifulSoup(open(filen),'html.parser',from_encoding='gbk')
    dic = {}
    pdic = {}
    for i in soup.find_all("tr"):
        for j in i.stripped_strings:
            print(j)'''
            
