# models redux
class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board() 
        self.fleet = []
        # below applies to the player not the players board
        self.previous_targets = []

    def is_ready(self):
        return len(self.fleet) == 5

class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.hits = 0
    def hit(self):
        self.hits += 1
    def is_sunk(self):
        return self.hits == self.size

class Board:
    def __init__(self, size=10):
        self.size = size
        self.locations = self.create_board()
    # creates key and checks to see if it is valid
    # i like this below
    # tested
    def create_board(self):
        return {chr(65+j)+str(i+1): '~' for i in range(self.size) for j in range(self.size)}

    def board_key(self, string_value):
        column = "".join([char.upper() for char in string_value if char.isalpha()])
        # breaks near "Z"
        if ord(column) > 64 + self.size or ord(column) < 65:
            return False  
        row = "".join([number for number in string_value if number.isdigit()])
        if int(row) > self.size or int(row) < 1:
            return False
        dict_key_format = column + row
        return dict_key_format
    # tested
    # using to place ships
    def value_at_location(self, string_key):
        dict_key = self.board_key(string_key)
        if dict_key:
            return self.locations[dict_key]
        return False
    # i like this below
    # sets key value to the value provided if the key is in the dict
    def edit_board(self, string_value, value):
        key = self.board_key(string_value)
        if key:
            self.locations[key] = value
            return True
        return False
    # locates valid sequences of coordinates
    # sequences begin at start 
    #   PARTIALLY TESTED
    def generate_sequences(self, start_string, size):
        sequences = []

        start = self.board_key(start_string)

        if not start:
            return False

        end_list = self.sequence_direction(start, size)
        
        for end in end_list:
            if end:
                if end.isalpha() and self.board_key(end+start[1:]):

                    raw_range = self.coordinate_generator(ord(start[0]), ord(end))
                    sequences.append([chr(l) + start[1:] for l in raw_range])

                elif end.isdigit() and self.board_key(end+start[0]):

                    raw_range = self.coordinate_generator(int(start[1:]), int(end))
                    sequences.append([start[0] + str(i) for i in raw_range]) 

        return sequences

    # creates a list of end coordinates based on an origin
    # ends are found by adding or subtracting length
    #   PARTIALLY TESTED 
    def sequence_direction(self, origin, length): 
        length -= 1                  
        end_list = []
        # vertical down
        end = str(int(origin[1:])+length)
        end_list.append(end)
        # vertical up
        end = str(int(origin[1:])-length)
        end_list.append(end)
        # horizontal right
        end = chr(ord(origin[0])+length)
        end_list.append(end)
        # horizontal left
        end = chr(ord(origin[0])-length)
        end_list.append(end)
        return end_list
    #   PARTIALLY TESTED
    def coordinate_generator(self, start, end):
        step = 1 - 2 * (start > end)
        return [i for i in range(start, end+step, step)]

    def display_board(self):
        display = []
        for j in range(self.size):
            line = []
            for i in range(self.size):
                if isinstance(self.locations[chr(65+i)+str(j+1)], str):
                    line.append('  {}  '.format(self.locations[chr(65+i)+str(j+1)]))
                else:
                    line.append('  ~  ')
                    
            display.append(line)
        return display



# any interaction between a player and another players board occurs in this class
class BattleShip:
    def __init__(self):
        self.players = []
        self.war_time = False
        # not sure how to do this
        # self.ship_sizes = {'Aircraft Carrier':5,'BattleShip':4,'Submarine':3,'Destroyer':3,'Patrol Boat':2}
    # adjusted for new board model
    # TESTED
    def add_player(self, player):
        self.players.append(player)

    # TESTED
    def end_turn(self):
        if self.game_over() and self.war_time:
            return False
        last_player = self.players.pop(0)
        self.players.append(last_player) 
        return True
 
    # TESTED
    def current_board(self):
        if self.war_time:
            target = 1
        else:
            target = 0
        return self.players[target].board

    # Half Tested
    def game_over(self):
        for ship in self.players[1].fleet:
            if not ship.is_sunk():
                return False
        return True

    # TESTED
    # You Optimized it?
    # Yeah, we optimized it. 
    def ship_location_validator(self, start_coor, ship):
        target_board = self.current_board()
        if start:
            return target_board.generate_sequences(start_coor, ship.size)
        else:
            return False

    # has not been optimized for ai
    # TESTED
    def place_ship_here(self, locations, ship):
        if self.occupied(locations):
            return False
        for key in locations:
            # might not want to use current_board() here
            self.current_board().edit_board(key, ship)   
        self.players[0].fleet.append(ship) 
        return True

    # input from BattleShip.ship_location_validator()
    # called in BattleShip.ship_location_validator()
    # has not been optimized for ai
    # TESTED
    def occupied(self, coordinates):
        # has to be adapted
        current_board = self.current_board()
        for key in coordinates:
            # USES VALUE_AT
            if current_board.value_at_location(key) != '~':
                return True
        return False

    # user inputs coordinates
    # called in the controller
    # has not been optimized for ai
    def shoot_at(self, coordinate):
        target_board = self.current_board()
        target_key = target_board.board_key(coordinate)

        if not target_key or target_key in self.players[0].previous_targets:
            return False
        # USES VALUE_AT
        if target_board.value_at_location(target_key) != '~':
            target_board.value_at_location(target_key).hit()
            # target_board.value_at_location(target_key).is_sunk()
            # Value to insert at target location
            value = "*"
            
        else:
            # Value to insert at target location
            value = chr(164)

        target_board.edit_board(target_key, value)
        self.players[0].previous_targets.append(target_key)
        return True




def set_up_game():
    ac = Ship("Aircraft Carrier", 5)
    destroyer = Ship("Destroyer", 3)

    game = BattleShip()
    game.add_player(Player("Zack"))
    game.add_player(Player("Bill"))
    game.players[0].board.create_board()
    game.players[1].board.create_board()
    ship_local = game.ship_location_validator("9a","9c",destroyer)
    game.place_ship_here(ship_local, destroyer)
    ship_local = game.ship_location_validator("2e","e6",ac)
    game.place_ship_here(ship_local, ac)
    # [print(line) for line in game.players[0].board.display_board()]
    return game
# game.ship_location_validator("F6","9f",destroyer)
# game = set_up_game()
# game.current_board().display_board()
# game.shoot_at("1a")
# print(game.current_board().display_board())
# [print(line) for line in test.current_board().display_board()] 