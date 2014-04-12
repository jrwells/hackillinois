class Metrics:
	@staticmethod
	def InningRunsTotalRuns(game_data):

	@staticmethod
	def WalksAndBalks(game_data):
		""" Gets quantity of runs earned not by RBI (walks/balks/errors) """
		runs_scored = game_data['linescore']['r']
		runs_scored_away = runs_scored[1]
		runs_scored_home = runs_scored[0]

		for entry in game_data['boxscore']['batting']:
			if entry['team_flag'] == "home":
				rbi_home = entry['rbi']
			else:
				rbi_away = entry['rbi']

		return (runs_scored_away - rbi_away, runs_scored_home - rbi_home)

	@staticmethod
	def PitchingChangeDistribution(game_data):

	@staticmethod
	def GameBattingAvgVsSeason(game_data):

	@staticmethod
	def LeadChanges(game_data):

	@staticmethod
	def RBIDistribution(game_data):
