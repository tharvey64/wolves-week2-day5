from models import Player,Ship,Board
from views import View

class Controller:
	def __init__(self):
	   self.view = View()
       self.ocean = Board(10)
       self.admiral = Player("thomas")

    # def place_ships(self):
