#-*- coding: utf-8 -*-
from tqdm import tqdm
import codecs
from dask import delayed, compute
from dask.diagnostics import ProgressBar
from konlpy.tag import Kkma,Okt
from konlpy.utils import pprint
import gensim
from clean import *

def to_word(sentence_dic,kor_tag):
  #returns list of list with elements of important words
  out = []
  for i in tqdm(sentence_dic):
    out.append(imp_words(i,sentence_dic[i],kor_tag))
  return out


def imp_words(i, text, kor_tag):
# to do
#   make it work for all the taggers
    okt = Okt()
    out_list = []
    okt_stop = ['Eomi','Punctuation','Unknown', 'Josa','PreEomi', 'Conjunction', 'Punctuation', 'KoreanParticle']
    #print("Filtering words")
    try:
        #print(text)
        for sentence in text:
            for l in okt.pos(sentence):
                try:
                    if(okt_stop.index(l[1]) != -1):
                        continue
                except:
                    if(len(l[0]) > 1):
                        out_list.append(l[0])
    except:
        with codecs.open('./models/error_id_list.txt','a',encoding="utf-8") as f:
            f.write(str(i))
            f.write('\n')
    return out_list
def to_dictionary(sentence_dic, vocab_size):
    tmp = 0
    vocab = []
    dic = []
    kor_tag = "okt"
    print("To dictionary Started")
    for i in tqdm(sentence_dic):
        tmp = tmp +1
        if(tmp < vocab_size * len(sentence_dic)):
            dic.append(imp_words(i,sentence_dic[i],kor_tag))
        else:
            vocab.append(imp_words(i,sentence_dic[i],kor_tag))
    return dic,vocab
    
def train(load_model,sentence_dic,kor_tag,window,min_count,size,vocab_size):
    tmp = 0
    first = []
    print("Training started")
    for i in tqdm(sentence_dic):
        tmp = tmp +1
        first.append(imp_words(i,sentence_dic[i],kor_tag))
        if(tmp == vocab_size):
            break
    print("Number of intial Vocabulary input : " + str(len(first)))
    model = gensim.models.Word2Vec(first,window=window, min_count=min_count, size=size)
    for i in tqdm(sentence_dic):
        tmp = tmp +1
        if(tmp % 10000 == 0):
            model.save("./models/"+load_model)
        if(tmp < 5000):
            continue
        model.train([imp_words(i, sentence_dic[i],kor_tag)],total_examples=1,epochs=1)
    model.save("./models/"+load_model)
