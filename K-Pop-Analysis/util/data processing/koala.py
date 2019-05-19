from koalanlp.Util import initialize
from koalanlp.proc import *
from koalanlp import API
import os
from koalanlp.proc import SentenceSplitter


def install_java():
  # apt-get install -y openjdk-8-jdk-headless -qq > /dev/null  
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"     #set environment variable

install_java()
# 초기화 합니다.
initialize(java_options="-Xmx4g -Dfile.encoding=utf-8", KKMA="2.0.2", EUNJEON="2.0.0", RHINO="2.0.5", HNN="2.0.5")


tagger = Tagger(API.RHINO)
texts = ["아무도 없는 곳 하얀 하늘을 보며 그대를 생각해 그 대여 함께 해요.","뜨거운 태양 아래에 서 있는 너의 모습에 한순간 나의 마음을 뺏기고 말았어"]
for text in texts:
  sentences = tagger(text)
  out = []
  for sent in sentences:
    for word in sent:
      s = word.getSurface()
      if len(s) < 5 and len(s) > 1:
          out.append(s)
      else:
          # 안녕하/VV 시/EP 어요/EF 
          for morph in word:
                m = morph.getTag()
                if 'V' in list(str(m)) or 'N' in list(str(m)):
                    ss = morph.getSurface()
                    # TODO
                    # run without this line of filtering one letter verb/nouns
                    if len(ss) > 1:
                      out.append(ss)
  print("Current Cleaning")
  print(out)
  print("________________________\n Whole List")
  for sent in sentences:
    for word in sent:
        for morph in word:
              m = morph.getTag()
              ss = morph.getSurface()
              print(ss,m)    
              if 'V' in list(str(m)) or 'N' in list(str(m)):
                  if m != "VCP":
                    ss = morph.getSurface()
                    # TODO
                    # run without this line of filtering one letter verb/nouns
                    # print(ss,m)
                    out.append(ss)
  print("Normal stopword removal Cleaning")
  print(out)
  print("____________________________________________")

 # tagged = tagger.tagSentence("안녕하세요. 눈이 오는 설날 아침입니다.")
             
        #     print("%s/%s " % (morph.getSurface(), morph.getTag()), end='')
  # Print sentences
    # print(sent.surfaceString())
    # print("# Analysis Result")
    # 눈이 오는 설날 아침입니다 .
    # Analysis Result
    # Word [0] 눈이 = 눈/NNG 이/JKS
    # Word [1] 오는 = 오/VV 는/ETM
    # Word [2] 설날 = 설날/NNG
    # Word [3] 아침입니다 = 아침/NNG 이/VCP ㅂ니다/EF
    # for word in sent:
        # print("Word [%s] %s = " % (word.getId(), word.getSurface()), end='')
  
