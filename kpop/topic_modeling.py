import gensim.corpora as corpora
import gensim
from gensim.models import CoherenceModel
import pyLDAvis.gensim



def create_lda(num_topic, dictionary):
    """
    input: dictionary of words, num_topic
    output: lda model with number of topic = num_topic 
    """
    corpus, id2word = generate_corpus(dictionary)
    lda= gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topic, id2word=id2word)
    topics = lda.print_topics(num_words = 10)
    # see list of topics
    for topic in topics:
        print(topic)
    return lda, corpus, id2word

def generate_corpus(dictionary):
    """
    input: list of bag of words
    output: id to word conversion dictionary, doc2bow format list of list of tuples 
    """
    # Create dictionary
    id2word = corpora.Dictionary(dictionary)
    # Create bag of words
    corpus = [id2word.doc2bow(text) for text in dictionary]
    #[[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]
    return corpus, id2word

def text2topic(ldamodel, text):
    """
    input: ldamodel,text
    output: print result of model 
    """
    ldamodel.get_document_topics(text)

def model_evaluate(lda_model,text,id2word,num_topics):
    """
    input: lda_model,text(BOW),id2word,num_topics 
    output: coherence score of model
    """
    coherencemodel = CoherenceModel(model=lda_model, texts=text, dictionary=id2word, coherence='c_v')
    print("Coherence score:",coherencemodel.get_coherence())
    # top_topics = lda_model.top_topics(corpus)
    # # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    # avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
    # print('Average topic coherence: %.4f.' % avg_topic_coherence)

def lda_visualize(ldamodel, dictionary, num_topic,name):
    '''
    Input: ldamodel,  dictionary, num_topic,model name
    Output: html file visualizing the model (Pyldavis)
    '''
    corpus, dic= generate_corpus(dictionary)
    # pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(ldamodel, corpus, dic)
    pyLDAvis.save_html(vis, './models/'+str(model)+'_LDA_Visualization_' +str(num_topic) + '.html')

