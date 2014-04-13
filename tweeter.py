#Twitter handler
import twitter
from debug import log

class Tweeter:

	def __init__(self):
		# login as unclecsporttime
		self.api = twitter.Api(consumer_key='UUglFzLUxQzdTxDHssbX4g',
        consumer_secret='Cz006KLdT8vCDMpJJQSeAY69BXzEmE0Eup5mNzxyxQ',
        access_token_key='2440307432-NNZwDBvTk1dOikeMakZD2zShgWey1k7pB1tc1vs',
        access_token_secret='OAGVt4Hq6dzX7NbpXaC1jmsnHPsxjvWVp85ydOhK54tHJ')

	def post_summary(self,summary):
		self.api.PostUpdate(summary)
		log("Posted summary %s" % summary)
