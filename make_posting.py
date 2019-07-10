#ポスティングリストを作る
#月ごとのスティングリスト
from collections import Counter
import MeCab
import sys
import string
import math
from collections import OrderedDict
from numpy import *

name = '名詞'#ここを変更する
month = 0
nouncount = 0
mn = 1
k = 0
o = "0"
file = "userReview"
txt = ".txt"
monthdata = []
r = 1
data = []
alldata = []
alldata1 = []
adventmonth = {}
monthcount = 1
posting = {}

#作りたいポスティングリストの月
month = "12"

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
            if line2[1] == month:
                code = line[0]

                t = MeCab.Tagger(' '.join(sys.argv)) # 形態素解析器の変数（オブジェクト）を作成
                line3 = t.parse(line[3])#レビューの形態素解析
                ward = [ward.replace('\t',',').split(',') for ward in line3.split('\n')[:-2]]
                        #形態素解析データを分割してリストに

                for x in ward:#wardの中身を参照　名詞があったらcounter用リストに追加
                    if name in x[1]:
                        if  x[0] in posting:#ポスティングリストの中身に名詞があるかどうか参照
                            posting[x[0]].append(code)
                        else:#入っていなかったら追加
                            posting[x[0]] = [code]

            line = f.readline()


#作りたいポステイングリストの名前を月ごとに変更
with open("posting_12", "w") as f:  # w:上書きモード
    for i in posting:
        f.write(str(i))
        for n in posting[i]:
            f.write(',' + str(n))


        f.write("\n")
