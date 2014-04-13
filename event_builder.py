#Creates the events based on data from metrics
from event import *

#Arbitrary Constants
INNING_RUN_PERCENT_THRESHOLD = .4
INNING_RUN_TOTAL_THRESHOLD = 3
INNING_RUN_LOSS_MULTIPLIER = .75
IMPRESSIVE_AMOUNT_OF_INNINGS_PITCHED = 8

# Arbitrary Weights
INNING_RUN_MAX_WEIGHT = .7
STAR_PITCHER_BASE_WEIGHT = .5

from metrics import *
from summary_builder import *
from event import *
class Event_builder:
	def build_events(self, gameData):
		if (int(gameData['linescore']['r']['home']) > int(gameData['linescore']['r']['away']) ):
			self.winning_team = "home"
		else:
			self.winning_team = "away"

		self.gameData = gameData

		#inning runs total runs
		inning_runs = Metrics.InningRunsTotalRuns(gameData)

		#walked in runs
		walked_runs = Metrics.WalksAndBalks(gameData)

		#pitching changes
		pitching_changes = Metrics.PitchingChangeDistribution(gameData)

		#Game batting ave
		game_batting_ave = Metrics.GameBattingAvgVsSeason(gameData)

		#Lead changes
		lead_changes = Metrics.LeadChanges(gameData)

		#RBI percentage
		rbi_percentage = Metrics.RBIDistribution(gameData)

		return (inning_runs + walked_runs + pitching_changes + game_batting_ave +
			lead_changes + rbi_percentage)

	def build_inning_events(self, inning_metrics):
		""" Builds the events for highest scoring innings, returns a list of
			events. """
		#Needed to look up team data and names
		team_names = (self.gameData['away_team_name'], self.gameData['home_team_name'])
		team_designation = ('away','home')
		team_index = 0
		team_desc = ''
		events = []
		for team in inning_metrics:
			#Runs the equation to determine the weight, dependant entirely on
			#constants at the start of the file
			weight = float(team[team_designation[team_index]+'_max']) * float(team[team_designation[team_index]+'_inning']) / float(self.gameData['status']['inning']) * min(1, INNING_RUN_PERCENT_THRESHOLD / float(team[team_designation[team_index]+'_max'])) * min(1, INNING_RUN_TOTAL_THRESHOLD / team[team_designation[team_index]+'_value']) * INNING_RUN_MAX_WEIGHT
			#If they lose, inflict a weight penalty
			if self.winning_team != team_designation[team_index]:
				weight = weight / float(self.gameData['linescore']['r']['diff']) * INNING_RUN_LOSS_MULTIPLIER

			#Crazy stuff to print ordinal numbers
			runs = int(team[team_designation[team_index]+'_value'])
			k = runs%10
			team_desc = "scored %s runs in the %s%s inning" % (team_names[team_index), runs, "%d%s"%(runs,"tsnrhtdd"[(runs/10%10!=1)*(k<4)*k::4]))
			team_index += 1

			#adds the new a event to the event list
			events.append(event(team_desc, weight,self.winning_team))

		return events

	def build_walks_events(self, walks_metrics):
		None

	def build_pitching_change_events(self, pitching_metrics):
		team_types = ["away", "home"]
		events = []

		for key in team_types:
			if pitching_metrics["first_sub_" + key] >= IMPRESSIVE_AMOUNT_OF_INNINGS_PITCHED:

				this_team_won = (self.winning_team == key)

				pitcher_name = pitching_metrics["name_" + key]
				strikeouts = pitching_metrics["strikeouts_" + key]
				innings = pitching_metrics["first_sub_" + key]

				pitcher_blurb = "%s pitched %s strikeouts in %s innings." % (pitcher_name, strikeouts, innings)

				events.append(event(pitcher_blurb, STAR_PITCHER_BASE_WEIGHT, this_team_won))

		return events

	def build_lead_change_events(self, lead_metrics):

	def build_rbi_events(self, rbi_metrics):

