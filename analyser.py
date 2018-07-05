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
            
            # Stich the rest of the message togeher again
            message_with_person = " ".join(split_comma)
            
            # Get person and message
            person, message = seperate_messsage_person(message_with_person)
            
            # Shorten Person
            person = "F" if person == "Florian(you)" else "P"

            # Determine what the message consists of
            topic = determine_message_topic(message)

            # Save the things already known and prepare the other ones
            save_dict = {"date": date, "person": person, "file": 0, "pic": 0,
                         "voice_msg": 0, "sticker": 0, "link": 0, "gif": 0,
                         "text": 0, "video": 0, "contact": 0, "location": 0}
            # Save the topic
            save_dict[topic] = 1
            save_list.append(save_dict)
        
    return create_dataframe(save_list)


def create_dataframe(save_list):
    """
    Creates a dataframe from the collected data
    """
    df = pd.DataFrame(save_list)
    df.set_index("date", inplace=True)
    return df
            
            
def seperate_messsage_person(message_with_person):
    """
    Seperates the person from the message and returns both
    """
    # Split by the first colon
    split_colon = message_with_person.split(":")
    # Get the person out of it and avoid the first whitespace
    person = split_colon.pop(0)[1:]
    # Stitch the message together again
    message = " ".join(split_colon)
    return person, message


def determine_message_topic(message):
    """
    Determines whats in the message and returns a string with the name of the 
    topic.
    """
    if "[[" not in message:
        return "text"
    lookup_dict = {"Document": "file", "Photo": "pic", 
                   "Voice": "voice_msg", "Sticker": "sticker",
                   "Webpage": "link", "GIF": "gif", "Video": "video", 
                   "Contact": "contact", "Geo": "location"}
    # Get ride of rest of the message
    msg_type = message.split("]]")[0]
    # Get rid of leading whitespace
    msg_type = msg_type[1:]
        # Delete the leading parantheses
    msg_type = msg_type.replace("[[", "")
    # Get ride if weird sticker emojis
    if "Sticker" in msg_type:
        msg_type = msg_type.split(" ")[1]
    # Get rid of additonal type information
    msg_type = msg_type.split(" ")[0]
    # Return the correct type
    return lookup_dict[msg_type]

         
            
    
    
    
    
chat_df = read_chat("chat_hist_pau_begin_bis_180705.txt")
print(chat_df)
    

