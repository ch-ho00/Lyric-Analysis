The purpose of this tool is to navigate the closeness of words trained with K-pop lyrics. 

1. Search Close Words
    Input parameter: 
        1. Word to be searched.
        2. Number of close words required
        3. Directory of train file (must be stored in data folder)
        4. Option of train / load model
        5. Type of Korean tagger
    ## Below is Model's hyper-parameter 
        6. Window size: The number of neighbor words to be considered to give 'context' of a particular word while training. 
        7. min_count: Minimum number of occurance of a word to be in the dictionary
        8. size : Dimension of the embedding vector
        9. vocab_size: Number of lyrics to be considered while constructing the initial dictionary
    Output:
        Text file including the result. 
            Result will be saved in result folder
            File will be stored with key and hyper-parameter setting.
            Models will be saved in models folder in order for later load purpose.

    How: 
        Input parameters in main.py
        creates / loads a model
            create: 
                files in data will be used as train data 
                train.py will train and save model
            load:
                train.py will load model
        evaluate.py will include functions to generate result
        
