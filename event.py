""" Describes an event. """

class Event:
	def __init__(self, description, weight, team_name, team_won=None):
		self.description = description
		self.weight = weight
		self.team_name = team_name
		self.team_won = team_won