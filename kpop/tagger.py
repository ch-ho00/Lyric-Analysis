#-*- coding: utf-8 -*-
from tqdm import tqdm
import codecs
from konlpy.tag import Kkma,Okt
from konlpy.utils import pprint
import gensim
from clean import *
from kiwipiepy import Kiwi
from train import *
# from koalanlp.Util import initialize
# from koalanlp.proc import *
# from koalanlp import API

class ReaderExam:
    def __init__(self, filePath):
        self.file = open(filePath)

    def read(self, id):
        if id == 0: self.file.seek(0)
        return self.file.readline()
def prepare_kiwi(train_file):
    """
    input: train file i.e. corpora
    output: kiwi model
    """
    numThread = 4
    kiwi = Kiwi(numThread)
    reader = ReaderExam(train_file)
    minCount = 5
    maxWordLength = 6
    minScore = 0.25
    kiwi.extractWords(reader.read, minCount, maxWordLength, minScore)
    kiwi.prepare()
    return kiwi

def kiwi_words(kiwi,i, text): 
    """
    input : sentence list, kiwi model
    output : stop_word removed bag-of-word in list
    """

    topN = 1
    # for u in kiwi.analyze(text, topN):
    #     print(u)
    #     print("_________________")
    
    out_list = []
    kiwi_find = ['NNG', 'MAG', 'VV','NP']
    kiwi_stop = ['Eomi','Punctuation','Unknown', 'Josa','PreEomi', 'Conjunction', 'Punctuation', 'KoreanParticle']
    tmp = 0
    for sentence in text:
        if len(sentence) > 2:
            for lll in kiwi.analyze(sentence, topN):
                for ll in lll: 
                    if tmp == 0:
                        for l in ll: 
                            try:
                                if kiwi_find.index(l[1]) != -1:
                                    if(len(l[0]) > 1):
                                        out_list.append(l[0])    
                            except:

                                continue
                        tmp += 1
                    else:
                        tmp =0
    # except:
    #     with codecs.open('./models/error_id_list.txt','a',encoding="utf-8") as f:
    #         f.write(str(i))
    #         f.write('\n')
    return out_list


def split_train(imp_words,vocab_size):
    """
    input: 
    output: 
    """
    vocab = []
    dic = []
    tmp = 0
    print("To dictionary Started")
    for i in tqdm(imp_words):
        tmp = tmp +1
        if(tmp < vocab_size * len(imp_words)):
            dic.append(imp_words[i])
        else:
            vocab.append(imp_words[i])
    return dic,vocab

def koala_word(tagger,i, song):
    """
    input: list of sentences (represent one song per list)
    output: stopword removed bag-of-words list
    """
    for s in song:
        sentences = tagger(song)
        out = []
        for sent in sentences:
            for word in sent:
                s = word.getSurface()
                if len(s) < 5 and len(s) > 1:
                    out.append(s)
                else:
                    # 안녕하/VV 시/EP 어요/EF 
                    for morph in word:
                        m = morph.getTag()
                        if 'V' in list(str(m)) or 'N' in list(str(m)):
                            ss = morph.getSurface()
                            # TODO
                            # run without this line of filtering one letter verb/nouns
                            if len(ss) > 1:
                                out.append(ss)
    return out