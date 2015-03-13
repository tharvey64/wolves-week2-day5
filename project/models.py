# import sqlite3

class Player:
    def __init__(self, name):
        self.name = name
        # add through init parameters
        # self.board

class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.location = []
        self.hits = []

    def add_coordinates(self, coordinates_tuples):
        self.location = coordinates_tuples

    def is_hit(self, coordinate):
        if coordinate in self.location and coordinate not in self.hits:
            self.hits.append(coordinate)
            return True
        return False

    def is_sunk(self):
        return len(self.hits) == len(self.location)

class Board:
    def __init__(self, size):
        self.size = size
        self.ships_on_board = []
        self.previous_targets = []
        self.display = [['  ~  'for i in range(size)] for j in range(size)]
        # self.markers = {'hit':'*', 'miss':chr(164), 'wave':'~'
    def add_ship_location(self, ship):
        self.ships_on_board.append(ship)


class BattleShip:
    def __init__(self):
        self.players = []
        self.boards = []
        self.ship_sizes = {'Aircraft Carrier':5,'BattleShip':4,'Submarine':3,'Destroyer':3,'Patrol Boat':2}
    # called in controller
    def add_player(self, player):
        self.players.append(player)
    # no input
    # called in controller
    def end_turn(self):
        if self.game_over():
            return True
        last_player = self.players.pop(0)
        self.players.append(last_player) 

        last_board = self.boards.pop(0)
        self.boards.append(last_board)
        return False
    # takes two coordinates inputs from user
    # called in controller
    def place_ship(self, start_coordinates, end_coordinates, ship):
        if start_coordinates[0] == end_coordinates[0]:
            if abs(start_coordinates[1]-end_coordinates[1]) == ship.size:
                
                step = start_coordinates[1]-end_coordinates[1] / ship.size

                place_ship_here = [(coordinate[0],i) for i in range(start_coordinates[1], end_coordinates[1]+step, step)]
                
                if not self.occupied(place_ship_here):
                    ship.location = place_ship_here
                    self.boards[0].add_ship_location(ship)
                    return True

        elif start_coordinates[1] == end_coordinates[1]:
            if abs(start_coordinates[0]-end_coordinates[0]) == ship.size:
                
                step = start_coordinates[0]-end_coordinates[0] / ship.size

                place_ship_here = [(i,coordinate[1]) for i in range(start_coordinates[0], end_coordinates[0]+step, step)]
                
                if not self.occupied(place_ship_here):
                    ship.location = place_ship_here
                    self.boards[0].add_ship_location(ship)
                    return True
        return False
    # input from BattleShip.place_ship()
    # called in BattleShip.place_ship()
    def occupied(self, coordinates):
        for ship.location in self.boards[0].ships_on_board:
            for coordinate_tuple in coordinates:
                if coordinate_tuple in ship.location:
                    return True
        return False
    # user inputs coordinates
    # called in the controller
    def shoot_at(self, coordinate):
        if coordinate in self.boards[1].previous_targets:
            return False
        self.boards[1].previous_targets.append(coordinate)
        return True
    # no input
    # call in controller
    def check_ships(self):
        for ship in self.boards[1].ships_on_board:
            if not ship.is_sunk() and ship.is_hit(self.boards[1].previous_targets[-1])
                coordinate = self.boards[1].previous_targets[-1]
                self.boards[1].display[coordinate[1]][coordinate[0]] = '*'
                return True
        self.boards[1].display[coordinate[1]][coordinate[0]] = chr(164)
        return False
    # no input
    # called in BattleShip.game_over()
    def game_over(self):
        for ship in self.boards[1].ships_on_board:
            if not ship.is_sunk():
                return False
        return True

