# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 19:42:05 2018

@author: Florian Jehn
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def read_chat(file):
    """
    Reads in the Chat and creates a df from it
    """
    # List to save all the dictionaries
    save_list = []
    
    # Loop through the file
    with open(file, "r", encoding="utf8") as infile:
        for line in infile:
            # Split the file in what is presumably a datetime and a message
            split_comma = line.split(",")
            # Split the thing that should be the datetime into presumably date and time
            split_whitespace = split_comma.pop(0).split(" ")
            # Determine if the first part of split white is a date by trying to convert it
            try:
                date = datetime.datetime.strptime(split_whitespace[0], '%d.%m.%Y')
            # Skip the line if a value error is raised, as this means that it 
            # is not a date
            except ValueError:
                continue
            # Dictionary to save the results of the line
            save_dict = {"date": date}
            
            # Stich the rest of the message togeher again
            message_with_person = " ".join(split_comma)
            # Split by the first colon
            split_colon = message_with_person.split(":")
            person = split_colon.pop(0)[1:]
            message = " ".join(split_colon)
            print(date)
            print(person)



            
            save_list.append(save_dict)

            
            
    
    
    
    
chat_df = read_chat("chat_hist_pau_begin_bis_180705.txt")
    

