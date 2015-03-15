from models import Player,Ship,Board
from views import View

class Controller:
	def __init__(self):
		self.view = View()
		self.ocean = Board(10)
		self.admiral = Player("thomas")

    # def place_ships(self):

	# def play(self):

	def initiate_game(self):
		self.view.welcome_screen()
		self.view.start_new_game()
		self.view.get_player_name()
		myGame.add_player_and_board()

	def place_vessels(self):
		self.view.fleet_status()
		self.view.select_ship_to_position()
		myShip.add_coordinates()
		self.view.position_starting_coordinate()
		self.view.position_ending_coordinate()
		myGame.place_ship()
		if myGame.place_ship == False:
			coordinates_invalid()

	def fire_guns(self):
		myGame.shoot_at()
		if myGame.shoot_at == False:
			previous_target()
		if myGame.shoot at == True:
			if myShip.is_hit() == True:
				target_hit()
				if myShip.is_sunk() == True:
					ship_sunk
			else
				target_missed()

	def manage_turn_end(self):
		myGame.check_ships()
		myGame.end_turn()

	# def get_game_status(self):
	# 	if myGame.game_over:


aPlayer = Player()
myShip = Ship()
myBoard = Board()
myGame = Controller()

myGame.initiate_game()


place_vessels()
fire_guns()
manage_turn_end()
get_game_status()
