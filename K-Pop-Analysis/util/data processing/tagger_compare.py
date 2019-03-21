from konlpy.tag import Hannanum,Mecab,Komoran,Okt,Kkma
from google.colab import files
hannanum = Hannanum()
komoran = Komoran()
# mecab = Mecab()
okt = Okt()
kkma = Kkma()
words = []
imp_words = []
tmp = 0 
tmpstr = ""
filename = ""

#stop POS taggers
hannanum_stop = ['JC', 'JX', 'JP','EP','EF', 'EC','ET','XS', 'NB', 'NC']
okt_stop = ['Eomi','Punctuation','Unknown', 'Josa']
kkma_stop = ['JK','IC','JC', 'JX','EP','EF','EC', 'ET', 'XP','XS', 'VV', 'ECS', 'ECD','ETD','JKM','ECE','JKO'] 
komoran_stop = ['EC','ETM', 'XPN','XSN', 'XSV', 'XSA','SF','VV','JKO','JX','VCP', 'JKB','EP'] 
# f2 = codecs.open('')
for songid in sentence_dic:
  tmp = tmp  +1
# hannanum 
  filename = str(songid)+"_hannaum_test.txt"
  filename2= str(songid)+"_hannaum_filter.txt"
  for sentence in sentence_dic[songid]:  
    for i in hannanum.pos(sentence,22):
      words.append(i)
      try:
        if(hannanum_stop.index(i[1]) != -1):
          continue
      except:
        imp_words.append(i)
  with open(filename,'w') as f:
      f.write(str(words))
  files.download(filename)
  with open(filename2,'w') as f:
      f.write(str(imp_words))
  files.download(filename2)
  words = []
  imp_words = []
  
# Okt / twitter korean   
  filename = str(songid)+"_okt_test.txt"
  filename2= str(songid)+"_okt_filter.txt"
  for sentence in sentence_dic[songid]:     
    for i in okt.pos(sentence):
      words.append(i)        
      try:
        if(okt_stop.index(i[1]) != -1):
          continue
      except:
          imp_words.append(i)
  with open(filename,'w') as f:
    f.write(str(words))
  files.download(filename)
  with open(filename2,'w') as f:
     f.write(str(imp_words))
  files.download(filename2)
  words = []
  imp_words= []

# komoran   
  filename = str(songid)+"_komoran_test.txt"
  filename2= str(songid)+"_komoran_filter.txt"
  for sentence in sentence_dic[songid]:     
    for i in komoran.pos(sentence):
      words.append(i)
      try:
        if(komoran_stop.index(i[1])!= -1):
          continue
      except:
        imp_words.append(i)
  with open(filename,'w') as f:
     f.write(str(words))
  files.download(filename)
  with open(filename2,'w') as f:
     f.write(str(imp_words))
  files.download(filename2)
  words = []
  imp_words=[]

#kkma 
  filename = str(songid)+"_kkma_test.txt"
  filename2= str(songid)+"_kkma_filter.txt"
  for sentence in sentence_dic[songid]:     
    for i in kkma.pos(sentence):
      words.append(i)
      try:
        if(kkma_stop.index(i[1])!= -1):
          continue
      except:
        imp_words.append(i)
  with open(filename,'w') as f:
     f.write(str(words))
  files.download(filename)
  with open(filename2,'w') as f:
     f.write(str(imp_words))
  files.download(filename2)
  words = []
  imp_words = []
  if(tmp ==10):
    break