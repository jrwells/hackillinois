class SummaryBuilder:
  def __main__(self):
    pass

  """
  Add an event to the SummaryBuilder.  Arguments:
    description: the string to add to the Summary
    weight: arbitrary measure of importance between 0<=w<=1
            shametext is negative
    (team_won: did this team win - True or False
        if None, this event doesn't correspond to a team.)
  """
  def add_event(self,description,weight,team_won=None):
    pass

  """
  Build a summary for this game.
  """
  def build_summary(self):
    pass