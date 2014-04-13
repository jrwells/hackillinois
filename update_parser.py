import datetime, json, urllib2, MySQLdb
from summarize import *
from metrics import *
from event_builder import *
from summary_builder import *

def resetDB():
	query = "UPDATE `games` SET `finished` = 0;"
	cur.execute(query)

# return a list of game IDs for games that aren't finished
def getUnfinishedGames():
	# get games that have started and haven't finished
	query = "SELECT `game_id` FROM `games` WHERE `start_time` < NOW() AND `finished` = 0;"
	cur.execute(query)

	gameQueue = []
	for row in cur.fetchall():
		gameQueue.append(row[0])
	return gameQueue


def generateSummary(gameData):
	# start with who won and the score
	summary = Summarize.get_winner(gameData)
	short_summary = Summarize.get_winner_short(gameData)

	blurbs = []

	# notable things - no hitters, perfect games, etc.
	#blurbs.append(Summarize.get_no_hitter(gameData))

	# grand slams and home runs
	#blurbs.append(Summarize.get_home_runs(gameData))

	# errors
	#blurbs.append(Summarize.get_errors(gameData))

	# perfect game
	#blurbs.append(Summarize.get_perfect_game(gameData))

	# mvp batter
	#blurbs.append(Summarize.get_mvp_batter(gameData))

	# winning pitcher
	#blurbs.append(Summarize.get_winning_pitcher(gameData))

	# get top 3 blurbs
	#blurbs.sort()
	#blurbs.reverse()

	#for i in range(0, len(blurbs)):
#		if blurbs[i][0] > 0:
	#		summary = summary + " " + blurbs[i][1]

	#inning runs total runs
	# summary += '<br> Inning Runs / Total Runs: %s' % (str(Metrics.InningRunsTotalRuns(gameData))).replace("'", '')

	# #walked in runs
	# summary += '<br> Walked in Runs: %s' % (str(Metrics.WalksAndBalks(gameData)))

	# #pitching changes
	# summary += '<br> Pitching Changes: %s' % (str(Metrics.PitchingChangeDistribution(gameData))).replace("'", '')

	# #Game batting ave
	# summary += '<br> Game Batting Aves: %s' % (str(Metrics.GameBattingAvgVsSeason(gameData)))

	# #Lead changes
	# summary += '<br> Lead Changes: %s' % (str(Metrics.LeadChanges(gameData)))

	# #RBI percentage
	# summary += '<br> RBI Percentage: %s' % (str(Metrics.RBIDistribution(gameData))).replace("'", '')
	event_builder = EventBuilder(gameData)
	summary_builder = SummaryBuilder(summary, short_summary, gameData['away_team_name'], gameData['home_team_name'] )
	for event in event_builder.build_events():
		summary_builder.add_event(event)

	return (summary_builder.build_summary(), summary_builder.build_teaser_text())

# initialize db connection
db = MySQLdb.connect(
		host="box650.bluehost.com",
		user="colorap5_unclec",
		passwd="zLoV$&mF*M#w",
		db="colorap5_unclec")

cur = db.cursor()

root = 'http://gd2.mlb.com/components/game/mlb/'
current_date = datetime.datetime.now()
day, month, year = current_date.day, current_date.month, current_date.year

url = '%syear_%s/month_%02d/day_%02d/master_scoreboard.json' % (root, year, int(month), int(day))

resetDB()
queue = getUnfinishedGames()

if queue:
	# master_scoreboard = json.load(urllib2.urlopen(url))
	master_scoreboard = json.load(open("master_scoreboard.json"))
	loops = 0

	for record in master_scoreboard['data']['games']['game']:
		if record['id'] in queue:
			if record['status']['status'] == "Final":
				# fetch boxscore and coalesce
				root_dir = "http://gd2.mlb.com" + record['game_data_directory'] + '/boxscore.json'
				boxscore = json.load(urllib2.urlopen(root_dir))['data']['boxscore']
				record['boxscore'] = boxscore

				summary, teaserText = generateSummary(record)

				query = "UPDATE `games` SET `finished` = 1, `full_summary` = \"%s\" WHERE `game_id` = '%s' LIMIT 1;" % (summary, record['id'])
				cur.execute(query)

				loops = loops + 1

	print "Updated %d game(s)" % loops
else:
	print "No missing data ;)"
