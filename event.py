""" Describes an event. """

class Event:
	def __init__(self, description, weight, team_name, event_type, team_won=None):
		self.description = description
		self.weight = weight
		self.team_name = team_name
		self.team_won = team_won
		self.event_type = event_type

	def __str__(self):
		return "The " + self.team_name + " " + self.description + "."
