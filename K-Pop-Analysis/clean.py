#-*- coding: utf-8 -*-
import codecs
from konlpy.utils import pprint
from tqdm import tqdm

def kiwi_bow():
    f = open("./data/cleaned/kiwi_bow.txt")
    l = f.readline()
    cleaned_kiwi_words = {}
    print("started \n_____________")
    tmp = 0
    while len(l) != 0:
        l = str(l).replace('\'','')
        l = str(l).replace('[','')
        l = str(l).replace(']','')
        l = str(l).replace('\n','')
        try:
            if tmp == 0:
                idd = int(l)
                tmp = 1
            else:
                tmp = 0
                cleaned_kiwi_words[idd] = l.split(',')
        except:
                print("exception",idd,l)
                l = f.readline()
                continue
        l = f.readline()
    return cleaned_kiwi_words


def koala_bow():
    f = open("./data/cleaned/koala_bow.txt")
    l = f.readline()
    cleaned_koala_words = {}
    print("started \n_____________")
    tmp = 0
    while len(l) != 0:
        l = str(l).replace('\'','')
        l = str(l).replace('[','')
        l = str(l).replace(']','')
        l = str(l).replace('\n','')        
        try:
            if tmp == 0:
                tmp = 1
                idd = int(l)
            else:
                tmp = 0
                cleaned_koala_words[idd] = l.split(',')
        except:
                print("exception",l)
                l = f.readline()
                continue
        l = f.readline()
    return cleaned_koala_words


def to_sentence(dic,kkma):
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

def kiwi_clean(kiwi_dir):
    f2 = codecs.open(kiwi_dir, encoding="utf-8")
    imp_word = {}
    song_word = []
    for line in f2:
        try:
            line.index('/')
            tmp = 0
            tmp2 = 0
            while line.index('/',tmp) != -1:
                try:
                    tmp = line.index('/',tmp+1)
                    if line[0] == '/' and len(song_word)==0:
                        idd = int(line[9:line.index('/',9)])
                        imp_word['dummy'] = [0]
                    elif line[0]=='/':
                        imp_word[idd] = song_word
                        idd = int(line[5:line.index('/',5)])
                        song_word = []
                        break
                    if tmp2 ==0:
                        # check tagger 
                        if str(line[tmp+1:tmp+4]).replace(' ','') == "NNG" or str(line[tmp+1:tmp+4]).replace(' ','') == "VV" or str(line[tmp+1:tmp+4]).replace(' ','') == "MAG" or str(line[tmp+1:tmp+4]).replace(' ','') == "VA" or str(line[tmp+1:tmp+4]).replace(' ','') == "VX":
                            # length of word minimum 2
                            if len(line[tmp2:tmp]) > 1:
                                song_word.append(str(line[tmp2:tmp]).replace(' ',''))
                    else:
                        if str(line[tmp+1:tmp+4]).replace(' ','') == "NNG" or str(line[tmp+1:tmp+4]).replace(' ','') == "VV" or str(line[tmp+1:tmp+4]).replace(' ','') == "MAG" or str(line[tmp+1:tmp+4]).replace(' ','') == "VA" or str(line[tmp+1:tmp+4]).replace(' ','') == "VX":
                            if len(line[tmp2+2:tmp]) > 1:
                                song_word.append(line[tmp2+2:tmp])
                    tmp2 = line.index('+',tmp2+1)
                except: 
                    break
        except:
            continue
    del imp_word['dummy']
    return imp_word

