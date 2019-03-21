# Scrape and Analyze Contemporary Christian music

Research Question: Through the analysis of LDA model trained by Christian Music lyrics, how have topics/words of Christian music changed over time? 

Jesusfreakhideout.com™ is one of the world's largest Christian music online resources. Created in August of 1996 as what originated as a small webpage titled "The Jesus Freak Hideout," the site was the flourishing creation of music fan and graphic designer John DiBiase. In August of 1998, the site blossomed into Jesusfreakhideout.com, bearing a big vision for spreading faith-based music across the globe via the web.

https://www.jesusfreakhideout.com

<img src="https://github.com/chanhopark00/ccm_scrape/blob/master/image/site.png" width="600" >

Through BeautifulSoup, 20335 lemmatized songs along with the artist and year of songs are saved. 

## Work Flow
1. Collect song lyircs into structured data
2. Removing stopword, stemming and cleaning lyric
3. Create dictionary, corpora
4. Generate LDA model
5. Evaluate

## Choice of LDA Model

A topic in LDA is a multinomial distribution over the (typically thousands of) terms in the vocabulary of the corpus.
Propose ranking terms for a given topic in terms of both the frequency of the term under that topic as well as the term’s exclusivity to the topic.

Therefore a change in the distribution/composition of topics for texts from different timelines, is sufficient to claim that 
there has been a major change in frequency of containing certain words over time. 

## Library used
1. Gensim: LDA topic modelling
2. Beautifulsoup: Web Scraping
3. pyLDAvis: LDA topic modelling visualisation
4. nltk : Text preprocessing

## Result and Evaluate

Out of multiple models through the optimisation of hyperparameters, including the number of topics, relavance metric, alpha and beta, the following is the model generated with the highest interpretability; the parameters are 
    
   number of topics = 3
   
   relavence metric = 0.6
   
   alpha (LDA model parameter) = auto
   
<img src="https://github.com/chanhopark00/ccm_scrape/blob/master/image/3_topic1.png" width="400" >

Topic 1 

<img src="https://github.com/chanhopark00/ccm_scrape/blob/master/image/3_topic2.png" width="400" >

Topic 2

<img src="https://github.com/chanhopark00/ccm_scrape/blob/master/image/3_topic3.png" width="400" >

Topic 3


Setting  = 1 results in the familiar ranking of terms in decreasing order of their topic-specific probability, and
setting  = 0 ranks terms solely by their lift. Lift is a measure of the performance of a targeting model (association rule) at predicting or classifying cases as having an enhanced response (with respect to the population as a whole), measured against a random choice targeting model. Basically, the relavence metric controls the flexibility.

A low alpha value places more weight on having each document composed of only a few dominant topics (whereas a high value will return many more relatively dominant topics). 

In order to evaluate the effectiveness of the model, I have incorporated different metrics and modes.
The 4 methods are by comparing with different topic modelling model, analyzing unseen text, visualising model and checking the coherence score.

### Comparison between different models (HDP, LSI)

<img src="https://github.com/chanhopark00/ccm_scrape/blob/master/image/hdp1.png" width="900" >
<img src="https://github.com/chanhopark00/ccm_scrape/blob/master/image/hdp2.png" width="900" >

We can notice the HDP and LSI model contains same words appearing across more than one topics. Therefore the interpretability makes the models inapt for analysis


### Analysis of unseen text


https://github.com/chanhopark00/ccm_scrape/blob/master/image/song1.png" 


https://github.com/chanhopark00/ccm_scrape/blob/master/image/song2.png" 


https://github.com/chanhopark00/ccm_scrape/blob/master/image/song3.png" 


https://github.com/chanhopark00/ccm_scrape/blob/master/image/song4.png" 

<Song 1,2,3,4>

The following is the result.

https://github.com/chanhopark00/ccm_scrape/blob/master/image/unseen_text.txt" 

I have made this part concise because it involves subjectivity while analysis. 
From this perspective, I personally believe that the parameters are set most reasonably when number of topic is two.

### LDA Visualisation

With the help of pyLDAvis library we are able to 

<img src="https://github.com/chanhopark00/ccm_scrape/blob/master/image/visualisation.png" width="800" >

A pair of overlaid bars represent both the corpus-wide frequency of a given term as well as the topic-specific frequency of the term


#### LDA Coherence score


<img src="https://github.com/chanhopark00/ccm_scrape/blob/master/image/coherence_plot.png" width="600" >

The coherence score is for assessing the quality of the learned topics.

For one topic, the words 𝑖,𝑗 being scored in ∑𝑖<𝑗Score(𝑤𝑖,𝑤𝑗) have the highest probability of occurring for that topic. You need to specify how many words in the topic to consider for the overall score.

From the graph plotted we can see that the coherence score is highest when the number of topics are around three or four.
