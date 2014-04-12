#Creates the events based on data from metrics

#Arbitrary Constants
INNING_RUN_PERCENT_THRESHOLD = .4

from metrics import *
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

	def build_inning_events(self, inning_metrics):
		for team in inning_metrics:
			if team[0] > INNING_RUN_PERCENT_THRESHOLD and

	def build_walks_events(self, walks_metrics):

	def build_pitching_change_events(self, pitching_metrics):

	def build_lead_change_events(self, lead_metrics):

	def build_rbi_events(self, rbi_metrics):

