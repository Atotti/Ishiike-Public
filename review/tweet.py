import tweepy
from pprint import pprint
import environ

env = environ.Env()
env.read_env('.env')

# API情報を記入
BEARER_TOKEN = env('BEARER_TOKEN')
API_KEY = env('API_KEY')
API_SECRET = env('API_SECRET')
ACCESS_TOKEN = env('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = env('ACCESS_TOKEN_SECRET')


# クライアント関数を作成
def ClientInfo():
    client = tweepy.Client(bearer_token    = BEARER_TOKEN,
                           consumer_key    = API_KEY,
                           consumer_secret = API_SECRET,
                           access_token    = ACCESS_TOKEN,
                           access_token_secret = ACCESS_TOKEN_SECRET,
                          )
    
    return client

# 関数
def CreateTweet(message):
    tweet = ClientInfo().create_tweet(text=message)
    return tweet
