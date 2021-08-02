import csv
from collections import defaultdict
import random
import re
import io
from difflib import SequenceMatcher #To measure string similarity

#USED FOR LEVELS 1 and 3

#Keys = katakana, values = Latin
#My dictionary only includes characters that can appear on their own (almost all)
diccio_alfabeto = {"ア":"a","イ":"i","ウ":"u","エ":"e","オ":"o",
                   "カ":"ka","キ":"ki","ク":"ku","ケ":"ke","コ":"ko",
                   "ガ":"ga","ギ":"gi","グ":"gu","ゲ":"ge","ゴ":"go",
                   "サ":"sa","シ":"shi","ス":"su","セ":"se","ソ":"so",
                   "ザ":"za","ジ":"zi","ズ":"zu","ゼ":"ze","ゾ":"zo",
                   "タ":"ta","チ":"chi","ツ":"tsu","テ":"te","ト":"to",
                   "ダ":"da","ヂ":"ji","ヅ":"zu","デ":"de","ド":"do",
                   "ナ":"na","ニ":"ni","ヌ":"nu","ネ":"ne","ノ":"no",
                   "ハ":"ha","ヒ":"hi","フ":"fu","ヘ":"he","ホ":"ho",
                   "バ":"ba","ビ":"bi","ブ":"bu","ベ":"be","ボ":"bo",
                   "パ":"pa","ピ":"pi","プ":"pu","ペ":"pe","ポ":"po",
                   "マ":"ma","ミ":"mi","ム":"mu","メ":"me","モ":"mo",
                   "ヤ":"ya","ユ":"yu","ヨ":"yo",
                   "ラ":"ra","リ":"ri","ル":"ru","レ":"re","ロ":"ro",
                   "ワ":"wa","ヰ":"wi","ヱ":"we","ヲ":"wo","ン":"n"}

#-------------------------------------------------------------

#READING CITIES
csvfileCITIES = open('queryCITIES.csv', encoding = 'utf-8')
readerCITIES = csv.DictReader(csvfileCITIES)

#Gathering cities from the CSV file
dicciodeciudades_katakana = defaultdict() #key English, value katakana
for row in readerCITIES:
    if row['en_label'][0] == 'Q' and row['en_label'][1].isdigit():
        continue #ignore entries with no English label
    if row['ja_label'][0] == 'Q' and row['ja_label'][1].isdigit():
        continue #ignore entries with no Japanese label
    if row['ja_label'][0] not in diccio_alfabeto:
        continue #ignore entries in other scripts

    ciudad = row['en_label']
    ciudadkatakana = row['ja_label']
    dicciodeciudades_katakana[ciudad] = ciudadkatakana
        
#***********************************
        
#READING COUNTRIES
csvfileCOUNTRIES = open('queryCOUNTRIES.csv', encoding = 'utf-8')
readerCOUNTRIES = csv.DictReader(csvfileCOUNTRIES)

#Gathering countries from the CSV file
dicciodecountries_katakana = defaultdict() #key English, value katakana
for row in readerCOUNTRIES:
    if row['en_label'][0] == 'Q' and row['en_label'][1].isdigit():
        continue #ignore entries with no English label
    if row['ja_label'][0] == 'Q' and row['ja_label'][1].isdigit():
        continue #ignore entries with no Japanese label
    if row['ja_label'][0] not in diccio_alfabeto:
        continue #ignore entries in other scripts

    country = row['en_label']
    countrykatakana = row['ja_label']
    dicciodecountries_katakana[country] = countrykatakana
#-------------------------------------------------------------        

#READING x2 CITIES
csvfileCITIES = open('queryCITIES.csv', encoding = 'utf-8')
readerCITIES = csv.DictReader(csvfileCITIES)

#READING x2 COUNTRIES
csvfileCOUNTRIES = open('queryCOUNTRIES.csv', encoding = 'utf-8')
readerCOUNTRIES = csv.DictReader(csvfileCOUNTRIES)

#WRITING To later write questions unto a csv file
mycsv = open('PREkatakanaPLACES_VERYHARD.csv', 'a', encoding="utf8")
cabeceros = ['type','question','correct','distractor1','distractor2']
writer = csv.DictWriter(mycsv, fieldnames=cabeceros, delimiter=';')
writer.writeheader() #Writing the headers

#********** CITIES

