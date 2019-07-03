#-*- coding: utf-8 -*-
from tqdm import tqdm
import codecs
from konlpy.tag import Kkma,Okt
from konlpy.utils import pprint
import gensim
from clean import *
from kiwipiepy import Kiwi
def kiwi_bow():
    '''
    Input: kiwi_bow.txt (text file including pre-cleaned words) 
    Output: list of kiwi-cleaned bag-of-word
    '''
    with codecs.open('kiwi_bow.txt','r',encoding="utf-8") as f:
        l = f.readline()
        cleaned_kiwi_words = {}
        # print("started \n_____________")
        tmp = 0
        while len(l) != 0:
            l = str(l).replace('\'','')
            l = str(l).replace('[','')
            l = str(l).replace(']','')
            l = str(l).replace('\n','')
            try:
                if tmp == 0:
                    idd = int(l)
                    tmp = 1
                else:
                    tmp = 0
                    cleaned_kiwi_words[idd] = l.split(',')
            except:
                    print("exception",idd,l)
                    l = f.readline()
                    continue
            l = f.readline()
    return cleaned_kiwi_words


def koala_bow():
    '''
    Input: koala_bow.txt (text file including pre-cleaned words) 
    Output: list of koala-cleaned bag-of-word
    '''
    with codecs.open("koala_bow.txt",'r') as f:
        l = f.readline()
        cleaned_koala_words = {}
        # print("started \n_____________")
        tmp = 0
        while len(l) != 0:
            l = str(l).replace('\'','')
            l = str(l).replace('[','')
            l = str(l).replace(']','')
            l = str(l).replace('\n','')        
            try:
                if tmp == 0:
                    tmp = 1
                    idd = int(l)
                else:
                    tmp = 0
                    cleaned_koala_words[idd] = l.split(',')
            except:
                    print("exception",l)
                    l = f.readline()
                    continue
            l = f.readline()
    return cleaned_koala_words

def train_word2vec(load_model,sentence_dic,window,min_count,size,vocab_size):
    '''
    Input: List of bag-of-word, hyperparamters (min_count, size,vocab_size) 
    Output: Trained model 
    '''
    vocab = []
    train = []
    tmp = 0 
    print("word2vec model train started")
    for i in sentence_dic:
        if tmp < vocab_size:
            vocab.append(sentence_dic[i])
        else:
            train.append(sentence_dic[i])
        tmp+=1
    model = gensim.models.Word2Vec(vocab,window=window, min_count=min_count, size=size)
    tmp = 0 
    for i in tqdm(train):
        tmp = tmp +1
        model.train([i],total_examples=1,epochs=1)
    print("train ended")
    model.save("./models/"+load_model)
    return model