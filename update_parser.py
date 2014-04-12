import datetime, requests, MySQLdb

# return a list of game IDs for games that aren't finished
def getUnfinishedGames():
	db = MySQLdb.connect(host="box650.bluehost.com",
		user="colorap5_unclec",
		passwd="zLoV$&mF*M#w",
		db="colorap5_unclec")

	cur = db.cursor()

	# get games that have started and haven't finished
	query = "SELECT `game_id` FROM `games` WHERE `start_time` < NOW() AND `finished` = 0;"
	cur.execute(query)

	gameQueue = []
	for row in cur.fetchall():
		gameQueue.append(row[0])
	return gameQueue



root = 'http://gd2.mlb.com/components/game/mlb/'
current_date = datetime.datetime.now()
day, month, year = current_date.day, current_date.month, current_date.year

url = '%syear_%s/month_%02d/day_%02d/master_scoreboard.json' % (root, year, int(month), int(day))

queue = getUnfinishedGames()

if queue:
	# master_scoreboard = requests.get(url).json()
	master_scoreboard = open("master_scoreboard.json").json()

	print master_scoreboard

else:
	print "No missing data ;)"
