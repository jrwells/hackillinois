class summarize:
	def get_winner(gameData):
		runs_scored = gameData['linescore']['r']
		if int(runs_scored['home']) > int(runs_scored['away']):
			winner = gameData['home_team_name']
			winner_score = runs_scored['home']
			loser = gameData['away_team_name']
			loser_score = runs_scored['away']
		else:
			winner = gameData['away_team_name']
			winner_score = runs_scored['away']
			loser = gameData['home_team_name']
			loser_score = runs_scored['home']

		return "%s defeated %s %d - %d" % (winner, loser, winner_score, loser_score)


