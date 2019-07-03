import sys
sys.path.append("..") # Adds higher directory to python modules path.
import gensim
from evaluate import *
from train import *
from clean import *
import codecs
from konlpy.tag import Kkma
from konlpy.utils import pprint
import os 

#hyper-parameters for model
window = 3
min_count = 5
size = 200
vocab_size = 40000

model_name =  "koala_word2lvec"
songlist = [1001965,1000066]
sentence_dic = kiwi_bow()
try:
        # load existing model
        model = gensim.models.Word2Vec.load('./models/'+name)
except:
        print("Model doesnt exist training process start")
        # File is generated
        model= train_word2vec(model_name,sentence_dic,window,min_count,size,vocab_size)
docvec =doc2avgvec(model,sentence_dic)
for s in songlist :
        for s2 in songlist:
                with codecs.open('./results/result.txt', 'a') as f:
                        f.write(similarity(s,s2, docvec))
                        f.write('\r\n')