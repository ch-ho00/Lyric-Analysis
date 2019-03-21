import os
import sys
import urllib.request
import codecs
from google.cloud import translate

def papago_translate(sentence_dic):
    client_id = "jLMwTd83YMjFqdIPLiCM"
    client_secret = "r6ckffVH34"

    for idd in sentence_dic:
        for sentence in sentence_dic[idd]:
            encText = urllib.parse.quote(sentence)
            data = "source=ko&target=en&text=" + encText
            url = "https://openapi.naver.com/v1/language/translate"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                response_body = str(response_body)
                print(response_body[response_body.find("translatedText")+len("translatedText")+3:response_body.find("srcLangType")-3])
                add = response_body[response_body.find("translatedText")+len("translatedText")+3:response_body.find("srcLangType")-3]
                with codecs.open("./data/translated.txt",'a',encoding="utf-8") as f:
                    f.write(add)
                    f.write('\n')
            else:
                print("Error Code:" + rescode)
def google_translate(sentence_dic,translate_client):
    # The target language
    target = 'en'
    tmp = 1
    for text in sentence_dic:
        print(sentence_dic[text])
        translation = translate_client.translate(
            sentence_dic[text],
            target_language=target)
        print(u'Translation: {}'.format(translation['translatedText']))
        tmp +=1
        if(tmp == 10):
            break