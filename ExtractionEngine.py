#eference Tweepy documentation

#Extracts tweet and stores it in different files which will not contain more than  100 tweets each. 
import tweepy as tw

import string
import json

 
con_key = "eP3FIjP"
con_secret = "wVfW2fCeUer00b39OZv8cUfDkx7D5BjhU6e"
access_key= "1277230588550959104-4ENWUx0iPp"
access_secret = "NbgKPPYZeC"
 
auth = tw.OAuthHandler(con_key, con_secret)
auth.set_access_token(access_key, access_secret)
 
api = tw.API(auth,wait_on_rate_limit=True)

#self.file = open("TweetExtract.json","a")
tweet_list=[]
class MyStreamListener(tw.StreamListener):
    def __init__(self,api=None):
        super(MyStreamListener,self).__init__()
        self.num_tweets=0
        self.file=open("1rawfile0.json","w")
    def on_error(self, status_code):
        if status_code == 420:
            print("Connection Failed!")
            return False
    index = 0
    def on_status(self,status):
        tweet=status._json
        self.file.write(json.dumps(tweet)+ ',\n')
        tweet_list.append(status)
        self.num_tweets+=1
        if self.num_tweets % 100 == 0:
            s_file = '1rawfile'+str(self.index + 1) +'.json'.format(self.num_tweets + 100)
            self.file = open(s_file,"w")
            self.index+=1
        if self.num_tweets<3000:
            print(self.num_tweets)
            return True
        else:
            return False
        self.file.close()

myStream = MyStreamListener()
st =tw.Stream(auth,listener=myStream)
#this line filters twiiter streams to capture data by keywords
st.filter(track=['covid','emergency','immune','vaccine',
'flu','snow'])
