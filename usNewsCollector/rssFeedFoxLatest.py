'''
This is getting RSS feed from tvn24 and saving it as a pickle
saving it locally

Before getting other feeds, change pickle name at the end of file.


example content

'content': [{'type': 'text/html', 'language': None, 'base': 'https://moxie.foxnews.com/google-publisher/latest.xml', 
'value': '<p><a href="https://www.foxnews.com/category/world/world-regions/russia" target="_blank">Russian government officials</a> are claiming Ukrainian forces 
attempted to kill President Vladimir Putin with a failed drone attack.</p> <p>Officials say two drones were used in the 
"assassination attempt" at <a href="https://www.foxnews.com/category/world/personalities/vladimir-putin" target="_blank">the president\'s 
residence</a> within the Kremlin compound, but were disabled by Russian defense systems.</p> <p>No injuries or damage to the residence was 
reported. Putin was seen in video and photos released Wednesday meeting with a regional governor outside Moscow.</p> 
<p>The Kremlin called the incident a "terrorist action" and threatened <a href="https://www.foxnews.com/category/world/conflicts/ukraine" 
target="_blank">retaliation against Ukraine</a> in reports from state media outlet RIA.</p> <p>"The Kremlin has assessed these actions as 
a planned terrorist act and an assassination attempt on the president on the eve of Victory Day, the May 9 Parade," RIA said.</p> 
<p>Unconfirmed videos have begun circulating online appearing to show a drone being shot down over the Kremlin, and smoke rising in Moscow.
\xa0</p> <p>"It’s too early to tell who is behind the purported drone attack and whether the attempted attack actually did happen. 
If Ukraine did do it, it would be viewed by Russia as massive escalation, allowing Putin to obliterate Kyiv, including Zelensky’s residence," 
former <a href="https://www.foxnews.com/person/k/rebekah-koffler" target="_blank"><u>Defense Intelligence Agency officer Rebekah Koffler</u></a> 
told Fox News Digital.</p> <p>She continued, "The way the article is written has signs of Russian disinformation.
 Versions of this article are all across Russian media, which indicates to me that the Kremlin has approved publishing it. 
 If it is a Russian "active measure", the goal would be provocation, to provoke, laying the groundwork and the pretext for a "retaliation" which the arews.com/static.foxnews.com/foxnews.com/content/uploads/2023/05/931/523/Russian-President-Vladimir-Putin-2.jpg?ve=1&tl=1',
 'type': 'image/jpeg', 'expression': 'full', 'width': '931', 'height': '523'}]

 entry.content[0]['value']
'''
import pickle
import feedparser
import pandas as pd
from datetime import datetime
from dateutil import tz # for adding timezone

#try opening pickle, create if doesn't exist
try:
    df = pd.read_pickle('rssFeedFoxLatest.pickle')
    #take date from first cell of the saved df
    recordedPublished = (df['published'].values[:1])[0]#it's a string in array, have toextract it first
    #Wed, 03 May 2023 04:55:57 EDT
    #format: format='%a, %b %m %Y %H:%M:%S'
    #recordedPublished = pd.to_datetime(recordedPublished, format='%a %b %m %Y %H:%M:%S')
    recordedPublished = recordedPublished[5:25]
    recordedPublished = pd.to_datetime(recordedPublished, format="%d %b %Y %H:%M:%S")
    recordedPublishedZone = recordedPublished.tz_localize('US/Eastern') #need to add this for Fox as they have EDT time
    print(recordedPublishedZone)
    #print(recordedPublished.type())
except Exception:
    #if pickle doesn't exist, create one
    #set date to past, use timezone
    recordedPublishedZone = datetime(2000, 1, 1, 12, 0, 0, tzinfo=tz.tzutc()) 
    df = pd.DataFrame(columns = ['published', 'title', 'summary', 'content'])
    

#feed = "https://tvn24.pl/najnowsze.xml" #sa tez najwazniejsze
#feed = "https://tvn24.pl/polska.xml"
#feed = "https://tvn24.pl/swiat.xml"
#feed = "https://www.theguardian.com/uk/rss"
feed = "https://moxie.foxnews.com/google-publisher/latest.xml"
newsFeed = feedparser.parse(feed)
#entry = newsFeed.entries[1]

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


column = ['published', 'title', 'summary', 'content']
rows_list = []

for entry in newsFeed.entries:
    #entryPublished = pd.to_datetime(entry.published, format='%a %b %m %Y %H:%M:%S')
    entryPublished = entry.published[5:25]
    entryPublished = pd.to_datetime(entryPublished, format="%d %b %Y %H:%M:%S")
    entryPublishedZone = entryPublished.tz_localize('US/Eastern')
    #print(entryPublishedZone)
    #print(recordedPublishedZone)
    
    if entryPublishedZone > recordedPublishedZone:
        row = [entry.published, entry.title, entry.summary, entry.content[0]['value']]
        #print(row)
        rows_list.append(dict(zip(column, row)))
    elif entryPublishedZone == recordedPublishedZone:
        #check if id already in id list
        if entry.title not in df.title.values:
            row = [entry.published, entry.title, entry.summary, entry.content[0]['value']]
        #print(row)
            rows_list.append(dict(zip(column, row)))

dfNew = pd.DataFrame(rows_list, columns=['published', 'title', 'summary', 'content'])
df = pd.concat([dfNew, df], ignore_index=True)
#print(df.shape)
#print(df.head())
#print(df.head())
df.to_pickle('rssFeedFoxLatest.pickle')
import os

print(os.getcwd())#check where pickle gets saved
 



