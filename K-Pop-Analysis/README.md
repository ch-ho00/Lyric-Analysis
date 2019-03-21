# K-Pop-Analysis
  Research Question: What is the correlation between the 'creativity' of song lyric and popularity of a K-pop song? If not what are the factors that affect the success of a song?  
  
The process of korean language data processing is not satisfactory; the word/sentence split and the morphological analysis is not upto the standard yet. Therefore this issue is in the process of resolving. 

Still, the plan of the project is as follows. 

## Project Work Flow 
  1. Data Crawling
  
  2. Data Proecessing and cleaning
  
      2.1 morphological analysis
      
      2.2 stop word removal
  
  3. Embedding
      
      3.1 Word Embedding
   
        3.1.1 Comparison of different taggers 
      
      3.2 Document Embedding
    
  4. Correlation Analysis 
  5. Result and Implication 

###  Libraries included
  1. Gensim/word2vec: Gensim is a robust open-source vector space modeling and topic modeling toolkit implemented in Python.
  2. Beautifulsoup :Beautiful Soup is a Python package for parsing HTML and XML documents. 
  3. Konlpy : Konlpy is a Python package for natural language processing (NLP) of the Korean language.
  4. Codecs : A codec is a device or computer program for encoding or decoding a digital data stream or signal.
  5. Gensim/LDA: LDA is used to create an embedding for texts. 

## Details of Project

### 1. Data Crawling
Description of each files are as follows: 
  1) GetAlbumList.py: Crawls the album list and ID of each song 
  2) GetAlbumInfo.py: Crawls the album/ artist information 
  3) downloadSong.py: Downloads the preview songs inside MSSQL
  4) DB.py: Setting regarding the MSSQL database
  5) chart.py: Downloads the chart information from site
 
### 2. Data Proecessing and cleaning
   
   Eventually the final dictionary of words that are being fed into the word2vec model is as follows: 
   
### 3. Embedding
   ### 3.1 Word Embedding

   #### 3.1.1 Comparison of different taggers 
       
   Loading time: Class loading time, including dictionary loads.
    Kkma: 5.6988 secs
    Komoran: 5.4866 secs
    Hannanum: 0.6591 secs
    Twitter: 1.4870 secs
    Mecab: 0.0007 secs
        
  Execution time: Time for executing the pos method for each class, with 100K characters.
    Kkma: 35.7163 secs
    Komoran: 25.6008 secs
    Hannanum: 8.8251 secs
    Twitter: 2.4714 secs
    Mecab: 0.2838 secs
        
   ### 3.1.2 Hyperparameter optimisation
   Hyper Parameter type 
    1. window size: The number of neighbor words to be considered to give 'context' of a particular word while training. 
    2. min_count: The minimum number of occurance of a word to be added to the dictionary . 
    3. size: The dimension of vector that represents the word.
   In order to find the most accurate form, we have tried 20 different type of parameter setting. 
   
   #### Result using parameter 2,2,100
   <img src="https://github.com/chanhopark00/K-Pop-Analysis/blob/master/image/2-2-100.PNG" width="400" >
   
   #### Result using parameter 2,3,100
   <img src="https://github.com/chanhopark00/K-Pop-Analysis/blob/master/image/2-3-100.PNG" width="400" >
   
   #### Result using parameter 2,4,150
   <img src="https://github.com/chanhopark00/K-Pop-Analysis/blob/master/image/2-4-150.PNG" width="400" >
   
   ### 3.1.3 Accuracy Analysis
Based on the results produced by multiple taggers and multiple hyper-parameter, we were able to find out the most accurate model was as follows:
    OKT tagger and the hyper-parameter of window_size=2, min_count=4 and size=150.

  ### 3.2 Visualisation of embedding
  
   ### 3.2 Document Embedding
   
   Implementation of this embedding is done through the help of Gensim's LDA and doc2vec model. 
   
   #### 3.2.1 Hyperparameter optimisation
   We have tried training the model with different values of the parameter. 
   
   List of parameters are as such:
      size: Dimension of the embedding vector
      alpha: Learning rate of the model
      min_alpha: Learning rate alpha changes over iteration
      min_count: Minimum number of occurance of a word to be in the dictionary 
      dm: Defines the training algorithm. If dm=1, ‘distributed memory’ (PV-DM) is used
        
   ####   3.2.2 Accuracy Analysis
  
###  4. Correlation Analysis 
  
###  5. Result and Implication 
  
