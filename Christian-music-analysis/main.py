#-*- coding: utf-8 -*-
import codecs
from scrape  import *
from topic_model import *
save_dir = "./results"
num_topics = [2,3,4,5,6]
song_ids = [12523,12524,12527]

dic_lyric = {}
lll = []
with codecs.open('./results/lemma_lyrics.txt','r') as f:
        l = f.readline()
        while len(l) != 0:
          l = l.replace('[','')
          l = l.replace(']','')
          l = l.replace('\'','')
          l = l.replace('\n','')
          idd = int(l[:l.find(':')].lstrip())
          dic_lyric[idd] = l[l.find(':'):].split(',')
          lll.append(dic_lyric[idd])
          l = f.readline()

#Check unseen text in dictionary format 
test_texts = []
coherence_score = []

for song_id in song_ids:
  test_texts.append(dic_lyric[song_id]) 
for num_topic in num_topics:
    lda, dic = create_lda(num_topic,lll)
    for text,text_id in zip(test_texts,song_ids):
        bow_text = [dic.doc2bow(text)]
        text2topic(lda ,bow_text,text_id)
    # When need to check perplexity and coherence score of model
    # coherence_score.append(evaluate(lda,lll))
    lda_visualize(lda, lll, num_topic)

