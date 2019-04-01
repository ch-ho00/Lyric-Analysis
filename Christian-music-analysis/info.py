import codecs
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

fin_result =[]
#load lyric list
f2 = codecs.open('./results/artistID.txt', 'r', encoding="utf-8")
artist_list = {}
for line in f2:
  if line.find(':') != -1:
    artist_list[line[:line.find(':')-1]] = line[line.find(':')+2:-1].replace(' ','')
for art_id in artist_list:
  url = "https://www.jesusfreakhideout.com/artists/"+str(artist_list[art_id]) +".asp"
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  ol=soup.select("ol")
  result = []
  for line in ol:
    if str(line).find('w3-padding-16') != -1 and str(line).find('w3-padding-16') != None:
        break
    elif str(line).find("cdreviews") != -1 and str(line).find("cdreviews") != None:
        split = str(line.text).split('\r')
        for part in split:
          part = part.replace('\n','')
          if part.find('[') != -1:
            result.append((artist_list[art_id],part[:part.find(',')], part[part.find(',')+1:part.find(',') +6], part[part.find('[')+1: part.find(']')]))
          else:
            result.append((artist_list[art_id],part[:part.find(',')], part[part.find(',')+1:part.find(',') +6], 'Independent'))
        fin_result.append(result)
        break
for art in fin_result:
  print(art)

