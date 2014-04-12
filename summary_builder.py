GENERIC_EVENT = 0

# Events that are not affected
MAIN_SUMMARY = 1

# Events that are more interesting if you win
GENERIC_POSITIVE = 101

# Events that are more interesting if you lose
GENERIC_NEGATIVE = 201

class SummaryBuilder:
  def __main__(self):
    pass

  """
  Add an event to the SummaryBuilder.  Arguments:
    description: the string to add to the Summary
    type: a type constant - determines weight effects
    weight: arbitrary measure of importance between 0<=w<=1
    (team_won: did this team win - True or False
        if None, this event doesn't correspond to a team.)
  """
  def add_event(self, description,type,weight,team_won=None):
    pass

  """
  Build a summary for this game.
  """
  def build_summary(self):
    pass