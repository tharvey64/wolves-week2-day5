from models import Player, Computer, BattleShipGame
from views import View

class Controller:
    def __init__(self):
        self.view = View()
        # self.admiral
        self.ship_specs = [
            dict(tag="A",name="Aircraft Carrier",size=5),
            dict(tag="B",name="Battleship",size=4),
            dict(tag="C",name="Crusier",size=3),
            dict(tag="S",name="Submarine",size=3),
            dict(tag="D",name="Destroyer",size=2)
        ] 
        self.game = BattleShipGame()
        self.game.ship_classifications = self.ship_specs

    def add_game_players(self):
        num_of_players = self.view.single_or_multiplayer()
        if not num_of_players.isdigit():
            num_of_players = 1
        for num in range(int(num_of_players)):
            name = self.view.get_player_name(num+1)
            self.game.add_player(Player(name))
        if num_of_players == '1':
            self.game.add_player(Computer())

    @staticmethod
    def check_location(point, board):
        if not point[1:].isdigit() or not point[0].isalpha():
            return None, None
        x_in = int(point[1:])-1
        y_in = ord(point[0])-65
        if not -1 < y_in < board.size or not -1 < x_in < board.size:
            return None, None
        return x_in, y_in

  
    def assemble_armada(self):
        # Add Option To Place Ships Randomly on The Board
        self.view.fleet_status()
        for admiral in  self.game.players:
            is_computer = isinstance(admiral, Computer)
            for ship_spec_idx in range(5):     
                ship_placed = None
                while not ship_placed:
                    # User/Computer

                    if is_computer:
                        # Can pass board height and width here
                        start_value = admiral.ship_placement_start_point()
                    else:
                        start_value = self.view.position_starting_coordinate(self.ship_specs[ship_spec_idx])
                    if any(num is None for num in self.check_location(start_value, admiral.board)):
                        continue
                    board_locations, place_ship_here = self.game.choose_ship_location(start_value, ship_spec_idx, admiral)
                    if not board_locations:
                        continue
                    # User/Computer
                    if is_computer:
                        selection_idx = admiral.position_ship(board_locations)
                    else:
                        selection_idx = self.view.position_selection(board_locations)
                        if not selection_idx.isdigit(): continue
                    ship_placed = place_ship_here(int(selection_idx))
                    if not ship_placed and not is_computer:
                        self.view.coordinates_invalid()
                self.game.add_ship_to_player(ship_placed, admiral)
                # Make This Optional
                if not is_computer:
                    board = self.game.display_player_board(admiral)
                    self.view.display_game(admiral.name, board)
            # Run Remaining Setup Methods For Computer Here
            if is_computer:
                # For Now Just Use computers List of Ships To Setup
                # Make Game Method That Returns The Sizes of The Opponents
                # Remaining Ships
                admiral.setup_image(admiral.fleet_status())
                # print("controller line 78")
                # print(admiral._Computer__image)
        # AsK If They Are Ready To Play
    # Clean This Up
    def game_flow(self):
        while not self.game.game_over():
            result = False
            admiral = self.game.get_current_player() 
            opponent = self.game.get_opponent()
            board_before_shot = self.game.display_opponents_board(opponent)
            is_computer = isinstance(admiral, Computer)
            # Return A Json
            while not result:
                if not is_computer:
                    self.view.display_game(opponent.name, board_before_shot)
                location = None                
                
                while not location:
                    if is_computer:
                        # Fill In The Appropriate Methods For Strategy
                        # ^^^^^^^^^^^^^^^^^^^^^
                        location = admiral.pre_turn()
                    else:
                        location = self.view.enter_firing_coordinates()
                    if any(num is None for num in self.check_location(location, opponent.board)):
                        self.view.coordinates_invalid()
                        location = None
                # rename result
                after_action_report = self.game.fire_shot(location, opponent)
                if is_computer:
                    admiral.post_turn(after_action_report, opponent.fleet_status())
                    if after_action_report.get('executed'):
                        self.view.display_game(
                            opponent.name,
                            self.game.display_player_board(opponent)
                            )
                else:
                    if not after_action_report.get('valid'):
                        self.view.coordinates_invalid()
                    elif not after_action_report.get('executed'):
                        self.view.previous_target()
                    elif after_action_report.get('hit'):
                        if after_action_report.get('sunk'):
                            self.view.ship_sunk()
                        else:
                            self.view.target_hit()
                    else:
                        self.view.target_missed()
                    board_after_shot = self.game.display_opponents_board(opponent)
                    self.view.display_game(opponent.name, board_after_shot)
                result = after_action_report.get('executed')
            # print(chr(27) + "[2J")
        self.view.victory_game_over()

def set_up_game():
    control = Controller()
    control.add_game_players()
    control.assemble_armada()
    control.game_flow()
set_up_game()
