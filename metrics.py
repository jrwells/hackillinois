#Arbitrary Constants
RBI_THRESHOLD_PERCENT = .33

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
			if entry['team_flag'] == "home":
				rbi_home = entry['rbi']
			else:
				rbi_away = entry['rbi']

		return (runs_scored_away - rbi_away, runs_scored_home - rbi_home)

	@staticmethod
	def PitchingChangeDistribution(game_data):


	@staticmethod
	def GameBattingAvgVsSeason(game_data):
		""" Returns a tuple (Away,Home) of the average difference between players season
		    batting average and their batting average in the current game """

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

	@staticmethod
	def RBIDistribution(game_data):
		""" Returns a list of players for each team with a percentage of RBIs for their team
			over RBI_THRESHOLD_PERCENT. Returns a tuple of lists of tuples: 
			([(<LAST NAME>, <RBIs>), (<LAST NAME>, <RBIs>)],[(<LAST NAME>, <RBIs>), (<LAST NAME>, <RBIs>)]) """

		boxscore = game_data['boxscore']
		# index for team
		team_index = 1
		# Away @ Home
		rbi_players = ([], [])
		for team in boxscore['batting']:
			# The threshold determined by RBI_THRESHOLD_PERCENT
			rbi_threshold = float(team['rbi']) * RBI_THRESHOLD_PERCENT
			for batter in team['batter']:
				batter_rbi = int(batter['rbi'])
				# if the batter rbi is high enough, create a tuple ( <LAST NAME>, <RBIs> ) and add it to the list
				if batter_rbi >= rbi_threshold:
					rbi_players[team_index].append( (batter['name_display_first_last'].split(' ')[-1], batter_rbi) )
			# Change the team index
			team_index = 0

		return rbi_players

