import urllib2, xml.etree.ElementTree as ET

#Arbitrary Constants
RBI_THRESHOLD_PERCENT = .33

class Metrics:
	@staticmethod
	def InningRunsTotalRuns(game_data):
		""" Gets the innings where the most proportion of runs """

		linescore = game_data['boxscore']['linescore']
		home_runs, away_runs, home_inning_runs, away_inning_runs = float(linescore['home_team_runs']), float(linescore['away_team_runs']), [], []
		if home_runs == 0:
			home_runs = 1
		if away_runs == 0:
			away_runs = 1

		for inning in linescore['inning_line_score']:
			if inning['home'] == 'x':
				home_inning_runs.append(0.0)
			else:
				home_inning_runs.append(float(inning['home'])/home_runs)
			away_inning_runs.append(float(inning['away'])/away_runs)

		away_max, home_max = max(away_inning_runs), max(home_inning_runs)
		away_tuple, home_tuple = (away_max, away_inning_runs.index(away_max) + 1), (home_max, home_inning_runs.index(home_max) + 1)
		return (away_tuple, home_tuple)

	@staticmethod
	def WalksAndBalks(game_data):
		""" Gets quantity of runs earned not by RBI (walks/balks/errors) """

		runs_scored = game_data['linescore']['r']
		runs_scored_away = runs_scored['away']
		runs_scored_home = runs_scored['home']

		for entry in game_data['boxscore']['batting']:
			if entry['team_flag'] == 'home':
				rbi_home = entry['rbi']
			else:
				rbi_away = entry['rbi']

		return (int(runs_scored_away) - int(rbi_away), int(runs_scored_home) - int(rbi_home))

	@staticmethod
	def GetEventLog(game_data):
		""" Return the XML event log for a game as a string """

		eventlog_url = "http://gd2.mlb.com" + game_data['game_data_directory'] + "/eventLog.xml"
		return urllib2.urlopen(eventlog_url).read()

	@staticmethod
	def PitchingChangeDistribution(game_data):
		""" Returns a tuple containing a tuple for each team:
		    (inning of first change, number of changes) """

		first_away, first_home = None, None
		total_away, total_home = 0, 0

		event_log = Metrics.GetEventLog(game_data)
		root = ET.fromstring(event_log)

		for team in root.findall("team"):
			for event in team.findall("event"):

				# check for pitching change
				if "Pitching Change" in event.get("description"):
					# update home or away accordingly
					if team.get("home_team") == "false":
						# set first if not yet set
						if first_away == None:
							first_away = int(event.get("inning"))
						total_away += 1

					else:
						# set first if not yet set
						if first_home == None:
							first_home = int(event.get("inning"))
						total_home += 1

		away_result = (first_away, total_away)
		home_result = (first_home, total_home)

		return (away_result, home_result)


	@staticmethod
	def GameBattingAvgVsSeason(game_data):
		""" Returns a tuple (Away,Home) of the average difference between players season
		    batting average and their batting average in the current game """

		boxscore = game_data['boxscore']
		#index for team
		team_index = 1
		#Away @ Home
		average_difference = [0,0]
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

		return (average_difference[0],average_difference[1])

	@staticmethod
	def LeadChanges(game_data):
		""" Count the number of times a team takes the lead """

		change_count = 0
		away_score, home_score = 0, 0
		leader = None
		for i in game_data['linescore']['inning']:

			away_score += int(i['away'])

			if away_score > home_score and leader != "away":
				leader = "away"
				change_count += 1

			if 'home' in i:
				home_score += int(i['home'])

			if home_score > away_score and leader != "home":
				leader = "home"
				change_count += 1

		return change_count

	@staticmethod
	def RBIDistribution(game_data):
		""" Returns a list of players for each team with a percentage of RBIs for their team
			over RBI_THRESHOLD_PERCENT. Returns a tuple of lists of tuples:
			([(<LAST NAME>, <RBIs>, <RBI_PERCENTAGE>), ... etc) """

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
					rbi_percent = float(team['rbi']) / float(team['rbi'])
					rbi_players[team_index].append( (batter['name_display_first_last'].split(' ')[-1], batter_rbi, rbi_percent) )
			# Change the team index
			team_index = 0

		return rbi_players

