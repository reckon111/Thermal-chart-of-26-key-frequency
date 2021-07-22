import pypinyin
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def calfre(txt,d):
    for i in 'abcdefghijklmnopqrstuvwxyz':
        fre=txt.count(i)/len(txt)
        d[i]=round(fre*100,2)
def change(d,l,l1):
    a=2
    b=1
    c=0
    for i in 'zxcvbnm':
        l[2][a]=d[i]/100
        a+=1
    for i in 'asdfghjkl':
        l[1][b]=d[i]/100
        b+=1
    for i in 'qwertyuiop':
        l[0][c]=d[i]/100
        c+=1
    for i in d:
        l1.append((i.upper(),d[i]))
    
if __name__ == "__main__":
    d={}
    l=[[0 for col in range(10)] for row in range(3)]
    l1=[]
    
    f=open('t1.txt',encoding='utf-8')
    txt=f.read()
    txt_zhongwen = re.sub(r"[^\u4e00-\u9fa5]",'',txt)  #将文本变为全中文
    txt_pinyin=pypinyin.slug(txt_zhongwen,separator='')#将全中文变为全拼音
    calfre(txt_pinyin,d) #计算每个字母出现的频率

    #做热力图
    change(d,l,l1)
    l1.sort(key=lambda x:x[1],reverse=True)

    labels=np.array([['Q','W','E','R','T','Y','U','I','O','P'],
                     ['','A','S','D','F','G','H','J','K','L'],
                     ['','','Z','X','C','V','B','N','M','']])
    
    f, (ax1, ax2) = plt.subplots(figsize=(10,10),ncols=2)
    sns.heatmap(np.array(l),cmap='Reds',annot = labels, fmt ='',
                xticklabels=False, yticklabels=False,ax=ax1,square=True,cbar=False)
    ax1.set_title('26个字母键的使用频率热力图(全拼)')
    plt.rcParams['font.sans-serif']=['SimHei']

    var = np.var([i[1] for i in l1])
    sa  = len(txt_pinyin)/len(txt_zhongwen)
    ax1.set_xlabel('全拼输入时，26键使用频率方差为：{:.4f}\n 全拼输入时，平均 {:.4f} 字母对应一个汉字'.format(var,sa))
    
    data=[ [i[1]/100] for i in l1]
    y_label = [ i[0] for i in l1]
    sns.heatmap(data,cmap='Reds',annot = True, fmt = "%",
                xticklabels=False,yticklabels=y_label,ax=ax2)
    ax2.set_title('26个字母键的使用频率热力图(全拼)')
    
    plt.show()


