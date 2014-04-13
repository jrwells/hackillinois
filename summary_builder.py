import Queue

from debug import log
import twitter_scraper
import pickle

SHAME_WEIGHT = 0.20
RELEVANCE_WEIGHT = 0.10

MAX_STRINGS = 6

REAL_DATA = True # each run costs 4 api calls to Alchemy - don't overuse

TEAMS = {"Orioles":["#Orioles","@Orioles"],
         "Red Sox":["#RedSox","@RedSox"],
         "Yankees":["#Yankees","@Yankees"],
         "Rays":["#Rays","@RaysBaseball"],
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
         "D-backs":["#DBack","#Diamondbacks","@DBacks"],
         "Rockies":["#Rockies","@Rockies"],
         "Dodgers":["#Dodgers","@Dodgers"],
         "Padres":["#Padres","@Padres"],
         "Giants":["#SFGiants","@SFGiants"],
         "Pirates":["#Pirates","@Pirates"]}

class SummaryBuilder:
  def __init__(self, main_description, short_description, winning_team, losing_team):
    ts = twitter_scraper.TwitterScraper()
    self.pq = Queue.PriorityQueue()
    self.short_description = short_description
    self.main_description = main_description
    self.winning_team = winning_team
    self.losing_team = losing_team
    self.event_list = []
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
    winning_events, losing_events, added = [], [], []
    while len(strings) < MAX_STRINGS and not self.pq.empty():
      pri, event = self.pq.get_nowait()
      if event.team_name == self.winning_team:
        winning_events.append(event)
      else:
        losing_events.append(event)
    winning_events.sort(key=lambda x: x.event_type, reverse=False)
    losing_events.sort(key=lambda x: x.event_type, reverse=False)
    events = winning_events + losing_events
    for event in events:
      will_add = True
      if event.event_type == 2:
        e_owner = ''
        if type(event.event_owner) == list or type(event.event_owner) == tuple:
          e_owner = event.event_owner[0]
        else:
          e_owner = event.event_owner
        for add in added:
          if add.event_type == 2:
            if type(add.event_owner) == list or type(add.event_owner) == tuple:
              if e_owner in add.event_owner:
                will_add = False
            else:
              if e_owner == add.event_owner:
                will_add = False
      if will_add:
        strings.append(str(event))
      added.append(event)

    self.event_list = events
    return " ".join(strings)

  """
  Build a shorter summary for twitter.
  """
  def build_teaser_text(self):
    strings, added = [self.short_description], []
    for event in self.event_list:
        will_add = True
        if event.event_type == 2:
          e_owner = ''
          if type(event.event_owner) == list or type(event.event_owner) == tuple:
            e_owner = event.event_owner[0]
          else:
            e_owner = event.event_owner
          for add in added:
            if add.event_type == 2:
              if type(add.event_owner) == list or type(add.event_owner) == tuple:
                if e_owner in add.event_owner:
                  will_add = False
              else:
                if e_owner == add.event_owner:
                  will_add = False
        if will_add:
          strings.append(str(event.teaser))
        added.append(event)

    return " ".join(strings)



