import gensim
import codecs
import os

def result(load_model, input_words, num_close_word):
    word_model = gensim.models.Word2Vec.load('./models/'+load_model)
    print("Saving result ...")
    for word in input_words:
        with codecs.open('./result/'+load_model+'.txt','a',encoding="utf-8") as f:
            f.write("Word :"+word)
            f.write('\n')
            print(word_model.wv.most_similar (positive=word))
            f.write(str([word_model.wv.most_similar (positive=word)[i][0] for i in range((len(word_model.wv.most_similar (positive=word))))]))
            f.write('\n\n')

def load_result(loaded_model,load_model,input_words, num_close_word):
    print("Saving result ...")
    for word in input_words:
        with codecs.open('./result/'+load_model+'.txt','a',encoding="utf-8") as f:
            f.write("Word :"+word)
            f.write('\n')
            print(loaded_model.wv.most_similar (positive=word))
            f.write(str([loaded_model.wv.most_similar (positive=word)[i][0] for i in range((len(loaded_model.wv.most_similar (positive=word))))]))
            f.write('\n\n')
