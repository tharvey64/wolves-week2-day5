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
    # add dict value to location here 
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
    # adjusted for new board model
    def __init__(self):
        self.players = []
        self.war_time = False
        # self.ship_sizes = {'Aircraft Carrier':5,'BattleShip':4,'Submarine':3,'Destroyer':3,'Patrol Boat':2}
    # called in controller
    # adjusted for new board model
    # TESTED
    def add_player(self, player):
        self.players.append(player)
    # called in controller
    # adjusted for new board model
    # TESTED
    def end_turn(self):
        if self.game_over() and self.war_time:
            return False
        last_player = self.players.pop(0)
        self.players.append(last_player) 
        return True
    # edit name of this and the instance variable
    # TESTED
    def current_board(self):
        if self.war_time:
            target = 1
        else:
            target = 0
        return self.players[target].board
    # no input
    # called in BattleShip.game_over()
    # adjusted for new board model
    # Half Tested
    def game_over(self):
        for ship in self.players[1].fleet:
            if not ship.is_sunk():
                return False
        return True

    # adjusted I Think not sure
    # slim this down 
     # TESTED
    def ship_location_validator(self, start_coor, end_coor, ship):
        # should probably pass a player into this method 
        target_board = self.current_board()

        start = target_board.board_key(start_coor)
        end = target_board.board_key(end_coor)


        # calling the board_key method ensures a letter will be
        # at index 0
        if not start or not end:
            return False

        # should the board be responsible for calculating the 
        # distances? 
        # I've decided the board should handle this
        # instead of the game.
        # check all sides using direction_of_ship
        fixed = self.direction_of_ship(start,end)
        if not fixed:
            return False
        elif abs(int(start[1:])-int(end[1:]))+1 == ship.size:
           
            row_values = self.coordinate_generator(int(start[1:]),int(end[1:]))
            valid_location = [target_board.board_key(fixed + str(i)) for i in row_values]
            return valid_location

        elif abs(ord(start[0])-ord(end[0]))+1 == ship.size:

            column_values = self.coordinate_generator(ord(start[0]),ord(end[0]))
            valid_location = [target_board.board_key(fixed + chr(x)) for x in column_values]
            return valid_location

        else:
            return False
    # might move this to the board
    # although it does not use any board methods
    # UPDATE Must Move this to Board
    # UPDATE The other methods i intend to move need this method
    # Rename this in board class
    # TESTED
    def direction_of_ship(self, start, end):
        if start[0] == end[0]:
            return start[0]
        elif start[1:] == end[1:]:
            return start[1:]
        else:
            return False
    # this should be moved to the board class
    # UPDATE Must Move this to Board
    # TESTED
    def coordinate_generator(self, start, end):
        step = 1 - 2 * (start > end)
        return [i for i in range(start, end+step, step)]

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
        current_board = self.players[0].board
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
