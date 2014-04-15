#Twitter handler
import twitter, math
from debug import log

class Tweeter:

	def __init__(self):
		# login as unclecsporttime
		self.api = twitter.Api(consumer_key='UUglFzLUxQzdTxDHssbX4g',
        consumer_secret='Cz006KLdT8vCDMpJJQSeAY69BXzEmE0Eup5mNzxyxQ',
        access_token_key='2440307432-NNZwDBvTk1dOikeMakZD2zShgWey1k7pB1tc1vs',
        access_token_secret='OAGVt4Hq6dzX7NbpXaC1jmsnHPsxjvWVp85ydOhK54tHJ')

	def post_summary(self,summary):
		for tweet_text in self.split_tweet(summary):
			self.api.PostUpdate(tweet_text)
		log("Posted summary %s" % summary)

	# Returns a list of tweets, split by sentence. Works for text requring <10
	# tweets
	def split_tweet(tweet):
		if len(tweet) <= 140:
			return [tweet]

		tweets = []

		sentences = tweet.split('.')
		cur_tweet_content = ''
		cur_tweet_number = 1

		while sentences:
			cur_sent = sentences.pop(0).lstrip()
			if cur_sent:
				if len(cur_tweet_content) + len(cur_sent) + 2 < 131:
					cur_tweet_content+=" " + cur_sent + '.'
				else:
					cur_tweet_content+='.. [%s/' % (cur_tweet_number)
					cur_tweet_content = cur_tweet_content.lstrip()
					tweets.append(cur_tweet_content)
					cur_tweet_content = cur_sent+'.'
					cur_tweet_number+=1

		cur_tweet_content+=' [%s/' % (cur_tweet_number)
		cur_tweet_content = cur_tweet_content.lstrip()
		tweets.append(cur_tweet_content)

		for i in range(0,len(tweets)):
			tweets[i] = tweets[i]+'%s]' % (cur_tweet_number)

		return tweets

