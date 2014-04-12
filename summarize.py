# interest thresholds
ERROR_INTEREST_THRESHOLD = 3
GRAND_SLAM_RUNNER_COUNT = 3

# score values
DO_NOT_MENTION_VALUE = 0
NO_HITTER_VALUE = 10

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
			score = DO_NOT_MENTION_VALUE

		return (score, error_summary_text)

	@staticmethod
	def get_home_runs(game_data):
		home_run_summary_text = None

		# check for grand slams
		game_home_runs = game_data['home_runs']['player']

		for hr in game_home_runs:
			if hr['runners'] == GRAND_SLAM_RUNNER_COUNT:
				home_run_summary_text = hr['last'] + " hit grand slam."
				return (6, home_run_summary_text)

		# report player home runs
		max_hr = 0
		max_hr_name = None
		for hr in game_home_runs:
			if hr['runners'] > max_hr:
				max_hr = hr['runners']
				max_hr_name = hr['last']

		home_run_summary_text = max_hr_name + " hit home run."
		return (4, home_run_summary_text)

	def fetch_boxscore(game_data):
		root_dir = game_data['game_data_directory'] + '/boxscore.json'
		boxscore = requests.get(root_dir).json()
		self.boxscore = boxscore['data']['boxscore']

	@staticmethod
	def get_no_hitter(game_data):
		no_hitter_text = ""
		if self.boxscore:
			for team in self.boxscore['pitching']:
				if int(team['h']) == 0:
					pitchers = team['pitcher']
					if len(pitchers) == 1:
						if len(no_hitter_text) == 0:
							no_hitter_text = pitchers[0]['name']
						else:
							no_hitter_text = no_hitter_text + " and " pitchers[0]['name']
					else:
						if len(no_hitter_text):
							if team['team_flag'] == 'away':
								no_hitter_text = self.boxscore['away_fname']
							else:
								no_hitter_text = self.boxscore['home_sname']
						else:
							if team['team_flag'] == 'away':
								no_hitter_text = no_hitter_text + " and " + self.boxscore['away_fname']
							else:
								no_hitter_text = no_hitter_text + " and " + self.boxscore['home_sname']
			if len(no_hitter_text) > 0:
				no_hitter_text += " had no hitter."
				return (NO_HITTER_VALUE, no_hitter_text
			else
				return (DO_NOT_MENTION_VALUE, no_hitter_text)
