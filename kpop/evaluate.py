import gensim
import codecs
import os
from topic_modeling import *
from tqdm import tqdm

# C:\Program Files\Java\jdk1.7.0_79\bin
# C:\Program Files\Java\jdk1.7.0_79\jre\bin\server 
def similarity(s1,s2,docvec):
    '''
    Input: two songID
    Output: cosine similarity between songs
    '''
    n = similar(docvec[s1],docvec[s2])
    return str(s1)+","+str(s2)+","+str(n)
def similar(vec1, vec2):
    '''
    Input: two document vectors
    Output: cosine similarity between vectors
    '''
    out = 0
    i2 = 0
    j2 = 0
    for i,j in zip(vec1,vec2):
        out = out + i *j
        i2 = i2 + i**2
        j2 = j2 + j**2
    if i2 * j2 != 0:
        return out/ (i2 * j2)**0.5
    else:
        return 0.3

def analysis_result(avg_vector_lyric, songid):
    '''
    Input: one songID
    Output: three songIDs with highest cosine similarity with input songID
    '''
    top3 = []
    maxx = 0
    songvec = avg_vector_lyric[songid]
    print("Document evaluation started")

    for l in avg_vector_lyric:
        if l != songid and similar(songvec,avg_vector_lyric[l]) > maxx:
            top3.append(l)
            maxx =similar(songvec,avg_vector_lyric[l])
            # print(maxx)
    print(top3[-3:], " are the most similar songs to ",songid)
    return top3            
def doc2avgvec(word2vec_model,list_words):
    '''
    Input: embedding model, list of bag-of-words 
    Output: matrix which each column represents document embedding of one bag-of-word
    '''
    out = {}
    avg = [0] * 200 
    tmp = 0 
    tmp2 = 0
    # print("Document embedding started")
    for l in tqdm(list_words):
        for word in list_words[l]:
            tmp +=1
            try: 
                # print(word,word2vec_model.wv[word])
                avg = [i + j for i,j in zip(avg,word2vec_model.wv[word])]
                tmp+=1
            except:
                # print("Not in Dictionary", word)
                tmp2 +=1

                continue
        avg = [i/tmp for i in avg]
        out[l] = avg
        avg = [0] * 200 
        tmp = 0
    # print("Not in dictionary ==" ,tmp2)
    return out

def load_result(loaded_model,model_name,input_words, num_close_word):
    '''
    Input: loaded_model,model_name,input_words, num_close_word
    Output: file containing embedding result
    '''
    for word in input_words:
        print(loaded_model.wv.most_similar (positive=word))
