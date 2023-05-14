'''
This is getting RSS feed from tvn24 and saving it as a pickle
saving it locally

Before getting other feeds, change pickle name at the end of file.
'''
import pickle
import feedparser
import pandas as pd
from datetime import datetime
from dateutil import tz # for adding timezone

#try opening pickle, create if doesn't exist
try:
    df = pd.read_pickle('rssFeedTvnNaj.pickle')
    #take date from first cell of the saved df
    recordedPublished = df['published'].values[:1]
    recordedPublished = pd.to_datetime(recordedPublished)
    #print(recordedPublished)
    #print(recordedPublished.type())
except Exception:
    #if pickle doesn't exist, create one
    #set date to past, use timezone
    recordedPublished = datetime(2000, 1, 1, 12, 0, 0, tzinfo=tz.tzutc()) 
    df = pd.DataFrame(columns = ['published', 'title', 'summary'])
    

#feed = "https://tvn24.pl/najnowsze.xml" #sa tez najwazniejsze
#feed = "https://tvn24.pl/polska.xml"
#feed = "https://tvn24.pl/swiat.xml"
feed = "https://tvn24.pl/najnowsze.xml"
newsFeed = feedparser.parse(feed)
entry = newsFeed.entries[1]

#print (entry.keys())
noOfEntries = len(newsFeed.entries)
#print ('Number of RSS posts :', len(newsFeed.entries))

#  concat (and therefore append) makes a full copy of the data, and constantly reusing this function 
# can create a significant performance hit. If you need to use the operation over several datasets, 
# #use a list comprehension. 
# you should NEVER grow a DataFrame, and that you should append your data to a 
# list and convert it to a DataFrame once at the end. 

#for better performance I create a list of dictionaries and change them into df

#check last entry in feed and compare


column = ['published', 'title', 'summary']
rows_list = []

for entry in newsFeed.entries:
    entryPublished = pd.to_datetime(entry.published)
    if entryPublished > recordedPublished:
        row = [entry.published, entry.title, entry.summary]
        #print(row)
        rows_list.append(dict(zip(column, row)))

dfNew = pd.DataFrame(rows_list, columns=['published', 'title', 'summary'])
df = pd.concat([dfNew, df], ignore_index=True)
#print(df.shape)
#print(df.head())
#print(df.head())
df.to_pickle('rssFeedTvnNaj.pickle')
import os

print(os.getcwd())#check where pickle gets saved
 



