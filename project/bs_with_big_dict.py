# models redux
class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        # need something to add ships or the 
        # ship needs to be added in the game
        self.ships = []
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
        self.board = {chr(65+j)+str(i+1): '~' for i in range(self.size) for j in range(self.size)}
        self.previous_targets = []
        
    # creates key and checks to see if it is valid
    # i like this below
    def _board_key(self, string_value):
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
    def value_at_location(self, string_key):
        dict_key = self._board_key(string_value)
        if dict_key:
            self.previous_targets.append(dict_key)
            return self.board[dict_key]
        return False
    # i like this below
    # sets key value to the value provided if the key is in the dict
    def edit_board(self, string_value, value):
        key = self._board_key(string_value)
        if key:
            self.board[key] = value
            return True
        return False
    # add dict value to board here 
    def display_board(self):
        return [['  ~  'for i in range(self.size)] for j in range(self.size)]


