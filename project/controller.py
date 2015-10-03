from models import Player,Ship,Board,BattleShip
from views import View

class Controller:
    def __init__(self):
       self.view = View()
       self.game = BattleShip()
       # self.admiral 
       self.ship = []

    def add_game_players(self):
        name = self.view.get_player_name(1)
        self.game.add_player(Player(name))

        # name = self.view.get_player_name(2)
        # self.game.add_player(Player(name))

    def assemble_armada(self):
        self.view.fleet_status()
        # armada = {'Aircraft Carrier':5,'BattleShip':4,'Submarine':3,'Destroyer':3,'Patrol Boat':2}
        armada = {'Submarine':3,'Destroyer':3,'Patrol Boat':2}
        for admiral in  self.game.players:
            for ship_info in armada.items():     
                # self.view.select_ship_to_position()
                print(ship_info)
                self.ship = Ship(ship_info[0], ship_info[1])
                
                board_locations = []
                while not board_locations:
                    start_value = self.view.position_starting_coordinate()
                    board_locations = self.game.ship_location_generator(start_value, self.ship)
                    if board_locations:
                        selection = self.view.position_selection("\n".join([str(idx+1) + ". " + str(sequence) for idx,sequence in enumerate(board_locations)]))
                        self.game.place_ship_here(board_locations[int(selection)-1], self.ship)
            self.game.end_turn()      
            # self.view.coordinates_invalid()
        # self.game.war_time = True

    def game_flow(self):
        while not self.game.game_over():
            # self.view.display_game(self.game.current_board().display_board())
            target = ""
            while not self.game.shoot_at(target):
                self.view.display_game(self.game.current_board().display_board())
                target = self.view.enter_firing_coordinates()
                self.game.shoot_at(target)
                print(chr(27) + "[2J")
            self.game.end_turn()
            # make different game methods to handle different boolean return values
        self.view.victory_game_over()


def set_up_game():
    control = Controller()
    control.add_game_players()
    control.assemble_armada()
    control.game_flow()
set_up_game()
