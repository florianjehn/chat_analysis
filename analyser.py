# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 19:42:05 2018

@author: Florian Jehn
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
            person = person[:2]
            # Exclude entries where the person is empty
            if person == "":
                continue
            
            # Add a better date describer and make the month better sortable
            month = date.month if date.month > 9 else "0" + str(date.month)            
            month_year = str(date.year) + "/" + str(month)

            # Determine what the message consists of
            topic = determine_message_topic(message)

            # Save the things already known and prepare the other ones
            save_dict = {"date": date, "person": person, "topic": topic,
                         "year/month": month_year}
            # Save the topic
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

            
def plot_whole_timeseries_by_type_person(chat_df):
    """Plots lineplots for all different types and persons"""
    grouped = chat_df.groupby(["topic", "person", "year/month"])
    amounts_per_month = grouped.size()
    persons = chat_df["person"].unique()
    topics = chat_df["topic"].unique()
    fig, subplots = plt.subplots(nrows=len(topics), sharex=True)
    for i, topic in enumerate(topics):
        print(topic)
        ax = subplots[i]
        ax.set_title(topic.title())
        for person in persons:    
            print(person)
            # This will fail if the person has never done this kind of message
            try:
                amounts_per_person_topic = pd.DataFrame(amounts_per_month.loc[(topic, person)].sort_index())
            except:
                amounts_per_person_topic = pd.DataFrame(0, index=sorted(chat_df["year/month"].unique()), columns=[0])
            # Create an empty dataframe with all dates of the original df,
            # So plottin is easier and add all the values from the other df
            plot_df = pd.DataFrame(0, index=sorted(chat_df["year/month"].unique()), columns=["count"])
            plot_df = pd.merge(plot_df, amounts_per_person_topic, left_index=True, right_index=True, how="left")
            plot_df.replace(np.nan, 0, inplace=True)
            del plot_df["count"]
            # Convert it to int
            plot_df[plot_df.columns[0]] == plot_df[plot_df.columns[0]].astype(int)
            # Delete the last row, as the month is not finished
            plot_df = plot_df.iloc[:-1,:]
            # Plot it
            ax.plot(plot_df, label=person)
            # Add the legend only in the first plot
            if i == 0:
                ax.legend()
            # Add the xlabel only in teh last plot and rotate the ticklabels
            if i == len(topics):
                ax.set_xlabel("Year/Month")
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)      
            # Make the plot nicer
            ax.set_facecolor("white")
            ax.grid(color="grey", alpha=0.3)
        
        ax.set_ylabel("Amount")
    fig.set_size_inches(10,30)
    fig.tight_layout()
    plt.savefig("chat.png", dpi=250, bbox_inches="tight")

    
    
    
chat_df = read_chat("club_der_freunde.txt")
print(chat_df)
plot_whole_timeseries_by_type_person(chat_df)

    




























