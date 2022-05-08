#regular expression help for emoticons is taken from https://stackoverflow.com/questions/28077049/regex-matching-emoticons
#for URL Mixed in any form regex https://stackoverflow.com/questions/28077049/regex-matching-url

import json
import re
import ast

from pymongo import MongoClient 
  

client=MongoClient() 

client = MongoClient("MongoDB URL") 
   
mydatabase = client['myMongoTweet'] 
   
mycollection=mydatabase['FilteredTweet']

print("Done with connection")

#import pdb;pdb.set_trace()  
 
def filter(tweet_text):
    tweet_text = re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet_text) #removed URL
    tweet_text = re.sub(r'#', '', tweet_text) #removed hashtag.
    tweet_text = re.sub(r'@', '', tweet_text) #removed @.
    tweet_text = re.sub(r'^RT[\s]+', '', tweet_text) #removed RT text depicting retweet.
    tweet_text = re.sub('[^A-Za-z0-9{}[]"",:_]+', '', tweet_text) #removed special character.
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002500-\U00002BEF"  
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  
        u"\u3030"
                      "]+", re.UNICODE)
    tweet_text = emoji_pattern.sub(r'',tweet_text)
    return tweet_text 


index = 0
# Opening JSON file 
for index in range(1):
    filename = 'TweetExtract.json'
    f = open(filename) 
    
    data = json.load(f) 

    for tweet in data:
        #initialise dictionary
        db_row = dict()
        user = dict()
        retweeted_status = dict()
       
       #check none and filters
        if tweet["text"] is not None:
            tweet_text = filter(tweet["text"])
        if tweet["user"]["description"] is not None:
            tweet_desc = filter(tweet["user"]["description"])
        if tweet["user"]["location"] is not None:
            tweet_loc = filter(tweet["user"]["location"])
        #if tweet['retweeted_status']["text"] is not None:
        #    retweet_text = filter(tweet["retweeted_status"]["text"])
        if tweet["user"]["name"] is not None:
            user_name = filter(tweet["user"]["name"])
        if tweet["user"]["screen_name"] is not None:
            user_screenname = filter(tweet["user"]["screen_name"])

    ##    line = eval(line1)
        user["name"] = tweet["user"]["name"]
        db_row["created_at"] = tweet["created_at"]
        db_row["id"] = tweet["id"]
        db_row["id_str"] = tweet["id_str"]
        db_row["text"] = tweet_text
        user["name"] = user_name
        user["id"] = tweet["user"]["id"]
        user["id_str"] = tweet["user"]["id_str"]
        user["location"] = tweet_loc
        user["followers_count"] = tweet["user"]["followers_count"]
        user["friends_count"] = tweet["user"]["friends_count"]
        user["listed_count"] = tweet["user"]["listed_count"] 

        db_row["user"] = user

        #retweeted_status["created_at"] = tweet["retweeted_status"]["created_at"]
        #retweeted_status["id"] = tweet["retweeted_status"]["id"]
        #retweeted_status["text"] = retweet_text

        #db_row["retweeted_status"] = retweeted_status
        
        db_row["user_location"] = tweet_loc
        db_row["user_screen_name"] = user_screenname
        db_row["user_description"] = tweet_desc
        db_row["quote_count"] = tweet["quote_count"]
        db_row["reply_count"] = tweet["reply_count"]
        db_row["retweet_count"] = tweet["retweet_count"]
        
        #Inserting each record
        # x = mycollection.insert_one(db_row)
        # json_object = json.dumps(tweet)
        with open('filter.json', 'a') as outfile:
            outfile.write(json.dumps(tweet)+ ',\n')
        print("Insert Done!")
        print(index)
 
 
