import gensim
import codecs
import os
import pyLDAvis.gensim
from topic_modeling import *
from tqdm import tqdm
def similarity(s1,s2,docvec):
    n = similar(docvec[s1],docvec[s2])
    print("Similarity between song ", s1,"and ",s2,"are ", n)
    return n
def similar(vec1, vec2):
    out = 0
    i2 = 0
    j2 = 0
    for i,j in zip(vec1,vec2):
        out = out + i *j
        i2 = i2 + i**2
        j2 = j2 + j**2
    return out/ (i2 * j2)**0.5

def analysis_result(avg_vector_lyric, songid):
    top3 = []
    maxx = 0
    songvec = avg_vector_lyric[songid]
    print("Document evaluation started")

    for l in avg_vector_lyric:
        if l != songid and similar(songvec,avg_vector_lyric[l]) > maxx:
            top3.append(l)
            maxx =similar(songvec,avg_vector_lyric[l])
            print(maxx)
    print(top3[-3:], " are the most similar songs to ",songid)
    return top3            
def doc2avgvec(word2vec_model,list_words):
    out = {}
    avg = [0] * 200 
    tmp = 0 
    tmp2 = 0
    print("Document embedding started")
    for l in tqdm(list_words):
        for word in list_words[l]:
            tmp +=1
            try: 
                # print(word2vec_model.wv[word])
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
    print("Not in dictionary ==" ,tmp2)
    return out

def result(load_model, num_close_word):
    word_model = gensim.models.Word2Vec.load('./models/'+load_model)
    return word_model    

def load_result(loaded_model,load_model,input_words, num_close_word):
    print("Saving result ...")
    for word in input_words:
        with codecs.open('./result/'+load_model+'.txt','a',encoding="utf-8") as f:
            f.write("Word :"+word)
            f.write('\n')
            print(loaded_model.wv.most_similar (positive=word))
            f.write(str([loaded_model.wv.most_similar (positive=word)[i][0] for i in range((len(loaded_model.wv.most_similar (positive=word))))]))
            f.write('\n\n')

def lda_visualize(ldamodel, dictionary, num_topic,model):
    corpus, dic= generate_corpus(dictionary)
    # pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(ldamodel, corpus, dic)
    pyLDAvis.save_html(vis, './models/'+str(model)+'_LDA_Visualization_' +str(num_topic) + '.html')

