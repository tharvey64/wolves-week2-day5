# import sqlite3

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()

class Ship:
    # ship_sizes = {'Aircraft Carrier':5,'BattleShip':4,'Submarine':3,'Destroyer':3,'Patrol Boat':2}
    def __init__(self, name, size):
        self.name = name
        self.size = size
        # might remove this with dictionary
        self.location = []
        self.hits = []

    def add_coordinates(self, coordinates_tuples):
        self.location = coordinates_tuples
        # change is hit to hit and have it mark it self as hit
    def is_hit(self, coordinate):
        if coordinate in self.location and coordinate not in self.hits:
            self.hits.append(coordinate)
            return True
        return False

    def is_sunk(self):
        return len(self.hits) == len(self.location)

class Board:
    def __init__(self, size=10):
        self.size = size
        # new idea below
        # self.board = {}
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
    def add_player(self, player, board):
        self.players.append(player)
        self.boards.append(board)
    # no input
    # called in controller
    def end_turn(self):
        if self.game_over():
            return False
        last_player = self.players.pop(0)
        self.players.append(last_player) 

        last_board = self.boards.pop(0)
        self.boards.append(last_board)
        return True
    # takes two coordinates inputs from user
    # called in controller
    def place_ship(self, start_coor, end_coor, ship):
        place_ship_here = []
        if start_coor[0] == end_coor[0]:
            if abs(start_coor[1]-end_coor[1]) == ship.size:
                
                y_coor = self.coordinate_generator(start_coor[1],end_coor[1])
                place_ship_here = [(start_coor[0],y) for y in y_coor]

        elif start_coor[1] == end_coor[1]:
            if abs(start_coor[0]-end_coor[0]) == ship.size:

                x_coor = self.coordinate_generator(start_coor[0],end_coor[0])
                place_ship_here = [(x,start_coor[1]) for x in x_coor]

        if place_ship_here and not self.occupied(place_ship_here):
            ship.location = place_ship_here
            self.boards[0].add_ship_location(ship)
            return True
        return False

    def coordinate_generator(start, end):
        step = int(start-end / -(start-end))
        return [i for i in range(start, end+step, step)]
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
            if not ship.is_sunk() and ship.is_hit(self.boards[1].previous_targets[-1]):
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