for row in readerCITIES:
    if row['en_label'][0] == 'Q' and row['en_label'][1].isdigit():
        continue #ignore entries with no English label
    if row['ja_label'][0] == 'Q' and row['ja_label'][1].isdigit():
        continue #ignore entries with no Japanese label
    if row['ja_label'][0] not in diccio_alfabeto:
        continue #ignore entries in other scripts
    katakana = row['ja_label'] #City in katakana
    ciudad = row['en_label'] #City in English


    pregunta = "Here's a city in katakana: " + katakana + ' Which one is it? '

    #DISTRACTORS: Other city names that are similar in Japanese
    posiblesdistractores = [] #all possible distractors
    
    for ciudadposible in dicciodeciudades_katakana: #I'll check similarity
        #Measuring the similarity takes long, so I first filter by length, which is quick
        if len(dicciodeciudades_katakana[ciudadposible]) == len(katakana):
            similarityratioKATAKANA = SequenceMatcher(None, katakana, dicciodeciudades_katakana[ciudadposible]).ratio()
            if similarityratioKATAKANA >= 0.5:
                posiblesdistractores.append(ciudadposible)
    #I may end up with few possible distractors, so I'll check that there are enough
    if len(posiblesdistractores) > 3:
        distractor1 = random.sample(posiblesdistractores,1)[0]
        if distractor1 == ciudad: #The correct answer can't be used as a distractor
           distractor1 = random.sample(posiblesdistractores,1)[0] 
        distractor2 = random.sample(posiblesdistractores,1)[0]
        if distractor2 == ciudad or distractor2 == distractor1: #No repetitions in the distractors
           distractor2 = random.sample(posiblesdistractores,1)[0] 
        #I may end up with few possible distractors,
           #so I'll only write the questions with good distractors
        if distractor1 != ciudad and distractor1 != distractor2:
            #Writing the csv
            writer.writerow({'type':'CITIES','question': pregunta,'correct': ciudad,
                             'distractor1': distractor1, 'distractor2': distractor2})

#******** COUNTRIES

for row in readerCOUNTRIES:
    if row['en_label'][0] == 'Q' and row['en_label'][1].isdigit():
        continue #ignore entries with no English label
    if row['ja_label'][0] == 'Q' and row['ja_label'][1].isdigit():
        continue #ignore entries with no Japanese label
    if row['ja_label'][0] not in diccio_alfabeto:
        continue #ignore entries in other scripts
    katakana = row['ja_label'] #Country in katakana
    country = row['en_label'] #Country in English

    pregunta = "Here's a country in katakana: " + katakana + ' Which one is it? '

    #DISTRACTORS: Other country names that are similar in Japanese
    posiblesdistractores = [] #all possible distractors
    
    for countryposible in dicciodecountries_katakana: #I'll check similarity
        similarityratioKATAKANA = SequenceMatcher(None, katakana, dicciodecountries_katakana[countryposible]).ratio()
        if similarityratioKATAKANA >= 0.5:
            posiblesdistractores.append(countryposible)
    #I may end up with few possible distractors, so I'll check that there are enough
    if len(posiblesdistractores) > 3:
        distractor1 = random.sample(posiblesdistractores,1)[0]
        if distractor1 == country: #The correct answer can't be used as a distractor
           distractor1 = random.sample(posiblesdistractores,1)[0] 
        distractor2 = random.sample(posiblesdistractores,1)[0]
        if distractor2 == country or distractor2 == distractor1: #No repetitions in the distractors
           distractor2 = random.sample(posiblesdistractores,1)[0] 
        #I may end up with few possible distractors,
           #so I'll only write the questions with good distractors
        if distractor1 != country and distractor1 != distractor2:
            #Writing the csv
            writer.writerow({'type':'COUNTRIES','question': pregunta,'correct': country,
                             'distractor1': distractor1, 'distractor2': distractor2})
#-------------------------------------------------------------
#Closing the files
csvfileCITIES.close()
csvfileCOUNTRIES.close()
mycsv.close()

#-----------------------------------------------------------------------
#Fixing extra line breaks
filecondoblelinebreak = open('PREkatakanaPLACES_VERYHARD.csv', encoding="utf8")
textostringueao = filecondoblelinebreak.read() #Converts to string
textotrasregex = re.sub(r'(\n)(\n)',r'\1', textostringueao) #\1 backref to first item

with io.open("katakanaPLACES_VERYHARD.csv",'a+',encoding='utf8') as f:
    f.write(textotrasregex)
#+ creates new file if none exists
#a append mode

f.close()    

