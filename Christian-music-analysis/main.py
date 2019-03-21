#-*- coding: utf-8 -*-
import codecs
from scrape  import *
from topic_model import *
save_dir = "./results"
num_topics = [2,3,4,5,6]
# #lyric list
# ll = lyric_list(artist_track(artist_list(save_dir),save_dir),save_dir)

#load lyric list
f2 = codecs.open('./results/lyric.txt', 'r', encoding="utf-8")
lyric_list = {}
lyric = ""
for line in f2:
  if line.find(':') != -1:
    lyric_list[line[:line.find(':')-1]] = line[line.find(':')+3:]

# lemmatized lyric list
lll = lemmatize(lyric_list,save_dir)

#Check unseen text in dictionary format 
test_texts ={   
                1:"Come and find me Lord Come and find me Lord, I need Your touch tonight Ive lost my way again  Come and find me Lord Come and find me Lord, I swear that I wont hide Its first time in a long time  You give me comfort You give me love You give me wonder I could not dream up You give me Father, and Youve given me Your Son Given me Your Spirit, Youve given me the One that  I can cling to I can hold onto You In these times of doubt and fear I want to burn with hope I want to trust and always know that You are near, You are near to those who cry  Come and find me Lord Come and find me Lord, I need Your touch tonight Ive lost my way again  Come and find me Lord Come and find me Lord, I promise I wont hide But let you in on the inside" ,
                2:"You said, Come to Me if youre weak (I wont look away) And I will keep you close But the closer I get, the harder it seems I find myself pulling away from all of the things I believe  CHORUS Lord, dont give up on me, its You I need So let Your love rain down upon my soul Filling up the deepest hole I still love You so I have tried to cross this river wide And even though the storms were raging high I could see Your light shining constantly (I could see the morning light shining constantly) Constantly, You were always there  You said Lay it down, give it up (I will understand) No matter what it is But instead I face failures and constant disbelief That You could ever love me knowing the secrets I keep  CHORUS  Despite my broken heart and shattered dreams Lord, Youre right there reminding me, reminding me  Oh, I have called to You in time of need You let Your love rain down upon my soul Constantly You let me know, I still love you so Oh, I have tried to cross this river wide And even though the storms were raging high I could see the morning light, shining in the sunrise Constantly ",
                3:" You have never changed your ways You think that you can own me like a slave And I want to walk away But every time I try youre in my face  You say I could have it all Trust you, you will never let me fall And my heart feels bound to your control But my spirit says, no, no, no  CHORUS Stop right there! Suddenly temptations flying Everywhere And you think youve got me down Well think again, Im not youre friend Its plain to see, Im not youre property (Dont play with me, Im not youre property)  Ring! Its you once again Begging me to listen to your plan But you see Ive found the truth Cause I have been redeemed and so were though  You say I could have it all Trust you, you will never let me fall I dont have to give into your demands The powers not in your hands  CHORUS (2x)  I dont have to do anything you want me to I dont need you to make me feel like I want more Cause God has shown His love is your weakness He is above and beyond all you can do  CHORUS (4x)" , 
                4: "I led a lonesome journey Full of disdain and furry I kept my angered yearning Close to me like fire burning I watched a million chances Slip through my weathered hands I almost lost myself  When I looked around there was no one else  CHORUS In the nick of time You opened up my mind And suddenly I saw the world much clearer In the nick of time You turned the water to wine And suddenly I didn't feel the fear Right before my eyes You showed me there was life to be found You're the miracle I prayed about You were the One to save my life In the nick of time  I followed habits around Been swept up above the clouds But fallen down, left shaken Abandoned by the pills I'd taken I could have kept on going With no one ever knowing You really wants to see a tired nobody like me?  CHORUS (repeat 2x)  I could not, I could not believe That You were right there waiting I never, no, I never dreamed That you'd be right there waiting Ooh, You were there for me And when I couldn't see, I couldn't, no, I couldn't see You showed me life Life... You showed me life Life... You showed me life, You showed me life  CHORUS " , 
                5: "Theres ten hours between us tonight And I feel like my heart will break  Cause its been way too long Since Ive last seen your face What Id give if you were here with me now And I was lost in your touch If I know my heart Theres nothing Ive ever wanted so much But to love you Just to love you Its all I wanna do Theres ten hours between us tonight And I feel like I could die But all the pain would just Go away if I could look in your eyes  And love you Just love you  Its all I wana do  Cause I know youre the one That Ive been praying for I could love you for a thousand years And wish for a thousand more Theres ten hours between us tonight But tonight can only last so long By twelve oclock tomorrow baby Youll be here in my arms And Ill hold you close to my heart And I pray you feel my love Until that day when time or space Will never again separate us And Ill love you Oh, Ill love you Its all I ever do  Cause I know youre the one  It just feels so right Would it be ok with you If I loved you for the rest of my life "
            }
test_texts = lemmatize_unseen(test_texts)
coherence_score = []
for num_topic in num_topics:
    lda, dic = create_lda(num_topic,lll)
    for text in test_texts:
        bow_text = [dic.doc2bow(text)]
        text2topic(lda ,bow_text)
    hdpmodel = create_hdp(num_topic,lll)
    lsimodel = create_lsi(num_topic,lll)
    coherence_score.append(evaluate(lda,lll))
    lda_visualize(lda, lll, num_topic)
plot_coherece(num_topics, coherence_score)

