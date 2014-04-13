# Creates the events based on data from metrics
from event import *
from debug import log
import random

# Arbitrary Constants
INNING_RUN_PERCENT_THRESHOLD = .4
INNING_RUN_TOTAL_THRESHOLD = 3
INNING_RUN_LOSS_MULTIPLIER = .75
IMPRESSIVE_AMOUNT_OF_INNINGS_PITCHED = 8
TEAM_AVERAGE_INTERESTINGNESS_THRESHOLD = 0.15
LEAD_CHANGE_THRESHOLD = 3
GRAND_SLAM_RUNNER_COUNT = 3

# Arbitrary Weights
INNING_RUN_MAX_WEIGHT = .7
STAR_PITCHER_BASE_WEIGHT = 0.4
NON_RBI_RUNS_MAX_WEIGHT = -0.6
NON_RBI_RUNS_WEIGHT_PER = -0.08
TEAM_AVERAGE_DIFFERENCE_POINTS = 0.1
LEAD_CHANGE_TAKE_AND_HOLD_WEIGHT = 0.2
LEAD_CHANGE_MAX_WEIGHT = 0.5
HOME_RUN_WEIGHT = 0.4
HOME_RUN_RUNNER_BONUS = 0.09

# Event Types
SUMMARIZING = 0
SCORING_TEAM = 1
SCORING_INDIVIDUAL = 2
PITCHING = 3


