## The project consists of two parts.

### 1. Word/Document embedding using Gensim
    
####    	- Data Preprocessing 

		- clean.py  
        	- tagger.py 
    
####    	- Train Model

		- main_word2vec.py 
        	- topic_modeling.py 
        	- train.py 

#### 	- Check effectiveness 

		- main_pretrained.py 
        	- evaluate.py

### 	2. LDA topic modeling 
    	  
#### 	  - Data Preprocessing 
	   
        	- clean.py
        	- tagger.py
    
#### 	  - Train Model
        
		- main_kiwi.py 
        	- main_koala.py 
        	- topic_modeling.py 
        	- train.py 

#### 	  - Check effectiveness  
        	
		- main_kiwi.py 
        	- main_koala.py 
        	- evaluate.py

### To be more specific about the three process in each project,
####    1. Data Preprocessing 
        - consists of processing the raw text file into structured data, sentence, to words
	- removing stopwords
	- lemmatization (if english) 

####    2. Train 
        - word2vec model / LDA model

####    3. Check effectiveness
        LDA
        - visualisation
	- list of words for each topic 
	- coherence score 
        Word2Vec
        - close word print
        - similarity between songs (cosine similarity )
	- most closest song

#### Remark

- Coherence score of the models (effectiveness of model) built using kiwi cleaned words were ~0.42 

- More information about coherence scores of others & coherence metric (refer to http://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf)

- To check the description of files and main files, one can refer to README/file_functions.md and README/main_files.md respectively.

- File ko.bin, ko.tsv are the pretrained korean word2vec models (source: https://github.com/Kyubyong/wordvectors)

- So if the vectors a and b are centered (i.e. have zero means), then their cosine similarity will be the same as their correlation coefficient. Therefore it is plausible to calculate the cosine similarity of each document vector(BOW / average of word embeddings or etc). 

To run the files one has to use docker for compatibility issues.
Steps are as follows:

	1. open "git bash" Terminal

	2. Move to the directory with main_XXXX.py // use cd command | current list check = ls  C:\Users\Yonghoon LEE\Desktop\kpop
	
	3. run command "docker build -t test ." (Change dockerfile line 8 to change main file to be executed)
	
	4. run command "docker run test" (After this step results will be generated in docker image)
	
	5. docker ps -a ( will display Image_ID)
	
	6. docker start Image_ID
	
	7. docker cp Image_ID:/usr/src/app/results/result.txt ./copied_result.txt (Retrieve similarity result)
	
	(For main_word2vec.py) 8.docker cp Image_ID:/usr/src/app/models/model_name ./copied_model (Retrieved model generated) 

#### Remark
	Before step3 one should make change to file "Dockerfile" to run different main_XXX file.
	
	Change line8 of "Dockerfile" to desired main file to run.
