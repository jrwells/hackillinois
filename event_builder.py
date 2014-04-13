# Creates the events based on data from metrics
from event import *
from debug import log

# Arbitrary Constants
INNING_RUN_PERCENT_THRESHOLD = .4
INNING_RUN_TOTAL_THRESHOLD = 3
INNING_RUN_LOSS_MULTIPLIER = .75
IMPRESSIVE_AMOUNT_OF_INNINGS_PITCHED = 8
TEAM_AVERAGE_INTERESTINGNESS_THRESHOLD = 0.05
LEAD_CHANGE_THRESHOLD = 3

# Arbitrary Weights
INNING_RUN_MAX_WEIGHT = .7
STAR_PITCHER_BASE_WEIGHT = 0.4
NON_RBI_RUNS_MAX_WEIGHT = -0.6
NON_RBI_RUNS_WEIGHT_PER = -0.08
TEAM_AVERAGE_DIFFERENCE_POINTS = 0.1
LEAD_CHANGE_TAKE_AND_HOLD_WEIGHT = 0.2
LEAD_CHANGE_MAX_WEIGHT = 0.5


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
		print inning_runs

		#walked in runs
		walked_runs = self.build_walks_events(Metrics.WalksAndBalks(self.gameData))
		print walked_runs

		#pitching changes
		pitching_changes = self.build_pitching_change_events(Metrics.PitchingChangeDistribution(self.gameData))
		print pitching_changes

		#Game batting ave
		game_batting_ave = self.build_batting_average_events(Metrics.GameBattingAvgVsSeason(self.gameData))
		print game_batting_ave

		#Lead changes
		lead_changes = self.build_lead_change_events(Metrics.LeadChanges(self.gameData))
		print lead_changes

		#RBI percentage
		rbi_percentage = self.build_rbi_events(Metrics.RBIDistribution(self.gameData))
		print rbi_percentage

		return (inning_runs + walked_runs + pitching_changes + game_batting_ave +
			lead_changes + rbi_percentage)

	def build_inning_events(self, inning_metrics):
		""" Builds the events for highest scoring innings, returns a list of
			events. """
		#Needed to look up team data and names
		team_names = { "away" : self.gameData['away_team_name'], "home" : self.gameData['home_team_name'] }
		team_designation = ('away','home')
		team_index = 0
		team_desc = ""
		events = []
		for team in team_designation:
			#Runs the equation to determine the weight, dependant entirely on
			#constants at the start of the file
			weight = float(inning_metrics[team+'_max']) * float(inning_metrics[team+'_inning']) / float(self.gameData['status']['inning']) * min(1, float(inning_metrics[team+'_max']) / INNING_RUN_PERCENT_THRESHOLD) * min(1, inning_metrics[team+'_value'] / INNING_RUN_TOTAL_THRESHOLD) * INNING_RUN_MAX_WEIGHT
			log("weight: %s" % weight)
			#If they lose, inflict a weight penalty
			if self.winning_team != team:
				weight = weight / float(self.gameData['linescore']['r']['diff']) * INNING_RUN_LOSS_MULTIPLIER

			#Crazy stuff to print ordinal numbers

			runs = int(inning_metrics[team+'_inning'])
			k = runs%10
			ordinal_val = "%d%s"%(runs,"tsnrhtdd"[(runs/10%10!=1)*(k<4)*k::4])
			team_desc = "scored %s runs in the %s inning" % (inning_metrics[team+'_value'], ordinal_val )
			team_index += 1

			#adds the new a event to the event list
			events.append(Event(team_desc, weight, team_names[team], self.winning_team == team))
			log("team_desc: %s" % team_desc)
			log("weight: %s" % weight)
			log("winz %s" % self.winning_team)

		return events

	def build_walks_events(self, walks_metrics):
		team_names = (self.gameData['away_team_name'], self.gameData['home_team_name'])
		team_designation = ('away','home')

		events = []
		for i in range(0, len(walks_metrics)):
			weight = NON_RBI_RUNS_WEIGHT_PER * walks_metrics[i]
			weight = min(weight, NON_RBI_RUNS_MAX_WEIGHT)
			blurb = "had a defensive breakdown."

			if weight > 0:
				events.append(Event(blurb, weight, team_names[i], team_designation[i] == self.winning_team))

				log("weight: %d" % weight)
				log("blurb: " + team_names[i] + " " + blurb)

			else:
				log("ignored event because weight 0")

		return events

	def build_pitching_change_events(self, pitching_metrics):
		team_names = { "away" : self.gameData['away_team_name'], "home" : self.gameData['home_team_name'] }
		team_types = ["away", "home"]
		events = []

		for key in team_types:
			if pitching_metrics["first_sub_" + key] >= IMPRESSIVE_AMOUNT_OF_INNINGS_PITCHED:

				this_team_won = (self.winning_team == key)

				pitcher_name = pitching_metrics["name_" + key]
				strikeouts = pitching_metrics["strikeouts_" + key]
				innings = pitching_metrics["first_sub_" + key]

				pitcher_blurb = "%s pitched %s strikeouts in %s innings." % (pitcher_name, strikeouts, innings)
				event_weight = STAR_PITCHER_BASE_WEIGHT + (0.025 * int(strikeouts))

				events.append(Event(pitcher_blurb, event_weight, team_names[key], this_team_won))
				log("pitcher blrub: %s" % pitcher_blurb)
				log("event_weight: %s" % event_weight)
				log("win: %s" % this_team_won)

		return events

	def build_batting_average_events(self, batting_metrics):
		team_names = (self.gameData['away_team_name'], self.gameData['home_team_name'])
		team_types = ["away", "home"]
		events = []

		for i in range(0, len(team_types)):
			if abs(batting_metrics[i]) > TEAM_AVERAGE_INTERESTINGNESS_THRESHOLD:
				weight = TEAM_AVERAGE_DIFFERENCE_POINTS * batting_metrics[i]

				if weight > 0:
					blurb = "were hot at the plate."
				else:
					blurb = "had a cold offense."

				events.append(Event(blurb, weight, team_names[i], self.winning_team == team_types[i]))

				log("weight: %d" % weight)
				log("blurb: " + team_names[i] + " " + blurb)

		return events

	def build_lead_change_events(self, lead_metrics):
		team_names = { "away" : self.gameData['away_team_name'], "home" : self.gameData['home_team_name'] }
		team_types = ["away", "home"]
		events = []
		weight = 0
		blurb = ''

		if lead_metrics['change_count'] == 1:
			weight = LEAD_CHANGE_TAKE_AND_HOLD_WEIGHT
			blurb = "took the lead and never gave it up"
			events.append(Event(blurb, weight, team_names[self.winning_team], True))

		elif lead_metrics['change_count'] > LEAD_CHANGE_THRESHOLD:
			weight = LEAD_CHANGE_MAX_WEIGHT * float(lead_metrics['last_change']) / float(self.gameData['status']['inning'])
			final_inning = int(lead_metrics['last_change'])
			k = final_inning%10
			ordinal_val = "%d%s"%(final_inning,"tsnrhtdd"[(final_inning/10%10!=1)*(k<4)*k::4])
			blurb = "battled for the lead and finally held it in the %s inning" % (ordinal_val)
			events.append(Event(blurb, weight, team_names[self.winning_team], True))

		log("weight: %d" % weight)
		log("blurb: " + team_names[self.winning_team] + " " + blurb)

		return events

	def build_rbi_events(self, rbi_metrics):
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
					rbi_percent = map(float, [p[2] for p in team])
					blurb = ','.join(players)
					blurb += " hit a combined %s RBIs" % (sum(rbis))
					weight = sum(rbi_percent) / len(rbi_percent)
					events.append(Event(blurb,weight,team_names[team_types[index]], self.winning_team == team_names[team_types[index]]))
				else:
					print team
					player = team[0]
					blurb = "%s hit %s RBIs" % (player[0], player[1])
					weight = float(player[2])
					events.append(Event(blurb,weight,team_names[team_types[index]], self.winning_team == team_names[team_types[index]]))
		return events



