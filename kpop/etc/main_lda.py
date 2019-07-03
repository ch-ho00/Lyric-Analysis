from topic_modeling import *
from clean import *
from train import *
from evaluate import *
from tagger import *
from koalanlp.Util import initialize
from koalanlp.proc import *
from koalanlp import API
import os       #importing os to set environment variable
from konlpy.tag import Kkma
import pandas as pd
from tqdm import tqdm
import gensim
from gensim.test.utils import datapath

def install_java():
  #apt-get install -y openjdk-8-jdk-headless -qq > /dev/null  
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"     #set environment variable

install_java()
# 초기화 합니다.
# initialize(java_options="-Xmx4g -Dfile.encoding=utf-8", KKMA="2.0.2", EUNJEON="2.0.0", RHINO="2.0.5")
# tagger = Tagger(API.RHINO)
topics = [4,5]
train_file = "./data/test.txt"
korean_song_id = pd.read_csv("./data/song_id.csv")
korean_song_id = korean_song_id['B_song_id'].tolist()
kiwi = prepare_kiwi(train_file)

kkma = Kkma()
# #cleaning for sentence_dic
f = open("./data/KPOP_sentence_dic.txt")
l = f.readline()
sentence_dic = {}
print("started _____________")
while len(l) != 0:
  try:
    if len(l) > 3 and len(l) < 9:
        idd = int(l)
    elif len(l) == 2:
      sentence_dic[idd] = sents.split(',')
    else:
      sents = l
  except:
    l = f.readline()
    continue
  l = f.readline()
print("checking in list \n _____________")
cleaned_kiwi_words = {}
for i in tqdm(sentence_dic):
    if i in korean_song_id:
        cleaned_kiwi_words[i]= kiwi_words(kiwi,i,sentence_dic[i])
    else:
        print("not there",i)
with codecs.open("./data/cleaned/kiwi_bow.txt", 'w', encoding='utf8') as f:
  for i in cleaned_kiwi_words:
      f.write(str(i))
      f.write('\n')
      f.write(str(cleaned_kiwi_words[i]))
      f.write('\n')
dictionary,vocab = split_train(cleaned_kiwi_words, 1)

for num_topic in topics:
    ldamodel,corpus,id2word = create_lda(num_topic, dictionary)
    # Save model to disk.
    temp_file = datapath("kiwi_model_"+str(num_topic))
    ldamodel.save(temp_file)

#  model_evaluate(ldamodel,dictionary,id2word,num_topic)
# lda_visualize(ldamodel,dictionary,num_topic)

# cleaned_koala_words = {}
# added = []
# print(sentence_dic)
# for i in tqdm(sentence_dic):
#     if i in korean_song_id:
#         cleaned_koala_words[i]= koala_word(tagger,i,sentence_dic[i])
#         added.append(i)

# dictionary,vocab = split_train(cleaned_koala_words, 1)
# print(len(cleaned_koala_words), " number of songs in the csv file")


