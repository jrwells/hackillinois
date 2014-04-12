import datetime, json, requests, MySQLdb

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
	return "GAME: %s" % str(gameData['home_team_name'])

def generateTeaserText(gameData):
	return ""

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

queue = getUnfinishedGames()

if queue:
	# master_scoreboard = requests.get(url).json()
	master_scoreboard = json.load(open("master_scoreboard.json"))
	loops = 0

	for record in master_scoreboard['data']['games']['game']:
		if record['id'] in queue:
			if record['status']['status'] == "Final":
				summary = generateSummary(record)
				teaserText = generateTeaserText(record)

				query = "UPDATE `games` SET `finished` = 1, `full_summary` = '%s', `teaser_text` = '%s' WHERE `game_id` = '%s' LIMIT 1;" % (summary, teaserText, record['id'])
				cur.execute(query)

				loops = loops + 1

	print "Updated %d game(s)" % loops
else:
	print "No missing data ;)"
