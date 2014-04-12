class Metrics:
	@staticmethod
	def InningRunsTotalRuns(game_data):
		linescore, home_runs, away_runs, inning_runs = game_data['boxscore']['linescore'], float(game_data['boxscore']['home_team_runs']), float(game_data['boxscore']['away_team_runs']), []
		for inning in linescore['inning_line_score']:
			ratios = []
			for key in inning.keys():
				if key == 'home':
					ratios[1] = float(inning[key])/home_runs
				elif key == 'away':
					ratios[0] = float(inning[key])/away_runs
			inning_runs.append(ratios)
		return inning_runs

	@staticmethod
	def WalksAndBalks(game_data):
		""" Gets quantity of runs earned not by RBI (walks/balks/errors) """

		runs_scored = game_data['linescore']['r']
		runs_scored_away = runs_scored[1]
		runs_scored_home = runs_scored[0]

		for entry in game_data['boxscore']['batting']:
			if entry['team_flag'] == 'home':
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
		""" Count the number of times a team takes the lead """

		change_count = 0
		away_score, home_score = 0, 0
		away_winning, home_winning = False, False
		for i in game_data['linescore']['inning']:
			away_score += int(i['away'])
			home_score += int(i['home'])

			if (away_score > home_score) and not away_winning:
				away_winning = True
				home_winning = False
				change_count += 1

			elif (home_score > away_score) and not home_winning:
				home_winning = True
				away_winning = False
				change_count += 1

			else:
				home_winning, away_winning = False, False

		return change_count

	@staticmethod
	def RBIDistribution(game_data):
