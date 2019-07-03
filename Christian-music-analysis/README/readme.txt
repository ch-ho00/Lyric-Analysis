To run the files, one has to use docker for compatibility issues.
Steps are as follows:
	1. open git bash
	2. Move to the directory with main.py
	3. run command "docker build -t test ."
	4. run command "docker run test" (After this step the resultant files are stored in the docker image)
	5. docker ps -a ( will display Image_ID)
	6. docker start Image_ID
	7. docker cp Image_ID:/usr/src/app/results/lda_result.txt ./copied_result.txt (Retrieve LDA result)
	8. docker cp Image_ID:/usr/src/app/results/lda_topics.txt ./copied_topics.txt (Retrieve LDA topics)
	9. docker cp Image_ID:/usr/src/app/LDA_Visualization_2.html ./copied.html (Retrieve pyLDAvis result) (2 can be replaced with number of topics)

This sub-project consists of two parts:

	1. Web scrapping Christian music lyrics

	2. LDA topic modeling
    		- data preprocessing
        		- to sentence
        		- to word
        		- stemming
        		- stopwords removal
    		- LDA model
        		- model generation
        		- model visualisation
        		- model effectiveness metric (coherence score)
		- Result:
			- LDA model 
			- top words consisting each topic // number of top words can be modified at topic_model.py line 49 
			- coherence score
			- pyLDAvis html file
			
When one needs to change the data feeding in, change "lyric_list" of main.py into dictionaray of documents
then the process of stemming,stopword removal will automatically process followed by LDA topic modeling.
When size of corpus is large lemmatisation & stopword removal takes time.

## Remark

To make use of different topic modeling models, one can add this to line 38 of main.py
	hdpmodel = create_hdp(num_topic,lll)
	lsimodel = create_lsi(num_topic,lll)
However these models are relatively slow and inaccurate.