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

	# Returns a tuple (Away,Home) of the average difference between players season
	# batting average and their batting average in the current game
	@staticmethod
	def GameBattingAvgVsSeason(game_data):
		boxscore = game_data['boxscore']
		#index for team
		team_index = 1
		#Away @ Home
		average_difference = (0, 0)
		for team in boxscore['batting']:
			#count players on team, who had at bats
			count = 0
			for batter in team['batter']:
				#calculate the diff between current and season batting average
				hits = float(batter['h'])
				at_bats = float(batter['ab'])
				#only calculate for players who batted 
				if at_bats > 0:
					game_average = hits / at_bats
					season_average = float(batter['avg'])
					average_difference[team_index] += game_average - season_average
					count += 1
			#calculate the average
			average_difference[team_index] = float(average_difference[team_index]) / float(count)
			#change the team index
			team_index = 0

		return average_difference

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
