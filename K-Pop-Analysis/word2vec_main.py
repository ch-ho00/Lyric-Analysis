import gensim
from evaluate import *
from train import *
from clean import *
import codecs
from konlpy.tag import Kkma
from konlpy.utils import pprint
import os 
import pandas as pd

#hyper-parameters for model
window = 3
min_count = 5
size = 200
vocab_size = 40000

load_model =  "koala_word2vec"
song1 = 1000066
song2 = 1001965
sentence_dic = kiwi_bow()
# _____________________________________________________
# korean_song_id = pd.read_csv("./data/song_id.csv")
# korean_song_id = korean_song_id['B_song_id'].tolist()
# for i in korean_song_id:
#         try:
#                 sentence_dic[i]
#         except:
#                 print("Not in list", i)
#                 continue
#______________________________________________________
try:
        model = gensim.models.Word2Vec.load('./models/'+load_model)
except:
        print("Model doesnt exist training process start")
        train_word2vec(load_model,sentence_dic,window,min_count,size,vocab_size)
        model = result(load_model, num_close_word)
docvec =doc2avgvec(model,sentence_dic)
analysis_result(docvec,song1)
similarity(song1,song2)

# Pre-trained model

# for model in (os.listdir('./models')):
#     if load_model == model and load_bool:
#         loaded_model = gensim.models.Word2Vec.load('./models/'+load_model)
#         # functions are at evaluate.py
#         load_result(loaded_model,load_model,input_words, num_close_word)
#         avg_vector_lyric = doc2avgvec(loaded_model,cleaned_koala_words)
#         analysis_result(avg_vector_lyric, songid)
#         exit()
# print("No models found\nProceeding to training",len(cleaned_koala_words))
# sentence_dic = to_sentence(clean_file(train_file))