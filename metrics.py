class Metrics:
	@staticmethod
	def InningRunsTotalRuns(game_data):
		linescore, home_runs, away_runs, home_inning_runs, away_inning_runs = game_data['boxscore']['linescore'], 
			float(game_data['boxscore']['home_team_runs']), float(game_data['boxscore']['away_team_runs']), [], []
		for inning in linescore['inning_line_score']:
			for key in inning.keys():
				if key == 'home':
					home_inning_runs.append(float(inning[key])/home_runs)
				elif key == 'away':
					away_inning_runs.append(float(inning[key])/away_runs)
		away_max, home_max = (max(away_inning_runs), away_inning_runs.index(max(away_inning_runs))), (max(home_inning_runs), home_inning_runs.index(max(home_inning_runs)))
		away_avg, home_avg = sum(away_inning_runs)/len(away_inning_runs), sum(home_inning_runs)/len(home_inning_runs)
		return ((away_max, away_avg), (home_max, home_avg))

	@staticmethod
	def WalksAndBalks(game_data):

	@staticmethod
	def PitchingChangeDistribution(game_data):

	@staticmethod
	def GameBattingAvgVsSeason(game_data):

	@staticmethod
	def LeadChanges(game_data):

	@staticmethod
	def RBIDistribution(game_data):
