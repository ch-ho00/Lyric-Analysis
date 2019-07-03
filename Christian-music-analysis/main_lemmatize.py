#-*- coding: utf-8 -*-
import codecs
from scrape  import *
from topic_model import *

#load lyric list
save_dir = "./results/"
f2 = codecs.open('./results/lyric.txt', 'r', encoding="utf-8")
lyric_list = {}
lyric = ""
for line in f2:
  if line.find(':') != -1:
    lyric_list[line[:line.find(':')-1]] = line[line.find(':')+3:]

#lyric_list has to be in dictionary format when feeding in different data
dic_lyric ,lll = lemmatize(lyric_list,save_dir)
for sid in dic_lyric:
    with codecs.open('./results/lemma_lyrics.txt','a') as f:
        f.write(str(sid) + ' : ')
        f.write(str(dic_lyric[sid]))
        f.write('\r\n')

