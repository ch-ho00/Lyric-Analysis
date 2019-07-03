#-*- coding: utf-8 -*-
import codecs
from konlpy.utils import pprint
from tqdm import tqdm

def to_sentence(dic,kkma):
  '''
  Input: dictionary of {songid: lyric}
  Output: dictionary of {songid: list of sentence} using kkma splitter
  '''
  sentence_dic = {}
  tmp_dic = []
  print("To sentence started")
  
  for i in tqdm(dic):
      try:
        tmp_dic = kkma.sentences(dic[i])
        sentence_dic[i] = tmp_dic
      except:
        continue
  print("Number of lyrics processed : ",len(sentence_dic))
  return sentence_dic

def to_sentence_hnn(dic,splitter):
  '''
  Input: dictionary of {songid: lyric}
  Output: dictionary of {songid: list of sentence} using hnn splitter
  '''
  sentence_dic = {}
  tmp_dic = []
  print("To sentence started")
  
  for i in tqdm(dic):
      try:
        tmp_dic = splitter(dic[i])
        sentence_dic[i] = tmp_dic
      except:
        continue
  print("Number of lyrics processed : ",len(sentence_dic))
  return sentence_dic

def clean_file(train_file,korean_song_id):
  '''
  Input: Raw text file 
  Output: dictionary of {songid: lyric}
  '''
  f2 = codecs.open(train_file, 'r', encoding="utf-8")
  id = 0
  dic = {}
  lyric = ""
  print("Cleaning started")
  for line in f2:
    if(line.find('\n') != -1):
        line = line.replace('\n','')
    if(line.find('\t') != -1):
      line = line.replace('\t','')
    if(line.find('\r') != -1):
      line = line.replace('\r','')
    if(line.find("|////////") != -1):
      continue
    if(line.find('[') != -1):
      line = line[:line.find('[')] + line[line.find(']') + 1:]
    if(line.find('(') != -1):
      line = line[:line.find('(')] + line[line.find(')') + 1:]
    if(line.find(')') != -1):
      line = line[:line.find(')') -2] + line[line.find(')') + 1:]
    if(line.find(':') != -1):
      line = line[:line.find(':') -2]  +line[line.find(':') + 1:]
    if(line.find('※') != -1):
      line = line.replace('※','')
    if(line.find('*') != -1):
      line = line.replace('*','')
    elif(line.find('|') != -1):
      if(len(lyric) > 10):
        if id in korean_song_id:
          lyric = lyric[:-4]
          dic[id] = lyric
      str_id = line[4:11]
      while(True):
        try:
          id = int(str_id)
          break
        except:
          str_id = str_id.replace('/','')
          try:
            id = int(str_id)
            break
          except:break
      lyric = ""
      line = line[line.rfind('/') + 1:]
      lyric = lyric + line
    else:
      lyric = lyric + line
  return dic


def imp_words(i, text):
    '''
     input: text, tag 
     output: cleaned text using tag input
    '''
    okt = Okt()
    out_list = []
    okt_stop = ['Eomi','Punctuation','Unknown', 'Josa','PreEomi', 'Conjunction', 'Punctuation', 'KoreanParticle']
    #print("Filtering words")
    try:
        #print(text)
        for sentence in text:
            for l in okt.pos(sentence):
                try:
                    if(okt_stop.index(l[1]) != -1):
                        continue
                except:
                    if(len(l[0]) > 1):
                        out_list.append(l[0])
    except:
        with codecs.open('./models/error_id_list.txt','a',encoding="utf-8") as f:
            f.write(str(i))
            f.write('\n')
    return out_list

def to_dictionary(sentence_dic, vocab_size):
    '''
    Input: list of list of sentences , proportion of initial vocabulary
    Output: dictionary, vocab (both list of cleaned bag-of-words)
    '''
    tmp = 0
    vocab = []
    dic = []
    kor_tag = "okt"
    print("To dictionary Started")
    for i in tqdm(sentence_dic):
        tmp = tmp +1
        if(tmp < vocab_size * len(sentence_dic)):
            dic.append(imp_words(i,sentence_dic[i]))
        else:
            vocab.append(imp_words(i,sentence_dic[i]))
    return dic,vocab
