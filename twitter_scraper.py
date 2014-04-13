import twitter
from alchemyapi import AlchemyAPI
import pickle
import re

from debug import log

# ARBITRARY CONSTANT FUNTIME
RELEVANCE_FLOOR = 0.45

# BLACKLIST
BLACKLIST_USERS = ['iBetWinners'] #tweet.user.screen_name
BLACKLIST_ITEMS = ['@iBetWinners','RT ']

URL_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

class TwitterScraper:
  def __init__(self):
    # login as unclecsporttime
    self.api = twitter.Api(consumer_key='bzlEXMYo3FKTRpLUdo4VegqAU',
        consumer_secret='EfNNNwnYok554xtWnnCB5owumZihU8QUsxwIu5R9cPbj86WxFG',
        access_token_key='2440307432-b601xzDLLzr9nm4FckxcZN6o2jsvgce0AHJfmAZ',
        access_token_secret='snt0USzE8WfGeSB27kmiMaDtZYyJAJeWwLjQZZTXMWlgb')
    self.aa = AlchemyAPI()

  """
  get_tweets: takes a search query

  return:
      list of sanitized tweets as strings
  """
  def get_tweets(self, query):
    log("Loading tweets for '%s'..."%query)
    tweets = self.api.GetSearch(term=query,count=50)
    #tweets = pickle.load(open("search_res", "rb"))

    log("Preprocessing tweets...")
    discard_count = 0
    results = []

    for tweet in tweets:
      uname = tweet.user.screen_name
      text  = tweet.text

      # Drop URLs
      text = re.sub(URL_REGEX, '', text)

      #print " >> @%s <<\n%s"%(uname,text)
      # Check blacklists
      if uname in BLACKLIST_USERS:
        log("@%s - discarded: blacklist user."%(uname),' >')
        discard_count = discard_count + 1
        continue
      if sum([(blacklist_text in text) for blacklist_text in BLACKLIST_ITEMS]):
        log("@%s - discarded: blacklist str"%uname,' >')
        discard_count = discard_count + 1
        continue

      results.append(text.encode('ascii','ignore'))

    log("Done preprocessing: %d/%d tweets discarded."%(discard_count,len(tweets)))
    return results

  """
  analyze_tweets: takes a list of strings, runs sentiment analysis and keyword
      parsing on it.

  return:
      a dictionary mapping keywords to relevance sentiment, and score.
      score: <0 is negative, >0 is positive, abs<.15 is mixed.

  """
  def analyze_tweets(self, tweets):
    log("Analyzing keywords...")
    query_text = ' '.join(tweets)
    response = self.aa.keywords('text',query_text,{'sentiment':1,'maxRetrieve':100})
    #response = pickle.load(open('keywords.p','rb'))

    results = {}

    if response['status'] == 'ERROR':
      log("ERROR: Keyword analysis failed...")
      print response
      return results

    for keyword in response['keywords']:
      if float(keyword['relevance']) > RELEVANCE_FLOOR:
        if 'score' in keyword['sentiment']:
          score = float(keyword['sentiment']['score'])
        else:
          score = 0.0 #invalid don't look at me :(
        results[keyword['text'].lower()] = {
            'relevance':float(keyword['relevance']),
            'sentiment':keyword['sentiment']['type'],
            'score':score}

    log("Analysis Complete.")
    return results

if __name__=='__main__':
  log("TwitterScraper test script running...")
  ts = TwitterScraper()
  r= ts.analyze_tweets(ts.get_tweets('#Rockies #Giants'))
  print r