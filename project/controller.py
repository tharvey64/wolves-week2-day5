from models import Player,Ship,Board,BattleShip
from views import View

class Controller:
    def __init__(self):
       self.view = View()
       self.game = BattleShip()
       # self.admiral
       self.ship = []

    def add_game_players(self):
        name = self.view.get_player_name()
        self.game.add_player(Player(name))

        name = self.view.get_player_name()
        self.game.add_player(Player(name))

    def assemble_armada(self):
        self.view.fleet_status()
        armada = {'Aircraft Carrier':5,'BattleShip':4,'Submarine':3,'Destroyer':3,'Patrol Boat':2}
        while not self.game.players[0].is_ready():
            for ship_info in armada.items():
                # self.view.select_ship_to_position()
                print(ship_info)
                self.ship = Ship(ship_info[0], ship_info[1])

                start_value = self.view.position_starting_coordinate()
                end_value = self.view.position_ending_coordinate()

                board_location = self.game.ship_location_validator(start_value, end_value, self.ship)
                self.game.place_ship_here(board_location, self.ship)

            if self.game.players[0].is_ready():
                self.game.end_turn()
            # self.view.coordinates_invalid()
        self.game.war_time = True

    def game_flow(self):
        while not self.game.game_over():
            self.view.display_game(self.game.current_board().display_board())
            target = ""
            while self.game.shoot_at(target):
                target = self.view.enter_firing_coordinates()
                self.game.shoot_at(target)
            self.game.end_turn()
            # make different game methods to handle different boolean return values
        self.view.victory_game_over()


def set_up_game():
    control = Controller()
    control.add_game_players()
    control.assemble_armada()
    control.game_flow()
set_up_game()
