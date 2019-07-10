#code_test42のテキストファイルを開いて平均の小さい順に並び替え
######前処理をし忘れていたので今追加
import MeCab
from collections import Counter

#################平均を求める関数######################
def ave(x):
    n = 0
    sum = 0
    for i in x:
        n = n + 1
        sum = i + sum

    return sum/n

####################################################

###########################出現回数の少ないストップワードを摘出##########

def stop(code):
    o = "0"
    file = "userReview"
    txt = ".txt"
    name = '名詞'
    #code = input("code ?: ")
    data = []
    stop = {}
    for i in range(12):
        if i > 9:
            filename = file + str(i) + txt #filename更新
            print(str(code) + " " + filename + "　　　　ストップワード作成中")
        else:
            filename = file + o + str(i) + txt
            print(str(code) + " " + filename + "　　　　ストップワード作成中")


        with open(filename, "r") as f:
            line = f.readline()
            while line:
                line = line.split() #ここに[0]データ番号と[1]日付、[3]レビューが入ってる。
                line2 = line[1].split('/')#line2[1]に月

                if str(code) == line[0]:
                    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/') # 形態素解析器の変数（オブジェクト）を作成
                    line3 = t.parse(line[3])#レビューの形態素解析
                    ward = [ward.replace('\t',',').split(',') for ward in line3.split('\n')[:-2]]
                                    #形態素解析データを分割してリストに
                    for x in ward:#wardの中身を参照　名詞があったらcounter用リストに追加
                        if name in x[1]:
                            data.append(x[0])


                line = f.readline()


    counter = Counter(data)

    #with open("test47_upnow", "w") as f:  # w:上書きモード
    #    f.write("code : " + str(code) + "\n")
    #    for word, cnt in counter.most_common():
    #        if cnt > 9:
    #            f.write(word + ":" + str(cnt) + "\n")
    with open("108_test48_stop", "w") as f:  # w:上書きモード
        for word, cnt in counter.most_common():
            f.write(str(word) + " : " + str(cnt) + "\n")
            if cnt < 10:      ########stopwordにする閾値
                stop[word] = cnt######辞書型のキーに出現頻度9以下の名詞、値に出現回数


    return stop###返り値は辞書型
##############################################################

code = input("code ?: ")
filename = str(code) + "_test42"

data = {}
data_stop = {}
word = {}
c = []
with open(filename, "r") as f:#辞書型を初期化するために一旦開く
    line = f.readline()
    while line:
        line = line.split()
        data[line[0]] = []####キーに名詞、値に12個のtfidf
        word[line[0]] = 0###キーに名詞、値にその名詞のtfidfの平均値
        line = f.readline()

with open(filename, "r") as f:
    line = f.readline()
    while line:
        line = line.split()

        line_2 = line[2].split('[')#tfidfリストの要素１つ目の[を取り除く処理
        line_13 = line[13].split(']')
        line[2] = line_2[1]
        line[13] = line_13[0]


        for i in range(2,14):    #雑処理
            a = line[i].split(',')
            line[i] = a[0]
            c.append(float(a[0]))#配列cに対して、tfidf値を12個格納

        data[line[0]] = c
        c = []

        line = f.readline()


data_stop = stop(code)#使用しない名詞の辞書型


for n in data:
    word[n] = ave(data[n])


w_filename = str(code) + "_test48"
print(w_filename)
with open(w_filename, "w") as f:  # w:上書きモード
    for k, v in sorted(word.items(), key=lambda x: x[1]):
        if str(k) not in data_stop:
            f.write(str(k) + " : " + str(data[k]))
            f.write("\n")






    #
