""" Describes an event. """

class Event:
	def __init__(self, description, weight, team_won=None):
		self.description = description
		self.weight = weight
		self.team_won = team_won