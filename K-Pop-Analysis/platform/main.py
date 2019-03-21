import gensim
from evaluate import *
from train import *
from clean import *
import codecs
from konlpy.tag import Kkma
from konlpy.utils import pprint
import os 


#Key for the model
key = "K-pop"
input_words = ["사랑", "이별", "시련",'고통', "슬픔"]     #Should be in a [] can be used as a list of words too 
num_close_word = 10
train_file = '../data/converted.txt'
kor_tag = "Okt"

#Set to true if loading model with hyper-parameters below
load_bool = True

#hyper-parameters for model
window = 3
min_count = 5
size = 100
vocab_size = 5000

load_model =  key+"_"+str(window)+"_"+ str(min_count)+"_"+str(size)

for model in (os.listdir('./models')):
    if(load_model == model and load_bool):
        loaded_model = gensim.models.Word2Vec.load('./models/'+load_model)
        load_result(loaded_model,load_model,input_words, num_close_word)
        exit()
print("No models found\nProceeding to training")
sentence_dic = to_sentence(clean_file(train_file))
train(load_model,sentence_dic,kor_tag,window,min_count,size, vocab_size)
result(load_model, input_words, num_close_word)
