# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 09:33:56 2021

@author: sheri
"""

import random
from sys import argv
import json

with open('German_Dictionary.txt') as f:
    data = f.read()
eng_germ_dict = json.loads(data)

list_options = list(eng_germ_dict.keys())
str_options = (', '.join(list_options))


def choose_dictionary():
    print(f'Here are the options: {str_options}')
    prompt = '> '
    chosen_dict = input(prompt)
    print(f"You've chosen {chosen_dict}, let's get started!")
    


    def practice_translate():

        keep_working = 'Y'
        while keep_working.upper() == 'Y':
            prompt = '> '
            filtered_dict = eng_germ_dict[chosen_dict]
            
            keys_list = list(filtered_dict)
            key_length = len(filtered_dict)
            min = 0
            max = key_length-1
            key_index = random.randint(min,max)
             
            #get english word that needs to be translated
            to_translate = keys_list[key_index]
            print(f'Please type the German word for: {keys_list[key_index]}')
            attempt = input(prompt)
            #get correct german word
            translated = filtered_dict[to_translate]
            if attempt == translated:
                print('Correct!')
            else:
                print('Please try again')
            keep_working = input('Keep going? (Y/N) ? > ')
        else:
            print('Nice Job today!')
            choose_dictionary()
    practice_translate()
        
choose_dictionary()