import gensim.corpora as corpora
import gensim

def create_lda(num_topic, dictionary):
    corpus, dic = generate_corpus(dictionary)
    lda= gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topic, id2word=dic, passes=15)
    topics = lda.print_topics(num_words = 10)
    # see list of topics
    for topic in topics:
        print(topic)
    return lda

def generate_corpus(dictionary):
    # Create dictionary
    dic = corpora.Dictionary(dictionary)
    # Create bag of words
    corpus = [dic.doc2bow(text) for text in dictionary]
    return corpus, dic

def text2topic(ldamodel, text):
     ldamodel.get_document_topics(text)

def model_evaluate(lda_model, data_lemmatized, dictionary):
    # Compute Perplexity
    print('\nPerplexity: ', lda_model.log_perplexity(corpus))
    # a measure of how good the model is. lower the better.
    # Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)

def visualize(ldamodel, corpus, dictionary):
    pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    vis


'''
https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/
'''