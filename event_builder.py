#Creates the events based on data from metrics

from metrics import *

def build_events(gameData):
	if (int(gameData['linescore']['r']['home']) > int(gameData['linescore']['r']['away']) ):
		winning_team = "home"
	else:
		winning_team = "away"

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

def build_inning_events(inning_metrics):

def build_walks_events(walks_metrics):

def build_pitching_change_events(pitching_metrics):

def build_lead_change_events(lead_metrics):

def build_rbi_events(rbi_metrics):

