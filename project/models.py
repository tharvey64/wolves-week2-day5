import sqlite3

class Player:
    def __init__(self, name):
        self.name = name
        # add through init parameters
        # self.board

class Ship:
    def __init__(self, size):
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
        self.ship_locations = []
        self.ship_sunk = []
    # name pending
    def add_important_locations(self, ship):
        self.ship_locations.append(ship)
    # name pending
    def check_locations(self):
        for idx,ship in enumerate(self.ship_locations):
            if ship.is_sunk():
                self.ship_locations.pop(idx)
                self.ship_sunk.append(ship)



# class BattleShip:
#     def __init__(self):
#         self.players = []
#         self.boards = []
    
#     def add_player(self, player):
#         self.players.append(player)

#     def end_turn(self):
#         last_player = self.players.pop(0)
#         self.players.append(last_player)    



