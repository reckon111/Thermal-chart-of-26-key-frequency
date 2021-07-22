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
    f1=open('t_shuangpin.txt',encoding='utf-8')
    txt_shuangpin=f1.read()
    txt=f.read()
    txt_zhongwen = re.sub(r"[^\u4e00-\u9fa5]",'',txt)
    
    txt_pinyin=pypinyin.slug(txt_zhongwen,separator='')


    calfre(txt_shuangpin,d)
    
    change(d,l,l1)
    l1.sort(key=lambda x:x[1],reverse=True)
    labels=np.array([['Q(iu)','W(ei)','E(e)','R(uan)','T(ue,\n ve)',
                      'Y(un)','U(sh)','I(ch)','O(uo,\n o)','P(ie)'],
                     ['','A(a)','S(ong,\n iong)','D(ai)','F(en)','G(gen)',
                      'H(ang)','J(an)','K(uai,\n ing)','L(uang,\n iang)'],
                     ['','','Z(ou)','X(ua,\n ia)','C(ao)','V(ui,\n v)',
                      'B(in)','N(iao)','M(ian)','']])
    
    f, ax = plt.subplots(1,1)
    sns.heatmap(np.array(l),cmap='Reds',annot = labels, fmt ='',
                xticklabels=False, yticklabels=False,ax=ax,square=True,cbar=False,linewidths=0.05)
    ax.set_title('（小鹤双拼）26个字母键的使用频率热力图')
    plt.rcParams['font.sans-serif']=['SimHei']

    var = np.var([i[1] for i in l1])
    sa  = len(txt_shuangpin)/len(txt_zhongwen)
    ax.set_xlabel('双拼输入时，26键使用频率方差为：{:.4f}\n 双拼输入时，平均 {:.4f} 字母对应一个汉字'.format(var,sa))
    
    data=[ [i[1]/100] for i in l1]
    y_label = [ i[0] for i in l1]
    f, ax = plt.subplots(1,1)
    sns.heatmap(data,cmap='Reds',annot = True, fmt = "%",
                xticklabels=False,yticklabels=y_label,ax=ax)
    ax.set_title('（小鹤双拼）26个字母键的使用频率热力图')
    
    plt.show()

