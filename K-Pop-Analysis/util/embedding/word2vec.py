#-*- coding: utf-8 -*-
from tqdm import tqdm
import codecs
from dask import delayed, compute
from dask.diagnostics import ProgressBar
from konlpy.tag import Kkma,Okt
from konlpy.utils import pprint
import gensim 

def to_word(sentence_dic):
  #returns list of list with elements of important words
  out = []
  for i in tqdm(dic):
    out.append(func(i,dic[i]))
  return out

def func(_i, text):
  kkma = Kkma()
  okt = Okt()
  imp_words = []
  okt_stop = ['Eomi','Punctuation','Unknown', 'Josa','PreEomi', 'Conjunction', 'Punctuation', 'KoreanParticle']
  tmp_dic = kkma.sentences(text)
  for sentence in tmp_dic:
   for i in okt.pos(sentence):
      try:
        if(okt_stop.index(i[1]) != -1):
          continue
      except:
          imp_words.append(i[0]) 
  return imp_words
  
def result(dic):
  tmp = 0
  first = []
  for i in tqdm(dic):
    tmp = tmp +1
    first.append(func(i,dic[i]))
    if(tmp == 5000):
      break

  t_window = [2,3,4]
  t_min_count = [2,3,4] 
  t_size = [100,150]
  tmp = 0
  for tt_window in t_window:
    for tt_min_count in t_min_count:
      for tt_size in t_size:
        filename = str(tt_window)+"-"+ str(tt_min_count)+"-"+str(tt_size) 
        model = gensim.models.Word2Vec(first,window=tt_window, min_count=tt_min_count, size=tt_size)
        for i in tqdm(dic):
            tmp = tmp +1
            if(tmp % 10000 == 0):
              model.save(filename)
            if(tmp < 5000):
              continue
            model.train([func(i, dic[i])],total_examples=1,epochs=1)
        model.save(filename)
