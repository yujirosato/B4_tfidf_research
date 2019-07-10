#名詞の持つ１２ヶ月分のtfidfの値を標準偏差の大きい順に出力

from collections import Counter
import MeCab
import sys
import string
import math
from collections import OrderedDict
from numpy import *



#############この関数でtf値を出力
def aaa(code):
    print("[" + code + "]" + "解析中")


    name = '名詞'#ここを変更する

    nsd = 0#文書dの中の全ての名詞の出現頻度
    o = "0"
    file = "userReview"
    txt = ".txt"
#    code = input('hotel ID:')
    data = {}
    counter = {}
    ward_tfidf = {}#キーに名詞をもち、値は12個のtfidf値をもつ辞書
    ward_tf = {}#その名詞のtf値
    s = {}
    ss = {}
    i = 0
    for i in range(12):
        h = str(i+1)
        if i < 9:
            h = "0" + str(i+1)
        data[h] = []           ######data{辞書}とcounter{辞書}の初期化
        counter[h] = []

    for i in range(12):
        if i > 9:
            filename = file + str(i) + txt #filename更新
            print(filename)
        else:
            filename = file + o + str(i) + txt
            print(filename)

        with open(filename, "r") as f:
            line = f.readline()
            while line:
                line = line.split() #ここに[0]データ番号と[1]日付、[3]レビューが入ってる。
                line2 = line[1].split('/')#line2[1]に月
                #print(line[3])

                if code == line[0]:
                    month = line2[1]
                    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/') # 形態素解析器の変数（オブジェクト）を作成
                    line3 = t.parse(line[3])#レビューの形態素解析
                    ward = [ward.replace('\t',',').split(',') for ward in line3.split('\n')[:-2]]
                            #形態素解析データを分割してリストに

                    for x in ward:#wardの中身を参照　名詞があったらcounter用リストに追加
                        if name in x[1]:
                            data[str(month)].append(x[0])
                            s[x[0]] = ''
                            ward_tfidf[x[0]] = []
                            ward_tf[x[0]] = []
                    flag = 0

                line = f.readline()


    for i in range(12):
        nsd = 0#その月の全ての単語の出現回数
        h = str(i+1)
        if i < 9:
            h = "0" + str(i+1)
        counter[h] = Counter(data[h])#1月から12月までの出現回数が辞書型の中にリストで集約

        for word, cnt in counter[h].most_common():
            nsd = nsd + cnt#その月の全ての単語の出現回数

        for word, cnt in counter[h].most_common():
            tf = 0
            tf = cnt / nsd
            ward_tf[word].append(tf)

        for k in ward_tf:
            if len(ward_tf[k]) == i:
                ward_tf[k].append(0)#その名詞のtf値



    #####ここからidf値を出すためのコード##########################################

    posdata = []#捨てリスト
    posid = {}
    idfdata = {}
    N = 29400

    ############################################
    for i in range(12):
        month = str(i+1)
        if i < 9:#                    解析する月のループ
            month = "0" + str(i+1)
    #############################################
        posfilename = "posting_" + month#解析ファイルの指定

        with open(posfilename, "r") as f:
            posline = f.readline()
            while posline:
                posline = posline.split()
                posdata = posline[0].split(',')#poslineリストの要素0番目には名詞名

                for word, cnt in counter[month].most_common():
                    if posdata[0] == word:#ポスティングリストとtfとして文書内に出てきた名詞が一致した場合
                        n = 0             #psdata[0]は名詞名
                        idf = 0
                        poscount = 0
                        posid[word] = []
                        for po in posdata[1:]:#########posdataの要素数0番目はキー、
                                              #########１番目以降は値というのがこれしか表現できない
                            posid[word].append(po)

                        counter2 = Counter(posid[word])
                        for word2, cnt2 in counter2.most_common():#その名詞が出てきた文書数の種類の数
                            poscount = poscount + 1####同じ文書IDに出現している可能性があるので、この方法意外実現不可

                        idf = (N / (poscount + 1))
                        #idfdata[word] = math.log(idf)#その名詞に対するtfidf値を計算
                        ward_tfidf[word].append(math.log(idf) * ward_tf[word][i])


                posline = f.readline()

        for k in ward_tfidf:
            if len(ward_tfidf[k]) == i:
                ward_tfidf[k].append(0)




    ##############################################################################
    code_name = code + "_test38"
    with open(code_name, "w") as f:  # w:上書きモード


        for i in ward_tfidf:
            x_sum = 0
            s1 = 0
            j = 0
            jj = 0
            x_ave = 0

            for k in ward_tfidf[i]:##########標準偏差を求める
                x_sum = x_sum + k

            x_ave = x_sum / 12

            for x in ward_tfidf[i]:
                j = x - x_ave
                jj = j * j
                s1 = s1 + jj
                j = 0
                jj = 0

            s2 = s1 / 12

            s[i] = math.sqrt(s2)


        for k, v in sorted(s.items(), key=lambda x: -x[1]):
            ss[k] = v

        for i in ss:
            f.write(str(i) + " : " + str(ward_tfidf[i]))
            f.write("\n")











#####レビュー数の上位２００件のホテルについて分析

filename = "review_num"
i = 0
line3_num = []
with open(filename, "r") as f:
    line_num = f.readline()
    while line_num:
        line_num = line_num.split()
        line2_num = line_num[0].split('[')
        line2_num = line2_num[1].split(']')
        line3_num.append(line2_num[0])
        if i > 199:
            break

        i = i + 1
        line_num = f.readline()

i = 0
for code in line3_num:
    print(str(i) + "回目")
    aaa(code)
    i = i + 1








#
