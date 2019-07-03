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
songlist = [1001965,1000066]

songid = 1001965
cleaned_koala_words = kiwi_bow()
input_words = [] 
num_close_word = 4
for model in (os.listdir('.')):
    if "ko.bin" == model: 
        loaded_model = gensim.models.Word2Vec.load('./ko.bin')
        # functions are at evaluate.py
        # load_result(loaded_model,model_name,input_words, num_close_word)
        avg_vector_lyric = doc2avgvec(loaded_model,cleaned_koala_words)
        for s in songlist :
            for s2 in songlist:
                with codecs.open('./results/result.txt', 'w') as f:
                    f.write(similarity(s,s2, avg_vector_lyric))
                    f.write('\r\n')