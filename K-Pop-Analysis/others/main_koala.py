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
from koalanlp import API
from gensim.test.utils import datapath
import gensim


def install_java():
  #apt-get install -y openjdk-8-jdk-headless -qq > /dev/null  
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"     #set environment variable

install_java()

initialize(java_options="-Xmx4g -Dfile.encoding=utf-8", KKMA="2.0.2",RHINO="2.0.5", EUNJEON="2.0.2", ETRI="2.0.2")

topics = [3,4,5]
train_file = "./data/test.txt"
tagger = Tagger(API.RHINO)
# ____________________________________
# GENERATE KOALA BOW
#   - functions are in tagger.py
# for i in tqdm(sentence_dic):
#         tmp +=1
#         if tmp == 5000:
#                 with codecs.open("./data/cleaned/koala_bow.txt", 'w', encoding='utf8') as f:
#                         for i in cleaned_koala_words:
#                                 f.write(str(i))
#                                 f.write('\n')
#                                 f.write(str(cleaned_koala_words[i]))
#                                 f.write('\n')
#                 break
#         cleaned_koala_words[i]= koala_word(tagger,i,sentence_dic[i])
#         # print(cleaned_koala_words[i])
#         added.append(i)
#__________________________________________

f = open("./data/cleaned/koala_bow.txt")
l = f.readline()
cleaned_koala_words = {}
print("started \n_____________")
while len(l) != 0:
  try:
    if len(l) > 3 and len(l) < 9:
        idd = int(l)
    else:
        l = str(l).replace('\'','')
        l = str(l).replace('[','')
        l = str(l).replace(']','')
        l = str(l).replace('\n','')
        cleaned_koala_words[idd] = l.split(',')
  except:
        print("exception",idd,l)
        l = f.readline()
        continue
  l = f.readline()

print("Saving cleaned words complete")
dictionary,vocab = todictionary(cleaned_koala_words, 1)
# create model
print("Generating and saving LDA models")
for num_topic in topics:
    ldamodel,corpus,id2word = create_lda(num_topic, dictionary)
    temp_file = datapath("koala_model_"+str(num_topic))
    ldamodel.save(temp_file)
#     model_evaluate(ldamodel,dictionary,id2word,num_topic)

#     lda_visualize(ldamodel,dictionary,num_topic)


# BELOW IS ATTEMPT TO TRANSLATE
# translate_client = translate.Client()
# google_translate(sentence_dic,translate_client)
