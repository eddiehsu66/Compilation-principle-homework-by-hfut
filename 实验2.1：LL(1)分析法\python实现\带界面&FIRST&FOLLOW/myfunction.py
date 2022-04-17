#用于完善编译原理实验二，加入first and follow集合
import string,copy,myfunction
from tkinter import *
class Stack:#构建栈
    def __init__(self,initial=None):
        self.st=[]
        if initial != None:
            self.st.append(initial)
    def isempty(self):
        return len(self.st)==0
    def push(self,info):
        self.st.append(info)
    def pop(self):
        return self.st.pop()
    def size(self):
        return len(self.st)
    def show(self):
        if len(self.st)==0 :
            return ''
        return self.st
    def show_last_one(self):
        if len(self.st)!=0:
            return self.st[-1]
    def clear(self):
        self.st.clear()
grammer={}#使用字典来存放语法
vn=[]#非终结符号
vt=[]#终结符号
FIRST={}#使用字典来存储first集合
FOLLOW={}#使用字典来存储follow集合
analysis={}#使用字典中字典来存储转移表
def read_text():#从文档中读
    r=open("text.txt",'r')
    line=r.readline()
    while(line):
        if '\n' in line:
            line=line[:-1]
        med=line.index('->')
        if line[0] not in grammer.keys():
            grammer[line[0]]=[line[med+2:]]
        else:
            grammer[line[0]].append(line[med+2:])
        med = [i.split('|') for i in grammer[line[0]]]
        grammer[line[0]] = [i for item in med for i in item]
        line=r.readline()
    r.close()
def pro_deal():#预处理，构建vt和vn
    for i in grammer.keys():
        vn.append(i)
    for values in grammer.values():
        for value in values:
            for i in value:
                if i not in string.ascii_uppercase:
                    if i not in vt:
                        vt.append(i)
def filter_e(result,item):#对于1<=j<=i-1,e in first(xj)中，则此函数返回i的数值
    for index,word in enumerate(item):
        if 'e' not in result[word]:
            return index
def get_first():
    for x in vt+vn:
        FIRST[x]=set()
        if x in vt:#规则一
            FIRST[x].update(x)
    sum=0
    med=1
    while(sum!=med):
        med=sum
        sum=0
        for x in vt + vn:
            if x in vn:  # 当为非终结符号的时候
                for item in grammer[x]:
                    if item == 'e':  # 规则2.2
                        FIRST[x].update('e')
                    elif item[0] in vt + vn:  # 规则2.1
                        FIRST[x].update(FIRST[item[0]])
                    if filter_e(FIRST, item):
                        if filter_e(FIRST, item) == len(item):
                            FIRST.update('e')
                        else:
                            FIRST[x].update(FIRST[filter_e(FIRST, item) + 1])
        for i in vt+vn:
            sum=sum+len(FIRST[i])
def get_product(element):#通过单一元素，反向找到其的产生式
    result={}
    for i in vn:#初始化
        result[i]=set()
    for i in vn:#进行筛选
        for item in grammer[i]:
            if len(item)>=2 and item[1]==element:
                result[i].add(item)
    for i in vn:#删除空集合的键值对
        if len(result[i])==0:
            del result[i]
    return result
def get_follow():
    for x in vn:
        FOLLOW[x] = set()
    sum = 0
    med = 1
    while (sum != med):
        med=sum
        sum=0
        for x in vn:
            if x ==vn[0]:
                FOLLOW[x].update('#')
            tem=get_product(x)#存储函数返回来的字典
            for key in tem.keys():
                for value in tem[key]:
                    if len(value)==3:
                        FOLLOW[x].update(FIRST[value[2]]-{'e'})
                        if 'e' in FIRST[value[2]]:
                            FOLLOW[x].update(FOLLOW[key])
                    if len(value)==2:
                        FOLLOW[x].update(FOLLOW[key])
        for i in vn:
            sum=sum+len(FOLLOW[i])
def get_analysis():#获得分析表
    vt_new=copy.deepcopy(vt)
    vt_new.append('#')#vt_new来表示表格列名
    vt_new.remove('e')
    for i in vn:#vn为表格行名
        analysis[i]={}#典中典
        for j in vt_new:
            analysis[i][j]=set()
    for key in grammer.keys():#对语法的遍历
        for value in grammer[key]:
            for i_vt in analysis[key].keys():
                if i_vt in FIRST[value[0]]:
                    analysis[key][i_vt].add(value)
            if 'e' in FIRST[value[0]]:
                for i_vt in analysis[key].keys():
                    if i_vt in FOLLOW[key]:
                        analysis[key][i_vt].add(value)
    for key in list(analysis.keys()):
        for value in list(analysis[key].keys()):
            if len(analysis[key][value])==0:
                analysis[key].pop(value)
