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
    for i in ['Z(un)','X(in)','C(ai)','V(zh)',
              'B(ei)','N(eng)','M(ang)']:
        l[2][a]=d[i]/100
        a+=1
    for i in ['A(ing)','S(ie)','D(ia)','F(ou)','G(iang)',
              'H(uan)','J(ue)','K(en)','L(iao)']:
        l[1][b]=d[i]/100
        b+=1
    for i in ['Q(ian)','W(ui)','E(uang)','R(uo)','T(ao)',
              'Y(iu)','U(sh)','I(ch)','O(ong)','P(an)']:
        l[0][c]=d[i]/100
        c+=1
    for i in d:
        l1.append((i,d[i]))
    
if __name__ == "__main__":
    d={}
    l=[[0 for col in range(10)] for row in range(3)]
    l1=[]
    s=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
       'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
       'w', 'x', 'y', 'z','iu','ei','uan','ue','ve','un','uo',
       'ie','ong','iong','ai','en','eng','ang','an','uai','ing',
       'uang','iang','ou','ua','ia','ao','ui','in','iao','ian',
       'sh','ch','zh'] #所有的声母和韵母
    for i in s:
        d[i]=0
    

    f=open('t1.txt',encoding='utf-8')
    txt=f.read()
    txt_zhongwen = re.sub(r"[^\u4e00-\u9fa5]",'',txt)  #读取文本

    for i in txt_zhongwen:          #统计每个声母和韵母出现的次数
        c=pypinyin.slug(i)
        if len(c)>2 and c[1]=='h':
            d[c[0:2]]+=1
            d[c[2:]]+=1
        else:
            if len(c)==1:
                d[c]+=2  #单个字母 既是声母也是韵母 +2
            else:
                d[c[0]]+=1
                d[c[1:]]+=1
    l2=[]                          #26个字母出现的次数
    for i in 'abcdefghijklmnopqrstuvwxyz':
        l2.append([i,d[i]])
    l2.sort(key=lambda x:x[1],reverse=True)

    l3=[]                           #非26个字母出现的次数
    for i in d:
        if i not in 'abcdefghijklmnopqrstuvwxyz':
            l3.append([i,d[i]])
    l3.sort(key=lambda x:x[1],reverse=True)
    '''for i in l2:
        print(i[0],i[1])
    print()
    for i in l3:
        print(i[0],i[1])    
    print()'''
    d_rel={}

    #先将ch、sh、zh映射到 三个不能作为声母的字母上
    d_rel['{}({})'.format('I','ch')]=d['i']+d['ch']
    d_rel['{}({})'.format('U','sh')]=d['u']+d['sh']
    d_rel['{}({})'.format('V','zh')]=d['v']+d['zh']

    #去掉 已经关联过的i、u、v和ch、sh、zh
    for i in range(len(l2)):      
        if l2[i][0] in ['i','u','v']:
            l2[i][1]=0
    for i in range(len(l3)):
            if l3[i][0] in ['ch','sh','zh']:
                l3[i][1]=0           
    l2.sort(key=lambda x:x[1],reverse=False)
    l3.sort(key=lambda x:x[1],reverse=True)
    del l2[0:3]
    del l3[-3:]
    '''for i in l2:
        print(i[0],i[1])
    print()
    for i in l3:
        print(i[0],i[1])    
    print()'''
    #将剩下的 声母出现次数从小到大 与 韵母出现次数从大到小 关联起来，使得26键使用更加均衡。
    for i in range(len(l2)):
        d_rel['{}({})'.format(l2[i][0].upper(),l3[i][0])]=d[l2[i][0]]+d[l3[i][0]]
    #将多余的4个韵母与字母关联（出现次数较少）
    d_rel['T(ao)']+=l3[-1][1]    #ve 2
    d_rel['S(ie)']+=l3[-2][1]    #iong 4
    d_rel['K(en)']+=l3[-3][1]    #uai 13
    d_rel['L(iao)']+=l3[-4][1]    #uang 53
    #将26键出现次数转化为频率(%)
    sum0=sum([d_rel[i] for i in d_rel])
    for i in d_rel:
        d_rel[i]=d_rel[i]/sum0*100
        '''if i =='T(ao)':                      #,'S(ie)','K(en)','L(iao)'
            print('T(ao,ve)','{:.4f}%'.format(d_rel[i]))
        elif i=='S(ie)':
            print('S(ie,iong)','{:.4f}%'.format(d_rel[i]))
        elif i=='K(en)':
            print('K(en,uai)','{:.4f}%'.format(d_rel[i]))
        elif i=='L(iao)':
            print('L(iao,uang)','{:.4f}%'.format(d_rel[i]))
        else:
            print(i,'{:.4f}%'.format(d_rel[i]))'''
        #print(d_rel[i])

    #计算频率(%)方差
    var = np.var([d_rel[i] for i in d_rel])
    
    #做热力图
    change(d_rel,l,l1)
    l1.sort(key=lambda x:x[1],reverse=True)
    labels=np.array([['Q(ian)','W(ui)','E(uang)','R(uo)','T(ao,\n ve)',
                      'Y(iu)','U(sh)','I(ch)','O(ong)','P(an)'],
                     ['','A(ing)','S(ie,\n iong)','D(ia)','F(ou)','G(iang)',
                      'H(uan)','J(ue)','K(en,\n uai)','L(iao,\n uang)'],
                     ['','','Z(un)','X(in)','C(ai)','V(zh)',
                      'B(ei)','N(eng)','M(ang)','']])
    
    f, ax = plt.subplots(1,1)
    sns.heatmap(np.array(l),cmap='Reds',annot = labels, fmt ='',
                xticklabels=False, yticklabels=False,ax=ax,square=True,cbar=False,linewidths=0.05)
    ax.set_title('(优化双拼)26个字母键的使用频率热力图')
    plt.rcParams['font.sans-serif']=['SimHei']
 
    sa  = sum0/len(txt_zhongwen)
    ax.set_xlabel('优化双拼输入时，26键使用频率方差为：{:.4f}\n  优化双拼输入时，平均 {:.4f} 字母对应一个汉字'.format(var,sa))
    
    data=[ [i[1]/100] for i in l1]
    y_label = [ i[0][0] for i in l1]
    f, ax = plt.subplots(1,1)
    sns.heatmap(data,cmap='Reds',annot = True, fmt = "%",
                xticklabels=False,yticklabels=y_label,ax=ax)
    ax.set_title('(优化双拼)26个字母键的使用频率热力图')
    
    plt.show()
    


