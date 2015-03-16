class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board() 
        self.fleet = []
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
        # if you return self then the name wont matter
        if self.hits == self.size:
            return self.name
        return False
        

class Board:
    def __init__(self, size=10):
        self.size = size
        self.locations = self.create_board()

    def create_board(self):
        return {chr(65+j)+str(i+1): '~' for i in range(self.size) for j in range(self.size)}

    def board_key(self, string_value):
        if not string_value:
            return False
        column = "".join([char.upper() for char in string_value if char.isalpha()])
        if ord(column) > 64 + self.size or ord(column) < 65:
            return False  
        row = "".join([number for number in string_value if number.isdigit()])
        if int(row) > self.size or int(row) < 1:
            return False
        dict_key_format = column + row
        return dict_key_format

    def value_at_location(self, string_key):
        dict_key = self.board_key(string_key)
        if dict_key:
            return self.locations[dict_key]
        return False

    def edit_board(self, string_value, value):
        key = self.board_key(string_value)
        if key:
            self.locations[key] = value
            return True
        return False

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

class BattleShip:
    def __init__(self):
        self.players = []
        self.war_time = False
        # self.ship_sizes = {'Aircraft Carrier':5,'BattleShip':4,'Submarine':3,'Destroyer':3,'Patrol Boat':2}

    def add_player(self, player):
        self.players.append(player)

    def end_turn(self):
        if self.game_over() and self.war_time:
            return False
        last_player = self.players.pop(0)
        self.players.append(last_player) 
        return True
 
    def current_board(self):
        if self.war_time:
            target = 1
        else:
            target = 0
        return self.players[target].board

    def game_over(self):
        for ship in self.players[0].fleet:
            if not ship.is_sunk():
                return False
        return True

    def ship_location_generator(self, start_coor, ship):
        target_board = self.current_board()
        board_positions = target_board.generate_sequences(start_coor, ship.size)
        pop_these = [idx for idx,coordinates in enumerate(board_positions) if self.occupied(coordinates)]
        [board_positions.pop(idx) for idx in pop_these]
        return board_positions

    def place_ship_here(self, locations, ship):
        if self.occupied(locations):
            return False
        for key in locations:
            self.current_board().edit_board(key, ship)   
        self.players[0].fleet.append(ship) 
        return True

    def occupied(self, coordinates):
        current_board = self.current_board()
        for key in coordinates:
            if current_board.value_at_location(key) != '~':
                return True
        return False

    def shoot_at(self, coordinate):
        target_board = self.current_board()
        target_key = target_board.board_key(coordinate)

        if not target_key or target_key in self.players[0].previous_targets:
            return False

        if target_board.value_at_location(target_key) != '~':
            target_board.value_at_location(target_key).hit()
            sunken_ship = target_board.value_at_location(target_key).is_sunk
            target_board.edit_board(target_key, "*")           
            if sunken_ship():
                return sunken_ship()          
            # value = "*"
        else:
            value = chr(164)
            target_board.edit_board(target_key, value)
        self.players[0].previous_targets.append(target_key)
        return True