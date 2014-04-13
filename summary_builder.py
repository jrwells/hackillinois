import Queue

from debug import log
import twitter_scraper
import pickle

SHAME_WEIGHT = 0.20
RELEVANCE_WEIGHT = 0.10

MAX_STRINGS = 6

REAL_DATA = False # each run costs 4 api calls to Alchemy - don't overuse

TEAMS = {"Orioles":["#Orioles","@Orioles"],
         "Red Sox":["#RedSox","@RedSox"],
         "Yankees":["#Yankees","@Yankees"],
         "Devil Rays":["#Rays","@RaysBaseball"],
         "Blue Jays":["#BlueJays","@BlueJays"],
         "White Sox":["#WhiteSox","@WhiteSox"],
         "Indians":["#Indians","@Indians"],
         "Tigers":["#Tigers","@Tigers"],
         "Royals":["#Royals","@Royals"],
         "Twins":["#Twins","#MNTwins","@Twins"],
         "Angels":["#Angels","@Angels"],
         "Athletics":["#Athletic","@Athletics"],
         "Mariners":["#Mariners","@Mariners"],
         "Rangers":["#Rangers","@Rangers"],
         "Braves":["#Braves","@Braves"],
         "Marlins":["#Marlins","@Marlins"],
         "Mets":["#Mets","@Mets"],
         "Phillies":["#Phillies","@Phillies"],
         "Nationals":["#Nats","#Nationals","@Nationals"],
         "Cubs":["#Cubs","@Cubs"],
         "Reds":["#Reds","@Reds"],
         "Astros":["#Astros","@Astros"],
         "Brewers":["#Brewers","@Brewers"],
         "Cardinals":["#STLCards","#Cardinals","@Cardinals"],
         "Diamondbacks":["#DBack","#Diamondbacks","@DBacks"],
         "Rockies":["#Rockies","@Rockies"],
         "Dodgers":["#Dodgers","@Dodgers"],
         "Padres":["#Padres","@Padres"],
         "Giants":["#SFGiants","@SFGiants"]}

class SummaryBuilder:
  def __init__(self, main_description, winning_team, losing_team):
    ts = twitter_scraper.TwitterScraper()
    self.pq = Queue.PriorityQueue()
    self.main_description = main_description
    if REAL_DATA:
      ## TODO: map team names to their hashtags
      if winning_team in TEAMS:
        self.win_team_sentiment = ts.analyze_tweets(ts.get_tweets(" OR ".join(TEAMS[winning_team])))
      else:
        log('ALERT: Failed to load sentiment data for team %s'%(winning_team))
        self.win_team_sentiment = {}
      if losing_team in TEAMS:
        self.lose_team_sentiment = ts.analyze_tweets(ts.get_tweets(" OR ".join(TEAMS[losing_team])))
      else:
        log('ALERT: Failed to load sentiment data for team %s'%(losing_team))
        self.lose_team_sentiment = {}
    else:
      self.win_team_sentiment = pickle.load(open('keywords.p'))
      self.lose_team_sentiment = pickle.load(open('keywords.p'))

  """
  Add an event to the SummaryBuilder.  Arguments:
    event: an Event

    -- old description here for clarity --
    description: the string to add to the Summary
    weight: arbitrary measure of importance between 0<=w<=1
            shametext is negative
    (team_won: did this team win - True or False
        if None, this event doesn't correspond to a team.)
  """
  def add_event(self,event):
    description = event.description
    weight = event.weight
    team_won = event.team_won

    if team_won == None or weight >= 0:
      real_weight = abs(weight)
    else:
      if team_won:
        adjusted_shame_weight = -SHAME_WEIGHT
      else:
        adjusted_shame_weight = SHAME_WEIGHT

      real_weight = abs(min(weight + adjusted_shame_weight, 0.0)) #apply the shameeeeee

    ## TODO: APPLY RELEVANCE + SENTIMENT ANALYSIS
    relevance = 0.0
    if team_won != None:
      if team_won: sent_db = self.win_team_sentiment
      else: sent_db = self.lose_team_sentiment

      for keyword in sent_db:
        if keyword in description.lower():
          relevance = relevance + sent_db[keyword]['relevance']
          log('keyword weight %s %f'%(keyword, relevance),'+ ')
    real_weight = real_weight + (relevance * RELEVANCE_WEIGHT)

    log('pri %f, PUT "%s"'%(real_weight,description))
    self.pq.put_nowait((1.0-real_weight,event))

  """
  Build a summary for this game.
  """
  def build_summary(self):
    strings = [self.main_description]
    while len(strings) < MAX_STRINGS and not self.pq.empty():
      pri,event = self.pq.get_nowait()
      strings.append(str(event))

    return " ".join(strings)