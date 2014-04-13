import random

# interest thresholds
ERROR_INTEREST_THRESHOLD = 3
GRAND_SLAM_RUNNER_COUNT = 3
NORMAL_INNING_COUNT = 9

# score values
DO_NOT_MENTION_VALUE = 0
NO_HITTER_VALUE = 10
MVP_BATTER_VALUE = 2
WINNING_PITCHER_VALUE = 4
PERFECT_GAME_VALUE = 10

# arbitrary ranking constants
BATTING_HOMERUN_MULTIPLIER = 0.4
BATTING_BB_MULTIPLIER = .01
BATTING_RBI_MULTIPLIER = 7.0

# action verbs
DEFEATED_STRONG = ['%s destroyed %s','%s trounced %s','%s eviscerated %s','%s gave %s what for']
DEFEATED_NORMAL = ['%s defeated %s']
DEFEATED_NARROW = ['%s narrowly beat %s']

STRONG_THRESHOLD = 4
NARROW_THRESHOLD = 1

class Summarize:
	@staticmethod
	def get_winner(game_data):
		runs_scored = game_data['linescore']['r']
		if int(runs_scored['home']) > int(runs_scored['away']):
			winner = game_data['home_team_name']
			winner_score = int(runs_scored['home'])
			loser = game_data['away_team_name']
			loser_score = int(runs_scored['away'])
		else:
			winner = game_data['away_team_name']
			winner_score = int(runs_scored['away'])
			loser = game_data['home_team_name']
			loser_score = int(runs_scored['home'])

		# check for extra innings
		inning_count = int(game_data['status']['inning'])
		extra_innings = ""
		if inning_count > NORMAL_INNING_COUNT:
			extra_innings = " in %d innings" % inning_count

		# pick an action verb
		if winner_score - loser_score <= NARROW_THRESHOLD:
			defeat_string = random.choice(DEFEATED_NARROW) % (winner, loser)
		elif winner_score - loser_score <= STRONG_THRESHOLD:
			defeat_string = random.choice(DEFEATED_NORMAL) % (winner, loser)
		else:
			defeat_string = random.choice(DEFEATED_STRONG) % (winner, loser)


		return "%s %d - %d%s. " % (defeat_string, winner_score, loser_score, extra_innings)

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

		if 'home_runs' not in game_data:
			return (DO_NOT_MENTION_VALUE, "")

		# check for grand slams
		game_home_runs = game_data['home_runs']['player']

		# make into list if not
		try:
			var = game_home_runs[0]['runners']
		except:
			game_home_runs = [game_home_runs]

		for hr in game_home_runs:
			if int(hr['runners']) == GRAND_SLAM_RUNNER_COUNT:
				home_run_summary_text = hr['last'] + " hit a grand slam."
				return (6, home_run_summary_text)

		# report player home runs
		max_hr = 0
		max_hr_name = None
		for hr in game_home_runs:
			if hr['runners'] > max_hr:
				max_hr = hr['runners']
				max_hr_name = hr['last']

		rbi = int(max_hr) + 1

		if rbi > 1:
			rbi_text = "%d shot" % rbi
		else:
			rbi_text = "solo"
		home_run_summary_text = max_hr_name + " hit a %s home run." % rbi_text
		return (rbi, home_run_summary_text)

	@staticmethod
	def get_no_hitter(game_data):
		no_hitter_text = ""
		for team in game_data['boxscore']['pitching']:
			if int(team['h']) == 0:
				pitchers = team['pitcher']
				if type(pitchers) is not list:
					if len(no_hitter_text) == 0:
						no_hitter_text = pitchers['name'].split(', ')[0]
					else:
						no_hitter_text = no_hitter_text + " and " + pitchers['name']
				else:
					if len(no_hitter_text) == 0:
						if team['team_flag'] == 'away':
							no_hitter_text = game_data['boxscore']['away_fname']
						else:
							no_hitter_text = game_data['boxscore']['home_sname']
					else:
						if team['team_flag'] == 'away':
							no_hitter_text = no_hitter_text + " and " + game_data['boxscore']['away_fname']
						else:
							no_hitter_text = no_hitter_text + " and " + game_data['boxscore']['home_sname']
			if len(no_hitter_text) > 0:
				no_hitter_text += " pitched a no hitter."
				return (NO_HITTER_VALUE, no_hitter_text)
			else:
				return (DO_NOT_MENTION_VALUE, no_hitter_text)

	@staticmethod
	def get_perfect_game(game_data):
		perfect_game_text = ""
		for team_pitching in game_data['boxscore']['pitching']:
			for team_batting in game_data['boxscore']['batting']:
				if team_pitching['team_flag'] != team_batting['team_flag']:
					if int(team_batting['h']) == 0 and int(team_batting['lob']) == 0 and int(team_batting['r']) == 0:
						pitchers = team_pitching['pitcher']
						if type(pitchers) is not list:
							perfect_game_text = pitchers['name'].split(', ')[0]
						else:
							if team_pitching['team_flag'] == 'away':
								perfect_game_text = game_data['boxscore']['away_fname']
							else:
								perfect_game_text = game_data['boxscore']['home_sname']
		if len(perfect_game_text) > 0:
			perfect_game_text += " pitched a perfect game!"
			return (PERFECT_GAME_VALUE, perfect_game_text)
		else:
			return (DO_NOT_MENTION_VALUE, perfect_game_text)


	@staticmethod
	def get_mvp_batter(game_data):
		boxscore = game_data['boxscore']
		mvp = None
		mvp_score = 0
		mvp_tit_for_tat = None
		rbis = None
		total_runs = int(game_data['linescore']['r']['home']) + int(game_data['linescore']['r']['away'])

		for team in boxscore['batting']:
			for batter in team['batter']:
				# compare this game's performance to their batting average for the season
				# used as a multiplier for mvp_score
				if float(batter['ab']) > 0 and float(batter['avg']) > 0:
					mvp_multiplier = (float(batter['h']) / float(batter['ab']) ) / float(batter['avg'])

					# arbitrary ranking of batting
					rbi_score = 0
					if int(batter['rbi']) > 0:
						rbi_score = BATTING_RBI_MULTIPLIER*(max(.33,float(batter['rbi'])/total_runs))
					cur_score = int(batter['h']) + rbi_score + BATTING_HOMERUN_MULTIPLIER*int(batter['hr']) + BATTING_BB_MULTIPLIER*int(batter['bb'])

					cur_score = cur_score * mvp_multiplier

					if cur_score > mvp_score:
						mvp_score = cur_score
						mvp = batter['name_display_first_last'].split(' ')[1]
						mvp_tit_for_tat = (batter['h'], batter['ab'])
						rbis = int(batter['rbi'])
		mvp_batter_text = "%s went %s for %s." % (mvp, mvp_tit_for_tat[0], mvp_tit_for_tat[1])
		if rbis > 0:
			mvp_batter_text = mvp_batter_text[:-1] + " with %s RBIs." % (rbis)
			if rbis < 2:
				mvp_batter_text = mvp_batter_text[:-2] + "."
		return (MVP_BATTER_VALUE, mvp_batter_text)

	@staticmethod
	def get_winning_pitcher(game_data):
		for team in game_data['boxscore']['pitching']:
			pitchers = team['pitcher']
			if type(pitchers) is not list:
				if 'win' in pitchers.keys() and pitchers['win'] == 'true':
					multiple_ks = ''
					if int(pitchers['so']) > 1:
						multiple_ks = 's'
					return (WINNING_PITCHER_VALUE, "WP, %s had %s K%s with a %s ERA." % (pitchers['name_display_first_last'].split(' ')[1], pitchers['so'], multiple_ks, pitchers['era']))
			else:
				for pitcher in pitchers:
					if 'win' in pitcher.keys() and pitcher['win'] == 'true':
						multiple_ks = ''
						if int(pitcher['so']) > 1:
							multiple_ks = 's'
						return (WINNING_PITCHER_VALUE, "WP, %s had %s K%s with a %s ERA." % (pitcher['name_display_first_last'].split(' ')[1], pitcher['so'], multiple_ks, pitcher['era']))
		return (DO_NOT_MENTION_VALUE, "")

