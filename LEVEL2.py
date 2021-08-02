from pandas import DataFrame, read_csv #For dataframes
#import matplotlib.pyplot as plt
import pandas as pd #For dataframes
import random
from difflib import SequenceMatcher #To measure string similarity
import jaconv #To convert between Japanese scripts

def LEVEL2function(topic_chosen):
    #--- TOPIC BOTH
    myfile = 'QUESTION_GENERATION/katakanaPLACES_HARD.csv'
    mydf = pd.read_csv(myfile,sep = ';') #Create dataframe from csv, I specify separator is ;

    #--- TOPIC CITIES
    CITIESdf = mydf.loc[mydf['type'] == 'CITIES'] #Subset of dataframe


    #--- TOPIC COUNTRIES
    COUNTRIESdf = mydf.loc[mydf['type'] == 'COUNTRIES'] #Subset of dataframe

    #--- CHOSEN TOPIC
    chosen_df = mydf #Set the whole dataframe as default
    if topic_chosen == 'CITIES':
        chosen_df = CITIESdf
    if topic_chosen == 'COUNTRIES':
        chosen_df = COUNTRIESdf
    if topic_chosen == 'BOTH':
        chosen_df = mydf    

    #------------------------------------------------------------------ LEVEL 2
    wannagoon = 'y' #Set variable to see if user wants more questions
    while wannagoon == 'y':
        randomnumber = random.randint(chosen_df.first_valid_index(),chosen_df.last_valid_index())
        question = chosen_df.loc[randomnumber]['question']
        hint = chosen_df.loc[randomnumber]['hint']
        correct = chosen_df.loc[randomnumber]['correct']
        distractor1 = chosen_df.loc[randomnumber]['distractor1']
        distractor2 = chosen_df.loc[randomnumber]['distractor2']
        listofoptions = [correct, distractor1, distractor2]
        random.shuffle(listofoptions) #I shuffle the options
        print(question)
        print(hint)
        for item in listofoptions:
            print('* ',item)
        answer = input("What's your answer? \n(Copy or type, don't worry about accents of uppercase): ")

        #I measure how similar the answer is to each option
        similarityratioCORRECT = SequenceMatcher(None, answer, correct).ratio()
        similarityratioDIST1 = SequenceMatcher(None, answer, distractor1).ratio()
        similarityratioDIST2 = SequenceMatcher(None, answer, distractor2).ratio()
        listsimilarities = [similarityratioCORRECT,similarityratioDIST1,similarityratioDIST2] 
        listsimilaritiesSORTED = (sorted(listsimilarities,reverse=True))

        if listsimilaritiesSORTED[0] == similarityratioCORRECT:
            print("✿ ビンゴ! You're correct, the answer is ", correct)
            print('\n')
        if listsimilaritiesSORTED[0] != similarityratioCORRECT:
            print("(;´・`)> 違う Sorry, keep practicing!")
            #I convert the distractors to print them as feedback
            hiragana1 = jaconv.alphabet2kana(distractor1.lower())
            katakana1 = jaconv.hira2kata(hiragana1)
            hiragana2 = jaconv.alphabet2kana(distractor2.lower())
            katakana2 = jaconv.hira2kata(hiragana2)
            print(distractor1, 'would be ', katakana1, ' (automatically transcribed)')
            print(distractor2, 'would be ', katakana2, ' (automatically transcribed)')
            print('\n')
        #I ask the user if they want to continue
        wannagoon_input = input('Want more questions? Type y for YES or n for NO: ')
        if wannagoon_input != 'y' and wannagoon_input != 'n':
            print("I'll assume you want no more questions 【・_・?】 ")
            wannagoon = 'n'
        if wannagoon_input == 'y': 
            wannagoon = 'y'
        if wannagoon_input == 'n': 
            wannagoon = 'n'
    if wannagoon == 'n':
        return(print('またね！ ( ･ω･)ﾉ'))


