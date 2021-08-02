import re #regex
import random #select random items
from pandas import DataFrame, read_csv #For dataframes
import pandas as pd #For dataframes
from difflib import SequenceMatcher #To measure string similarity
import jaconv #To convert between Japanese scripts


#------------------------------------------------ TOPIC SELECTION
#Asking the user to select a topic
print('\n')
print('カタカナを練習しましょう! ✧٩(•́⌄•́๑)')
print('\n')
print('Katakana is often used to write the names of cities or countries outside Japan')
topic_chosen = 'nothing'

while topic_chosen == 'nothing':
    topic_chosen_input = input('What do you want to practice now, CITIES or COUNTRIES (or both)? ')

    #I use regex to find the topic in the sentence written by the user
    patternBOTH = re.findall(r'both|((city|cities).*(country|countries))|((country|countries).*(city|cities))', topic_chosen_input, re.IGNORECASE)
    patternCITY = re.findall(r'city|cities', topic_chosen_input, re.IGNORECASE)
    patternCOUNTRY = re.findall(r'country|countries', topic_chosen_input, re.IGNORECASE)
    patternTOTAL = re.findall(r'both|city|cities|country|countries', topic_chosen_input, re.IGNORECASE)
    
    if len(patternTOTAL) == 0: #If the user doesn't specify a topic, I ask again
        topic_chosen = 'nothing'
    if len(patternBOTH) > 0:
        topic_chosen = 'BOTH CITIES AND COUNTRIES'
    if len(patternBOTH) == 0:    
        if len(patternCITY) != 0:
            topic_chosen = 'CITIES'                   
        if len(patternCOUNTRY) != 0:
            topic_chosen = 'COUNTRIES'
print('Ok, so your practice topic will be:') 
print(topic_chosen)
#----------------------------------- LEVEL SELECTION
print("I'll give you the name of a place in katakana and you have to select the English equivalent")
print("But first, choose your level:")
print("* LEVEL 1: You'll be given que transcription of the first character as a clue")
print("* LEVEL 2: You also get a clue, but that character will appear somewhere in all the options")
print("* LEVEL 3: You get no clues")
print("* LEVEL 4: No clues, and all the options will be similar in Japanese")

level = 'nothing'
while level == 'nothing':
    level_input = input('Type the number of the level you want: ')
    if ('1' not in level) and ('2' not in level) and ('3' not in level) and ('3' not in level):
        level == 'nothing'
    if '1'in level_input:
        print("You have chosen LEVEL 1")
        print('\n')
        level = '1'
    elif '2'in level_input: #ELIF so that if they say 14 it choses 1
        print("You have chosen LEVEL 2")
        print('\n')
        level = '2'
    elif '3'in level_input:
        print("You have chosen LEVEL 3")
        print('\n')
        level = '3'
    elif '4'in level_input:
        print("You have chosen LEVEL 4")
        print('\n')
        level = '4'

if level == '1':
    import LEVEL1
    LEVEL1.LEVEL1function(topic_chosen)
if level == '2':
    import LEVEL2
    LEVEL2.LEVEL2function(topic_chosen)
if level == '3':
    import LEVEL3
    LEVEL3.LEVEL3function(topic_chosen)
if level == '4':
    import LEVEL4
    LEVEL4.LEVEL4function(topic_chosen)

   




