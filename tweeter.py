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
		if len(summary) > 140:
			sentences = summary.split('.')
			summary_1 = ''
			summary_2 = ''
			for sentence in sentences:
				if len(summary_1) + len(sentence) + 5 < 140:
					summary_1 += sentence + '.'
				else:
					summary_1 += ' 1/2'
					for sent in sentences[sentences.index(sentence):]:
						summary_2 += sent + '.'

					summary_2 += ' 2/2'
					break
			self.api.PostUpdate(summary_1)
			self.api.PostUpdate(summary_2)

		else:
			self.api.PostUpdate(summary)
			log("Posted summary %s" % summary)
