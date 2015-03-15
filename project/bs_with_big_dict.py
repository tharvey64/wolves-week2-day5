# models redux
class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        # need something to add ships or the 
        # ship needs to be added in the game
        self.fleet = []
        # below applies to the player not the players board
        self.previous_targets = []
        # should the player keep track of the previous
        # guesses

class Ship:
    # ship_sizes = {'Aircraft Carrier':5,'BattleShip':4,'Submarine':3,'Destroyer':3,'Patrol Boat':2}
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.hits = 0
    def hit(self):
        self.hits += 1
    def is_sunk(self):
        return len(self.hits) == self.size

class Board:
    def __init__(self, size=10):
        self.size = size
        self.location = {}
    # creates key and checks to see if it is valid
    # i like this below
    # tested
    def create_board(self):
        self.location = {chr(65+j)+str(i+1): '~' for i in range(self.size) for j in range(self.size)}

    def board_key(self, string_value):
        column = "".join([char.upper() for char in string_value if char.isalpha()])
        if ord(column) > 64 + self.size or ord(column) < 65:
            return False  
        row = "".join([number for number in string_value if number.isdigit()])
        if int(row) > self.size or int(row) < 1:
            return False
        dict_key_format = column + row
        return dict_key_format
    # returns the value at the key provided if the key is in the dict 
    # i dont like this it shouldnt return the ship value the ship value 
    # contains info about the ship
    # tested
    # using to place ships
    def value_at_location(self, string_key):
        dict_key = self.board_key(string_key)
        if dict_key:
            return self.location[dict_key]
        return False
    # i like this below
    # sets key value to the value provided if the key is in the dict
    def edit_board(self, string_value, value):
        key = self.board_key(string_value)
        if key:
            self.location[key] = value
            return True
        return False
    # add dict value to location here 
    def display_board(self):
        display = [[self.location[chr(65+i)+str(j+1)] for i in range(self.size)] for j in range(self.size)]
        return display

class BattleShip:
    # adjusted for new board model
    def __init__(self):
        self.players = []
        # self.ship_sizes = {'Aircraft Carrier':5,'BattleShip':4,'Submarine':3,'Destroyer':3,'Patrol Boat':2}
    # called in controller
    # adjusted for new board model
    def add_player(self, player):
        self.players.append(player)
    # no input
    # called in controller
    # adjusted for new board model
    def end_turn(self):
        if self.game_over():
            return False
        last_player = self.players.pop(0)
        self.players.append(last_player) 
        return True
    # takes two coordinates inputs from user
    # called in controller
    # adjusted I Think not sure
    def place_ship(self, start_coor, end_coor, ship):
        place_ship_here = []
        current_board = self.players[0].board

        start = current_board.board_key(start_coor)
        end = current_board.board_key(end_coor)
        # calling the board_key method ensures a letter will be
        # at index 0
        if start[0] == end[0]:
            if abs(int(start[1:])-int(end[1:])) == ship.size:
                
                row_values = self.coordinate_generator(int(start[1:]),int(end[1:]))
                place_ship_here = [start[0]+str(i) for i in row_values]

        elif start[1:] == end[1:]:
            if abs(ord(start[0])-ord(end[0])) == ship.size:

                column_values = self.coordinate_generator(ord(start[0]),ord(end[0]))
                place_ship_here = [chr(x) + start[1:] for x in column_values]

        if place_ship_here and not self.occupied(place_ship_here):
            for key in place_ship_here:
                current_board.edit_board(key, ship)
            return True
        return False
    # adjusted for new version
    def coordinate_generator(start, end):
        step = int(start-end / -(start-end))
        return [i for i in range(start, end+step, step)]

    # input from BattleShip.place_ship()
    # called in BattleShip.place_ship()
    # adjusted
    def occupied(self, coordinates):
        current_board = self.players[0].board
        for key in coordinates:
            # USES VALUE_AT
            if current_board.value_at_location(key) != '~':
                return True
        return False
    # user inputs coordinates
    # called in the controller
    # adjusted 
    def shoot_at(self, coordinate):
        target_board = self.players[1].board
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

        target_board.edit_board(key, value)
        self.players[0].previous_targets.append(target_key)
        return True

    # no input
    # called in BattleShip.game_over()
    # adjusted for new board model
    def game_over(self):
        for ship in self.players[1].fleet:
            if not ship.is_sunk():
                return False
        return True