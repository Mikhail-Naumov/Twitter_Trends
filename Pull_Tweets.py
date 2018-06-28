import time
import oauth2
import tweepy
import pandas as pd
from tqdm import tqdm
from Twitter_codes import keys

CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET = keys()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

search = ['@McDonalds', 
         '@Sonicdrivein', 
         '@Starbucks',
         '@Shakeshack',
         '@Dominos',
         '@DennysDiner',
         '@ChipotleTweets',
         '@Wendys',
         '@Dunkindonuts']

date = time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))

all_companies = []
for company in tqdm(search):
    list_tweets = []
    for tweet in tweepy.Cursor(api.search, q=company, retry_delay=5, wait_on_rate_limit=True, lang="en").items(50):
        if not tweet.retweeted:
            if not tweet.is_quote_status:
                if not tweet.user.screen_name == company[1:]:
                    twitter_dic = {}
                    twitter_dic['Company'] = company
                    twitter_dic['time_tweeted'] = tweet.created_at
                    twitter_dic['unique_code'] = tweet.id_str

                    twitter_dic['text'] = tweet.text
                    twitter_dic['meta_lang'] = tweet.metadata['iso_language_code']
                    twitter_dic['hashtag'] = tweet.entities['hashtags']
                    twitter_dic['source'] = tweet.source

                    twitter_dic['retweet_count'] = tweet.retweet_count     
                    twitter_dic['favorite_count'] = tweet.favorite_count
                    twitter_dic['user_followers_count'] = tweet.author.followers_count
                    twitter_dic['user_name'] = tweet.author.name
                    twitter_dic['user_location'] = tweet.author.location
                    twitter_dic['number_of_user_tweets'] = tweet.author.statuses_count
                    twitter_dic['user_is_verified'] = tweet.author.verified
                    twitter_dic['user_profile_text'] = tweet.author.description
                    twitter_dic['number_of_people_they_follow'] = tweet.author.friends_count
                    list_tweets.append(twitter_dic)
    all_companies.extend(list_tweets) 

df = pd.DataFrame(all_companies)

with open('./Data/Tweets_{}.csv'.format(date), 'a') as f:
    df.to_csv(f, header=False)