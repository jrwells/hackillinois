ERROR_INTEREST_THRESHOLD = 3

class summarize:
	def get_winner(gameData):
		runs_scored = gameData['linescore']['r']

class Summarize:

	@staticmethod
	def get_winner(game_data):
		runs_scored = game_data['linescore']['r']
		if int(runs_scored['home']) > int(runs_scored['away']):
			winner = game_data['home_team_name']
			winner_score = runs_scored['home']
			loser = game_data['away_team_name']
			loser_score = runs_scored['away']
		else:
			winner = game_data['away_team_name']
			winner_score = runs_scored['away']
			loser = game_data['home_team_name']
			loser_score = runs_scored['home']

		return "%s defeated %s %s - %s. " % (winner, loser, winner_score, loser_score)

	@staticmethod
	def get_errors(game_data):
		error_count = game_data['linescore']['e']
		error_summary_text = None

		if int(error_count['home']) > ERROR_INTEREST_THRESHOLD:
			error_summary_text = game_data['home_team_name'] + " had " + error_count['home'] + " errors"

		if int(error_count['away']) > ERROR_INTEREST_THRESHOLD:
			if error_summary_text:
				error_summary_text = error_summary_text + " and "
				end = ""

			else:
				error_summary_text = ""
				end = " errors"

			error_summary_text = error_summary_text + game_data['away_team_name'] + " had " + error_count['away'] + end

		if error_summary_text:
			score = max(int(error_count['home']), int(error_count['away']))
			error_summary_text = error_summary_text + "."

		else:
			score = 0

		return (score, error_summary_text)
