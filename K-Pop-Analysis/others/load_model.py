from topic_modeling import *
from clean import *
from train import *
from evaluate import *
from tagger import *
import os       #importing os to set environment variable
from konlpy.tag import Kkma
from tqdm import tqdm
import gensim
from gensim.test.utils import datapath

# dictionary = kiwi_bow()
# num_topics =[3,4,5]
# for num_topic in num_topics:
#     temp_file = datapath("kiwi_model_"+str(num_topic))
#     lda = gensim.models.ldamodel.LdaModel.load(temp_file)
#     topics = lda.print_topics(num_words = 10)
#     # see list of topics
#     for topic in topics:
#         print(topic)
#     print("___________________________________________________________")
#     # lda_visualize(lda,dictionary,num_topic,"kiwi")

    
dictionary = koala_bow()
num_topics =[3,4,5]
for num_topic in num_topics:
    temp_file = datapath("koala_model_"+str(num_topic))
    lda = gensim.models.ldamodel.LdaModel.load(temp_file)
    topics = lda.print_topics(num_words = 10)
    # see list of topics
    for topic in topics:
        print(topic)
    print("___________________________________________________________")
    # lda_visualize(lda,dictionary,num_topic,"kiwi")