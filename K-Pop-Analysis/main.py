from topic_modelling import *
from clean import *
from train import *
from translate import *
num_topics = 5
train_file = "./data/test.txt"

#cleaning 
sentence_dic = clean_file(train_file)
# Instantiates a client
translate_client = translate.Client()
google_translate(sentence_dic,translate_client)
# dictionary,vocab = to_dictionary(sentence_dic, 0.9)
# print(vocab)
# # create model
# ldamodel = create_lda(num_topics, dictionary)
# model_evaluate(ldamodel,dictionary ,vocab)
# # evaluate model
# lda = text2topic(ldamodel, test_text)