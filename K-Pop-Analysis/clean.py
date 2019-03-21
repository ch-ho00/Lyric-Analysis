#-*- coding: utf-8 -*-
import codecs
from konlpy.tag import Kkma
from konlpy.utils import pprint

def to_sentence(dic):
    kkma = Kkma()
    sentence_dic = {}
    tmp_dic = []
    print("To sentence started")
    for i in dic:
        try:
          tmp_dic = kkma.sentences(dic[i])
          sentence_dic[i] = tmp_dic
        except:
          continue
    print("Number of lyrics processed : ",len(sentence_dic))
    return sentence_dic

def clean_file(train_file):
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
