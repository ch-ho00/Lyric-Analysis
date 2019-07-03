### There are 4 different main files in this directory.
    1. main_kiwi.py
    2. main_koala.py
    3. main_pretrained.py
    4. main_word2vec.py

### The functionalities of each main file is as such:
    1. main_kiwi.py
        This file makes use of pretrained kiwi-cleaned bow to generate LDA model in model folder. 
        Result:
            LDA model trained with kiwi cleaned words
            coherence score
            list of words representing topic 
        Rmk. 1. If one replaces cleaned_koala_words into any cleaned list of bag-of-words it will generate pyLDAvis visualisation HTML, topic results and coherence score.   
             2. visualisation tool takes long when dictionary is large
	     3. koala, kiwi Morpheme analyzer both require JDK environment issues to be resolved
    2. main_koala.py
        Same functionalities as main_kiwi.py with different Morpheme analyzer 
        
    3. main_pretrained.py
        This file makes use of a pretrained korean embedding model.
        - Result:
            - Compares similarity between 'song1' and 'song2'
            - Returns three most similar songs of 'songid'
            - Analysis of 'songid' 
        - Remark
        	uncommenting line 65 of evaluate.py we can see the vectors of each word.
            changing line 18 of main_pretrained.py's "ko.bin" into other pretrained model, it will work 
        if one changes "cleaned_koala_words" into list of bag-of-words then the code will replicate the same process
        - Improvements
            if one uncomments line 69 of evaluate.py we can see that there are alot of words that are not in the dictionary of the pretrained model. 
         
    4. main_word2vec.py        
        This file generates a word2vec embedding model.
        The train data is setted to be the cleaned bag-of-words using kiwi Morpheme analyzer
        One can train different types of model by changing variable "sentence_dic" to list of bag-of-words
        - Parameters:
            size : dimension of embedded vector
            window : number of near words to be considered
            min_count: minumum number of occurance of a word to be considered 
            vocab_size: number of vocabulary in the dictionary of model
        - Result:
           - result is same as main_pretrained.py with the trained model
           - trained model is saved as "name(variable)".bin
	- Remark:
	   - if one changes "cleaned_koala_words" into list of bag-of-words then the code will replicate the same process
