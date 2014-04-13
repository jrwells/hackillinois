#Creates the events based on data from metrics

#Arbitrary Constants
INNING_RUN_PERCENT_THRESHOLD = .4
INNING_RUN_TOTAL_THRESHOLD = 3
INNING_RUN_MAX_WEIGHT = .7
INNING_RUN_LOSS_MULTIPLIER = .75

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
		team_designation = ('away','home')
		team_index = 0
		team_weights = [None,None]
		team_desc = ['','']
		scores = (int(self.gameData['linescore']['r']['away']), int(self.gameData['linescore']['r']['home']) )
		for team in inning_metrics:
			weight = float(team[0]) * float(team[1]) / float(self.gameData['status']['inning']) * min(1, INNING_RUN_PERCENT_THRESHOLD / float(team[0])) * min(1, INNING_RUN_TOTAL_THRESHOLD / float(self.gameData['linescore']['inning'][int(team[1])][team_designation[team_index]])) * INNING_RUN_MAX_WEIGHT
			if self.winning_team != team_designation[team_index]:
				weight = weight / float(self.gameData['linescore']['r']['diff']) * INNING_RUN_LOSS_MULTIPLIER


			team_weights[team_index] = weight
			team_index += 1
	def build_walks_events(self, walks_metrics):

	def build_pitching_change_events(self, pitching_metrics):

	def build_lead_change_events(self, lead_metrics):

	def build_rbi_events(self, rbi_metrics):

