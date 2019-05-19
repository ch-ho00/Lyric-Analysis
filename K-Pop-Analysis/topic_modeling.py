import gensim.corpora as corpora
import gensim
from gensim.models import CoherenceModel


def create_lda(num_topic, dictionary):
    corpus, id2word = generate_corpus(dictionary)
    lda= gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topic, id2word=id2word)
    topics = lda.print_topics(num_words = 10)
    # see list of topics
    for topic in topics:
        print(topic)
    return lda, corpus, id2word

def generate_corpus(dictionary):
    # Create dictionary
    id2word = corpora.Dictionary(dictionary)
    # Create bag of words
    corpus = [id2word.doc2bow(text) for text in dictionary]
    #[[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]
    return corpus, id2word

def text2topic(ldamodel, text):
     ldamodel.get_document_topics(text)

def model_evaluate(lda_model,text,id2word,num_topics):
    coherencemodel = CoherenceModel(model=lda_model, texts=text, dictionary=id2word, coherence='c_v')
    print("Coherence score:",coherencemodel.get_coherence())
    # top_topics = lda_model.top_topics(corpus)
    # # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    # avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
    # print('Average topic coherence: %.4f.' % avg_topic_coherence)

def visualize(ldamodel, corpus, dictionary):
    pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    vis


'''
https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/
'''