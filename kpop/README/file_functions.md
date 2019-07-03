### train.py 
    
    def koala_bow():
        '''
        Input: koala_bow.txt (text file including pre-cleaned words) 
        Output: list of koala-cleaned bag-of-word
        '''

    def kiwi_bow():
        '''
        Input: kiwi_bow.txt (text file including pre-cleaned words) 
        Output: list of kiwi-cleaned bag-of-word
        '''

    def train_word2vec(load_model,sentence_dic,window,min_count,size,vocab_size):
        '''
        Input: List of bag-of-word, hyperparamters (min_count, size,vocab_size) 
        Output: Trained model 
        '''


### clean.py
    def clean_file(train_file,korean_song_id):
    '''
    Input: Raw text file 
    Output: dictionary of {songid: lyric}
    '''

    def to_sentence_hnn(dic,splitter):
    '''
    Input: dictionary of {songid: lyric}
    Output: dictionary of {songid: list of sentence} using hnn splitter
    '''

    def to_sentence(dic,kkma):
    '''
    Input: dictionary of {songid: lyric}
    Output: dictionary of {songid: list of sentence} using kkma splitter
    '''

    def imp_words(i, text,tag):
    '''
    input: text, tag 
    output: cleaned text using tag input
    '''

    def to_dictionary(sentence_dic, vocab_size):
    '''
    Input: dictionary of {songid: list of sentence} , proportion of initial vocabulary
    Output: dictionary[list of cleaned words], vocab [list of cleaned words]
    '''

### tagger.py
    tagging

    def prepare_kiwi(train_file):
    """
    input: train file i.e. corpora
    output: kiwi model
    """

    def kiwi_words(kiwi,i, text): 
    """
    input : sentence list, kiwi model
    output : stop_word removed bag-of-word in list
    """

    def split_train(imp_words,vocab_size):
    """
    input: 
    output: 
    """

    def koala_word(tagger,i, song):
    """
    input: list of sentences (represent one song per list)
    output: stopword removed bag-of-words list
    """

### topic_modeling.py

    def lda_visualize(ldamodel, dictionary, num_topic,name):
        '''
        Input: ldamodel,  dictionary, num_topic,model name
        Output: html file visualizing the model (Pyldavis)
        '''
    def create_lda(num_topic, dictionary):
        """
        input: dictionary of words, num_topic
        output: lda model with number of topic = num_topic 
        """
    def generate_corpus(dictionary):
        """
        input: list of bag of words
        output: id to word conversion dictionary, doc2bow format list of list of tuples 
        """
    def text2topic(ldamodel, text):
        """
        input: ldamodel,text
        output: print result of model 
        """
    def model_evaluate(lda_model,text,id2word,num_topics):
        """
        input: lda_model,text(BOW),id2word,num_topics 
        output: coherence score of model
        """

### evaluate.py

    def load_result(loaded_model,model_name,input_words, num_close_word):
        '''
        Input: loaded_model,model_name,input_words, num_close_word
        Output: file containing embedding result
        '''

    def doc2avgvec(word2vec_model,list_words):
        '''
        Input: embedding model, list of bag-of-words 
        Output: matrix which each column represents document embedding of one bag-of-word
        '''
    def analysis_result(avg_vector_lyric, songid):
        '''
        Input: one songID
        Output: three songIDs with highest cosine similarity with input songID
        '''
    def similar(vec1, vec2):
        '''
        Input: two document vectors
        Output: cosine similarity between vectors
        '''

    def similarity(s1,s2,docvec):
        '''
        Input: two songID
        Output: cosine similarity between songs
        '''
