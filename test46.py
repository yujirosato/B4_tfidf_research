#test42.pyまでの進捗　12個のtfidfを正規化したのち、標準偏差順に並び替える
#12ヵ月分のtfidfの平均をとって、トップとの差を求める。
#→最大値が１なので、平均が少ない値順にソートすればいい。
import MeCab
from collections import Counter


####################標準偏差を求める#########################
def calculate_mean(data):
    s = sum(data)
    N = len(data)
    mean =s/N

    return mean

#平均からの偏差を求める
def find_difference(data):
    mean = calculate_mean(data)
    diff = []

    for num in data:
        diff.append(num-mean)
    return diff

def calculate_variance(data):
    diff = find_difference(data)
    #差の２乗を求める
    squared_diff = []
    for d in diff:
        squared_diff.append(d**2)

    #分散を求める
    sum_squared_diff = sum(squared_diff)
    variance = sum_squared_diff/len(data)
    return variance

############################################
def min_max(x):########正規化する関数、返り値は正規化後の配列########
    xmin = min(x)
    xmax = max(x)
    result = []

    for i in x:
        result.append((i-xmin)/(xmax-xmin))

    return result

####################################################
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
    stop = []
    for i in range(12):
        if i > 9:
            filename = file + str(i) + txt #filename更新
            print(str(code) + " " + filename + "　　　　解析中")
        else:
            filename = file + o + str(i) + txt
            print(str(code) + " " + filename + "　　　　解析中")


        with open(filename, "r") as f:
            line = f.readline()
            while line:
                line = line.split() #ここに[0]データ番号と[1]日付、[3]レビューが入ってる。
                line2 = line[1].split('/')#line2[1]に月

                if code == line[0]:
                    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/') # 形態素解析器の変数（オブジェクト）を作成
                    line3 = t.parse(line[3])#レビューの形態素解析
                    ward = [ward.replace('\t',',').split(',') for ward in line3.split('\n')[:-2]]
                                    #形態素解析データを分割してリストに
                    for x in ward:#wardの中身を参照　名詞があったらcounter用リストに追加
                        if name in x[1]:
                            data.append(x[0])
                            stop[x[0]] = 0

                line = f.readline()


    counter = Counter(data)

    #with open("test47_upnow", "w") as f:  # w:上書きモード
    #    f.write("code : " + str(code) + "\n")
    #    for word, cnt in counter.most_common():
    #        if cnt > 9:
    #            f.write(word + ":" + str(cnt) + "\n")
    for word, cnt in counter.most_common():
        if cnt > 9:      ########stopwordにする閾値
            stop[word] = cnt######辞書型のキーに出現頻度10以上の名詞、値に出現回数


    return stop###返り値は辞書型
##############################################################

def aaa(code):

    s_filename = code + "_test42"

    data = {}#キーに名詞、バリューに正規化したtfidfリスト
    data_std = {}#キーに名詞、バリューに正規化した標準偏差
    #b = "上"
    c  = []


    with open(s_filename, "r") as f:
        line = f.readline()
        while line:
            line = line.split()

            data[line[0]] = []#########[value]正規化したtfidfの格納場所
            data_std[line[0]] = []#####[value]正規化した標準偏差

            line = f.readline()


    with open(s_filename, "r") as f:
        line = f.readline()
        while line:
            line = line.split()

            #if line[0] == b:
            #     break


            #data[line[0]] = []
            #print(" : line = " + str(line))

            line_2 = line[2].split('[')#tfidfリストの要素１つ目の[を取り除く処理
            line_13 = line[13].split(']')
            line[2] = line_2[1]
            line[13] = line_13[0]


            for i in range(2,14):    #雑処理
                a = line[i].split(',')
                line[i] = a[0]
                c.append(float(a[0]))#tfidf値だけの処理

            #print(line[0] + " : " + str(c))
            c = min_max(c)#########正規化したリスト###########
            data[line[0]] = c

            variance = calculate_variance(c)
            #print('分散の値は:{0}'.format(variance))

            std = variance**0.5

            data_std[line[0]] = std#辞書型にキーに名詞、バリューに標準偏差
            #print('標準偏差は:{0}'.format(std))


            c = []
            #print(str(line[0]) + "" + str(data[line[0]]) +
             #"　標準偏差 " + str(data_std[line[0]]))

            line = f.readline()

    w_filename = code + "_test42"
    print(w_filename)
    with open(w_filename, "w") as f:  # w:上書きモード
        for k, v in sorted(data_std.items(), key=lambda x: x[1]):
            f.write(str(k) + " : " + str(data[k]))
            f.write("\n")








filename = "review_num"
line3_num = []
i = 0
with open(filename, "r") as f:
    line_num = f.readline()
    while line_num:
        line_num = line_num.split()
        line2_num = line_num[0].split('[')
        line2_num = line2_num[1].split(']')
        line3_num.append(line2_num[0])
        if i > 200:
            break

        print(line2_num[0])
        aaa(line2_num[0])
        i = i + 1
        line_num = f.readline()




#
