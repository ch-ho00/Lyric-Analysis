import sys
sys.path.append("..") # Adds higher directory to python modules path.
from topic_modeling import *
from clean import *
from train import *
from evaluate import *
from tagger import *
# from koalanlp.Util import initialize
import os       #importing os to set environment variable
from konlpy.tag import Kkma
import pandas as pd

def install_java():
  #apt-get install -y openjdk-8-jdk-headless -qq > /dev/null  
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"     #set environment variable
install_java()
initialize(java_options="-Xmx4g -Dfile.encoding=utf-8", KKMA="2.0.2",RHINO="2.0.5", EUNJEON="2.0.2", ETRI="2.0.2")

topics = [3,4,5]
train_file = "./data/test.txt"
kiwi = prepare_kiwi(train_file)
kkma = Kkma()
# #cleaning for normal
sentence_dic = to_sentence(clean_file(train_file, korean_song_id),kkma)
cleaned_kiwi_words = {}

print(len(cleaned_kiwi_words), " number of songs processed")
# create model
for num_topic in topics:
    ldamodel,corpus,id2word = create_lda(num_topic, dictionary)
    lda_visualize(ldamodel,dictionary,num_topic)
    # model_evaluate(ldamodel,dictionary,id2word,num_topic)


