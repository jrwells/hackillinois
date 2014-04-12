import requests, MySQLdb
from pytz import timezone
from datetime import datetime, timedelta

# return a list of game IDs for games that aren't finished
def addNewGames(start_time, game_id):
	db = MySQLdb.connect(host="box650.bluehost.com",
		user="colorap5_unclec",
		passwd="zLoV$&mF*M#w",
		db="colorap5_unclec")

	cur = db.cursor()

	# get games that have started and haven't finished
	query = "INSERT INTO `games` (start_time, finished, game_id) VALUES ('%s', 0, '%s');" % (start_time, game_id)
	cur.execute(query)

root = 'http://gd2.mlb.com/components/game/mlb/'
current_date = datetime.now()
day, month, year = current_date.day, current_date.month, current_date.year
url = '%syear_%s/month_%02d/day_%02d/master_scoreboard.json' % (root, year, int(month), int(day))
master_scoreboard =  requests.get(url).json()
games = master_scoreboard['data']['games']['game']

timezones = { 'ET' : 'US/Eastern', 'MT' : 'US/Mountain', 'CT': 'US/Central', 'PT': 'US/Pacific', 'MST' : 'US/Mountain' }

for game in games:
	# Inserts start times in mountain times and game_id into database
	game_timezone = timezone(timezones[game['home_time_zone']])
	game_datetime = datetime.strptime("%s-%s-%s %s %s" % (year, month, day, game['home_time'], game['ampm']), "%Y-%m-%d %I:%M %p")
	mountain_time = game_timezone.localize(game_datetime).astimezone(timezone('US/Mountain')).strftime("%Y-%m-%d %H:%M")
	addNewGames(mountain_time, game['id'])


