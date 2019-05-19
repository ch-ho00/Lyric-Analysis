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
# def install_java():
#   #apt-get install -y openjdk-8-jdk-headless -qq > /dev/null  
#   os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"     #set environment variable

# install_java()

# initialize(java_options="-Xmx4g -Dfile.encoding=utf-8", KKMA="2.0.2",RHINO="2.0.5", EUNJEON="2.0.2", ETRI="2.0.2")

topics = [3,4,5]
train_file = "./data/test.txt"
kiwi = prepare_kiwi(train_file)
kkma = Kkma()

korean_song_id = pd.read_csv("./data/song_id.csv")
korean_song_id = korean_song_id['B_song_id'].tolist()
# #cleaning for normal
sentence_dic = to_sentence(clean_file(train_file, korean_song_id),kkma)
cleaned_kiwi_words = {}
# ____________________________________
# GENERATE KIWI BOW
#   - functions are in tagger.py
# for i in tqdm(sentence_dic):
#     if i in korean_song_id:
#         cleaned_kiwi_words[i]= kiwi_words(kiwi,i,sentence_dic[i])
#     else:
#         print("not there",i)
# dictionary,vocab = kiwi_dictionary(cleaned_kiwi_words, 1)
#______________________________

print(len(cleaned_kiwi_words), " number of songs processed")
# create model
for num_topic in topics:
    ldamodel,corpus,id2word = create_lda(num_topic, dictionary)
    # model_evaluate(ldamodel,dictionary,id2word,num_topic)
    lda_visualize(ldamodel,dictionary,num_topic)


# BELOW IS ATTEMPT TO TRANSLATE
# translate_client = translate.Client()
# google_translate(sentence_dic,translate_client)
