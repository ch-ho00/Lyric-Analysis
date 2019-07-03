import sys
sys.path.append("..") # Adds higher directory to python modules path.
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
from koalanlp import API
from gensim.test.utils import datapath
import gensim

def install_java():
  #apt-get install -y openjdk-8-jdk-headless -qq > /dev/null  
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"     #set environment variable

install_java()
initialize(java_options="-Xmx4g -Dfile.encoding=utf-8", KKMA="2.0.2",RHINO="2.0.5", EUNJEON="2.0.2", ETRI="2.0.2")

def line():
  print("\n________________________\n\n")

print("Saving cleaned words complete")
cleaned_koala_words = koala_bow()
topics = [3,4,5]
dictionary,vocab = split_train(cleaned_koala_words, 1)
# create model
print("Generating and saving LDA models")
for num_topic in topics:
    line()
    ldamodel,corpus,id2word = create_lda(num_topic, dictionary)
    line()
    temp_file = datapath("../models/koala_model_"+str(num_topic))
    ldamodel.save(temp_file)
    line()
    model_evaluate(ldamodel,dictionary,id2word,num_topic)
    line()
    lda_visualize(ldamodel,dictionary,num_topic,"koala")
    line()

