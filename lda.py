from gensim import corpora, models
from getStopwords import create_stopwords
from xml.sax.saxutils import unescape
import unicodedata, re, os
import pprint, emoji, mojimoji
import MeCab

def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

print('テキストフォルダ')
path = input('>> ')
txtlist = os.listdir('./text/{}'.format(path))

stop_words = create_stopwords('stop_words.txt')

words_list=[]

mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

mecab.parse('')

for name in txtlist:
    add_list = []
    txt = open("./text/{}/{}".format(path, name), "r")
    txts = txt.readlines()
    for line in txts:
        if line.find('\n'):
            line = line.replace('\n','')
        # 絵文字削除
        removed_emoji = remove_emoji(line)
        # 特殊文字デコード
        decmoji = unescape(removed_emoji)
        # 半角カナを全角に
        han2zen = mojimoji.han_to_zen(decmoji, ascii=False, digit=False)
        # 全角数字を半角に
        zen2han = mojimoji.zen_to_han(han2zen, ascii=False, kana=False)
        # @xxx リプライ時のユーザ名を削除
        norep = re.sub(r'@[0-9a-zA-Z_:]*', "", zen2han)
        # ハッシュタグ削除
        notag = re.sub(r'#.*', "", norep)
        # url 削除
        nourl = re.sub(r'(https?)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)', "", notag)
        # 半角数字を0に置き換え
        tozero = re.sub(r'\d+', '0', nourl)
        # 連続した0を削除
        nozero = re.sub(r'0*', '', tozero)
        # 英語を小文字に統一
        ko = nozero.lower()
        # normalize
        normal = unicodedata.normalize('NFKC',ko)
        # 半角記号を削除
        reui = re.sub(re.compile("[!-/:-@[-`{-~]"), '', normal)
        # 形態素解析
        node = mecab.parseToNode(reui)
        while node:
            part = node.feature.split(",")[0]
            if part == "BOS/EOS":
                node = node.next
                continue
            if node.feature.split(",")[6] == '*':
                word = node.surface
                w = word.lower()
            else:
                word = node.feature.split(",")[6]
                w = word.lower()

            if part == '名詞':
                if word not in stop_words and len(word) > 1:
                    add_list.append(word)
            node = node.next
    print(name + '：' + str(len(add_list)))
    words_list.append(add_list)
    txt.close()

#辞書作成
dic = corpora.Dictionary(words_list)
#出現頻度が低い単語と高い単語を取り除く
dic.filter_extremes(no_below=1, no_above=0.5)

pprint.pprint(dic.token2id)
#コーパスを作成
corpus = [dic.doc2bow(text) for text in words_list]

topic_N = 12

lda = models.LdaModel(corpus=corpus, num_topics=topic_N, id2word=dic)

lda.save('tweets_lda.model')

for i in range(topic_N):
    print("\n")
    print("="*80)
    print("TOPIC {0}\n".format(i))
    topic = lda.show_topic(i)
    for t in topic:
        print("{0:20}{1}".format(t[0], t[1]))