from metrics import *
from summary_builder import *
from event import *
class EventBuilder:
	def __init__(self, gameData):
		if (int(gameData['linescore']['r']['home']) > int(gameData['linescore']['r']['away']) ):
			self.winning_team = "home"
		else:
			self.winning_team = "away"

		self.gameData = gameData



	def build_events(self):
		#inning runs total runs
		inning_runs = self.build_inning_events(Metrics.InningRunsTotalRuns(self.gameData))

		#walked in runs
		walked_runs = self.build_walks_events(Metrics.WalksAndBalks(self.gameData))

		#pitching changes
		pitching_changes = self.build_pitching_change_events(Metrics.PitchingChangeDistribution(self.gameData))

		#Game batting ave
		game_batting_ave = self.build_batting_average_events(Metrics.GameBattingAvgVsSeason(self.gameData))

		#Lead changes
		lead_changes = self.build_lead_change_events(Metrics.LeadChanges(self.gameData))

		#RBI percentage
		rbi_percentage = self.build_rbi_events(Metrics.RBIDistribution(self.gameData))

		# Home runs & grand slams
		home_runs = self.build_homerun_events(self.gameData)

		return (inning_runs + walked_runs + pitching_changes + game_batting_ave +
			lead_changes + rbi_percentage + home_runs)

	def build_inning_events(self, inning_metrics):
		""" Builds the events for highest scoring innings, returns a list of
			events. """
		event_type = SCORING_TEAM
		#Needed to look up team data and names
		team_names = { "away" : self.gameData['away_team_name'], "home" : self.gameData['home_team_name'] }
		team_designation = ('away','home')
		team_index = 0
		team_desc = ""
		events = []
		for team in team_designation:
			if int(inning_metrics[team+'_max']) < 1:
				continue
			#Runs the equation to determine the weight, dependant entirely on
			#constants at the start of the file
			weight = (float(inning_metrics[team+'_max']) * float(inning_metrics[team+'_inning']) / float(self.gameData['status']['inning']) * min(1, float(inning_metrics[team+'_max']) /
				INNING_RUN_PERCENT_THRESHOLD) * min(1, inning_metrics[team+'_value'] / INNING_RUN_TOTAL_THRESHOLD) * INNING_RUN_MAX_WEIGHT)
			log("weight: %s" % weight)
			#If they lose, inflict a weight penalty
			if self.winning_team != team:
				weight = weight / float(self.gameData['linescore']['r']['diff']) * INNING_RUN_LOSS_MULTIPLIER

			#Crazy stuff to print ordinal numbers

			runs = int(inning_metrics[team+'_inning'])
			k = runs%10
			ordinal_val = "%d%s"%(runs,"tsnrhtdd"[(runs/10%10!=1)*(k<4)*k::4])
			plural = ''
			if inning_metrics[team+'_value'] > 1:
				plural = 's'

			score_word = random.choice(['score','net', 'chalk up', 'tally', 'record'])
			run_word = 'run'
			if inning_metrics[team+'_value'] > 1:
				run_word+='s'
			points_word = random.choice([run_word, ''])
			inning_word = random.choice(['inning', ''])

			team_desc = "%s %s %s in the %s %s" % (score_word, inning_metrics[team+'_value'], points_word, ordinal_val,inning_word )
			short_desc = "%d in %s" % (int(inning_metrics[team+'_value']), ordinal_val )
			team_index += 1

			#adds the new a event to the event list
			events.append(Event(team_desc, weight, team_names[team], event_type, None, short_desc, self.winning_team == team))
			log("team_desc: %s" % team_desc)
			log("weight: %s" % weight)
			log("winz %s" % self.winning_team)

		return events

	def build_walks_events(self, walks_metrics):
		event_type = SUMMARIZING
		team_names = (self.gameData['away_team_name'], self.gameData['home_team_name'])
		team_designation = ('away','home')

		events = []
		for i in range(0, len(walks_metrics)):
			weight = NON_RBI_RUNS_WEIGHT_PER * walks_metrics[i]
			weight = min(weight, NON_RBI_RUNS_MAX_WEIGHT)
			blurb = random.choice(['had a defensive breakdown', 'couldn\'t get it going in the field', 'were weak defensively', 'lacked fielding'])
			#blurb = "had a defensive breakdown"
			short_blurb = "poor D"

			if weight > 0:
				events.append(Event(blurb, weight, team_names[i], event_type, None, short_blurb, team_designation[i] == self.winning_team))

				log("weight: %d" % weight)
				log("blurb: " + team_names[i] + " " + blurb)

			else:
				log("ignored event because weight 0")

		return events

	def build_pitching_change_events(self, pitching_metrics):
		event_type = PITCHING
		team_names = { "away" : self.gameData['away_team_name'], "home" : self.gameData['home_team_name'] }
		team_types = ["away", "home"]
		events = []

		for key in team_types:
			if pitching_metrics["first_sub_" + key] >= IMPRESSIVE_AMOUNT_OF_INNINGS_PITCHED:

				this_team_won = (self.winning_team == key)

				pitcher_name = pitching_metrics["name_" + key]
				strikeouts = pitching_metrics["strikeouts_" + key]
				innings = pitching_metrics["first_sub_" + key]

				plural = ''
				if int(strikeouts) > 1:
					plural = 's'

				pitcher_blurb = "%s threw %s strikeouts in %s innings" % (pitcher_name, strikeouts, innings)
				short_blurb = "%s %s K%s in %s" % (pitcher_name, strikeouts, plural, innings)
				event_weight = STAR_PITCHER_BASE_WEIGHT + (0.025 * int(strikeouts))

				events.append(Event(pitcher_blurb, event_weight, team_names[key], event_type, None, short_blurb, this_team_won))
				log("pitcher blrub: %s" % pitcher_blurb)
				log("event_weight: %s" % event_weight)
				log("win: %s" % this_team_won)

		return events

	def build_batting_average_events(self, batting_metrics):
		event_type = SUMMARIZING
		team_names = (self.gameData['away_team_name'], self.gameData['home_team_name'])
		team_types = ["away", "home"]
		events = []

		for i in range(0, len(team_types)):
			if abs(batting_metrics[i]) > TEAM_AVERAGE_INTERESTINGNESS_THRESHOLD:
				weight = TEAM_AVERAGE_DIFFERENCE_POINTS * batting_metrics[i]

				if weight > 0:
					blurb = random.choice(['were strong at the plate', 'were cleaning up at the plate', 'were characterized by strong at bats', 'shined offensively'])
					#blurb = "were strong at the plate"
					short_blurb = "played well"
				else:
					blurb = random.choice(['had an off night on offense', 'couldn\'t get in a groove at the plate', 'struggled at the plate', 'had a tough time at bat'])
					#blurb = "had an off night for offense"
					short_blurb = "played poorly"


				events.append(Event(blurb, weight, team_names[i], event_type, None, short_blurb, self.winning_team == team_types[i]))

				log("weight: %d" % weight)
				log("blurb: " + team_names[i] + " " + blurb)

		return events

	def build_lead_change_events(self, lead_metrics):
		event_type = SUMMARIZING
		team_names = { "away" : self.gameData['away_team_name'], "home" : self.gameData['home_team_name'] }
		team_types = ["away", "home"]
		events = []
		weight = 0
		blurb = ''

		if lead_metrics['change_count'] == 1:
			weight = LEAD_CHANGE_TAKE_AND_HOLD_WEIGHT
			inning = int(lead_metrics['first_change'])
			k = inning%10
			ordinal_val = "%d%s"%(inning,"tsnrhtdd"[(inning/10%10!=1)*(k<4)*k::4])
			classic_blurb = "took the lead in the %s and never gave it up" % (ordinal_val)
			blurb = random.choice([classic_blurb, 'were never behind', 'stayed on top the whole game', 'kept the lead out of reach'])
			short_blurb = "lead from %s" % (ordinal_val)
			events.append(Event(blurb, weight, team_names[self.winning_team], event_type, None, short_blurb, True))

		elif lead_metrics['change_count'] > LEAD_CHANGE_THRESHOLD:
			weight = LEAD_CHANGE_MAX_WEIGHT * float(lead_metrics['last_change']) / float(self.gameData['status']['inning'])
			final_inning = int(lead_metrics['last_change'])
			k = final_inning%10
			ordinal_val = "%d%s"%(final_inning,"tsnrhtdd"[(final_inning/10%10!=1)*(k<4)*k::4])
			classic_blurb = "battled for the lead and finally held it in the %s inning" % (ordinal_val)
			blurb = random.choice[classic_blurb,'fought a tough battle, but came out on top', 'won in a close one', 'really had to battle for the W']
			short_blurb = "lead from %s" % (ordinal_val)
			events.append(Event(blurb, weight, team_names[self.winning_team], event_type, None, short_blurb, True))

		log("weight: %d" % weight)
		log("blurb: " + team_names[self.winning_team] + " " + blurb)

		return events

	def build_rbi_events(self, rbi_metrics):
		event_type = SCORING_INDIVIDUAL
		team_names = { "away" : self.gameData['away_team_name'], "home" : self.gameData['home_team_name'] }
		team_types = ["away", "home"]
		events = []
		index = 0
		for team in rbi_metrics:
			if team:
				blurb = ''
				if len(team) > 1:
					players = [p[0] for p in team]
					rbis = map(int,[p[1] for p in team])
					s_rbis = sum(rbis)
					rbi_percent = map(float, [p[2] for p in team])
					blurb = ' and '.join(players)
					short_blurb = ', '.join(players)
					plural = ''
					if s_rbis > 1:
						plural = 's'
					action_word = random.choice(['hit', 'managed', 'scored', 'tallied', 'recorded'])
					blurb += " %s a combined %s RBI%s" % (action_word, s_rbis, plural)
					short_blurb += " %s RBI%s" % (s_rbis, plural)
					weight = sum(rbi_percent) / len(rbi_percent)
					event_owner = players
					events.append(Event(blurb,weight,team_names[team_types[index]], event_type, event_owner, short_blurb, self.winning_team == team_types[index]))
				else:
					print team
					player = team[0]
					plural = ''
					if player[1] > 1:
						plural = 's'

					# getting casual now
					if player[1] == 1:
						count = "an"
					else:
						count = player[1]
					action_word = random.choice(['hit', 'managed', 'scored', 'tallied', 'recorded'])
					blurb = "%s %s %s RBI%s" % (player[0], action_word, count, plural)
					short_blurb = "%s %s RBI%s" % (player[0], player[1], plural)
					weight = float(player[2])
					event_owner = player
					events.append(Event(blurb,weight,team_names[team_types[index]], event_type, event_owner, short_blurb, self.winning_team == team_types[index]))
			index+=1
		return events

	def build_homerun_events(self, game_data):
		event_type = SCORING_INDIVIDUAL
		team_names = { "away" : self.gameData['away_team_name'], "home" : self.gameData['home_team_name'] }
		team_codes = { game_data["away_code"] : "away", game_data["home_code"] : "home" }
		events = []
		blurb = ""
		weight = 0.0

		if 'home_runs' not in game_data:
			return events

		# check for grand slams
		game_home_runs = game_data['home_runs']['player']

		# make into list if not
		try:
			var = game_home_runs[0]['runners']
		except:
			game_home_runs = [game_home_runs]

		for hr in game_home_runs:
			if int(hr['runners']) == GRAND_SLAM_RUNNER_COUNT:
				action_word = random.choice(['hit', 'rocked', 'scored', 'recorded'])
				blurb = hr['last'] + " %s a grand slam" % (action_word)
				short_blurb = hr['last'] + " Grand Slam"
				event_owner = hr['last']
				team_name = team_names[team_codes[hr['team_code'].encode("ascii")]]
				weight = HOME_RUN_WEIGHT + float(hr['runners']) * HOME_RUN_RUNNER_BONUS
				events.append(Event(blurb, weight, team_name, event_type, event_owner, short_blurb, team_codes[hr['team_code']] == self.winning_team))

		# report player home runs
		max_hr = 0
		max_hr_name = None
		for hr in game_home_runs:
			rbi = int(hr['runners']) + 1

			if(rbi == 4):
				continue

			if rbi == 1:
				hr_noun = "solo home run"
			else:
				hr_noun = "%d run homer" % rbi

			action_word = random.choice(['hit', 'rocked', 'scored', 'recorded'])
			blurb = hr['last'] + " %s a %s" % (action_word, hr_noun)
			short_blurb = hr['last'] + " HR"
			event_owner = hr['last']
			team_name = team_names[team_codes[hr['team_code'].encode("ascii")]]
			weight = HOME_RUN_WEIGHT + int(hr['runners']) * HOME_RUN_RUNNER_BONUS
			events.append(Event(blurb, weight, team_name, event_type, event_owner, short_blurb, team_codes[hr['team_code']] == self.winning_team))

		return events

