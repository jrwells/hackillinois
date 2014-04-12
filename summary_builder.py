import Queue

SHAME_WEIGHT = 0.05

MAX_STRINGS = 6

class SummaryBuilder:
  def __main__(self, main_description, winning_team, losing_team):
    self.pq = Queue.PriorityQueue()

  """
  Add an event to the SummaryBuilder.  Arguments:
    description: the string to add to the Summary
    weight: arbitrary measure of importance between 0<=w<=1
            shametext is negative
    (team_won: did this team win - True or False
        if None, this event doesn't correspond to a team.)
  """
  def add_event(self,description,weight,team_won=None):
    if team_won == None or team_won:
      real_weight = weight
    else:
      real_weight = weight - SHAME_WEIGHT #apply the shameeeeee

    ## TODO: APPLY SENTIMENT ANALYSIS

    self.pq.put_nowait((1.0-real_weight,description))

  """
  Build a summary for this game.
  """
  def build_summary(self):
    count = 0
    strings = []
    while count < MAX_STRINGS and not self.pq.Empty():
      pri,string = self.pq.get_nowait()
      strings.append(string)

    return " ".join(strings)