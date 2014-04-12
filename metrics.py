class Metrics:
	@staticmethod
	def InningRunsTotalRuns(game_data):

	@staticmethod
	def WalksAndBalks(game_data):

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

	@staticmethod
	def RBIDistribution(game_data):
