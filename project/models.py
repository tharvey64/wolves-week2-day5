import random
import uuid

class Player:
    def __init__(self, name):
        self.name = name
        self.key = uuid.uuid4().hex
        self.board = Board() 
        self.__fleet = []
        self.ships_sunk = []

    def is_ready(self):
        return len(self.__fleet) == 5

    def add_ship(self, ship):
        self.__fleet.append(ship)

    def fleet_sunk(self):
        return all(ship.is_sunk() for ship in self.__fleet)
    # Consider New Name
    def fleet_status(self):
        return [ship.get_size() for ship in self.__fleet if not ship.is_sunk()]

class Computer(Player):
    def __init__(self, height=10, width=10, name="computer"):
        super().__init__(name)
        self.__image = self.__build_image(width, height)
        self.__strategy = dict(seek=self.__seek,destroy=self.__destroy)
        self.__current_strategy = 'seek'
        self.__current_hit_streak = list()

    def ship_placement_start_point(self, height=10, width=10):
        point = random.randint(1, height*width)
        x_idx = point % width
        y_idx = point // width
        return chr(y_idx+65)+str(x_idx)

    def position_ship(self, choices):
        return random.randint(0, len(choices)-1)

    def setup_image(self, all_ship_sizes):
        self.__update_image(new_image=self.__image,
            boat_sizes=all_ship_sizes, 
            condition=lambda item: True)

    def pre_turn(self):
        '''
        @return string with a letter followed by an integer or an empty string 
        '''
        print(self.__current_strategy)
        possible_targets = self.__strategy[self.__current_strategy]()
        if possible_targets:
            print("models line 53")#Based On Strategy 
            print(possible_targets)#Select Random Coordinate From This Group
            print(self.__image)
            target = max(
                possible_targets, 
                key=lambda target: self.__image[target[0]][target[1]]
                )
            print(target)
            if len(target) == 2:
                return chr(target[0]+65)+str(target[1]+1)
        return ""

    def post_turn(self, result, ship_sizes_remaining):
        # If it is one of the First Two Branches 
        # Something Went Wrong
        print(result.get('target'))
        if not result.get('valid'):
            print("Fail models.py 70")
            # invalid target
            # image is out of sync with actual board
            # Create Function That Reads In The Opponents 
            # board and creates an accurate image
        elif not result.get('executed'):
            print("Fail models.py 76")
            # previous target
            # image is out of sync with actual board
            # Create Function That Reads In The Opponents 
            # board and creates an accurate image
        else:
            # update board
            # NEED THE PREVIOUS SHOT
            point = self.convert_to_coordinate(result.get('target'))
            # set target to 0
            print('models line 84')
            print(result.get('target'))
            print(point)
            self.__image[point[0]][point[1]] = 0
            new_image = self.__build_image()
            self.__update_image(new_image=new_image, 
                boat_sizes=ship_sizes_remaining, 
                condition=lambda item: item != 0)
            if result.get('sunk'):
                # ship sunk 
                self.__current_hit_streak = []
                # switch to seek mode
                self.__current_strategy = 'seek'
            elif result.get('hit'):
                # hit ship
                self.__current_hit_streak.append(point)
                # if not destroy mode switch to destroy mode store target
                self.__current_strategy = 'destroy'
    @staticmethod
    def convert_to_coordinate(target_string):
        '''
        @param target_string is a string with a letter folled by an integer

        @return a tuple of two integers or a tuple with two NoneTypes
        '''

        if not target_string[0].isalpha() or not target_string[1:].isdigit():
            return None,None
        y_idx = ord(target_string[0])-65
        x_idx = int(target_string[1:])-1
        return y_idx, x_idx

    def __seek(self):
        '''
        @return A 2D list or an empty list
        '''

        return [[y_idx, max(enumerate(line),key=lambda item: item[1])[0]] for y_idx, line in enumerate(self.__image)]

    def __destroy(self):
        '''
        @return A 2D list or an empty list
        '''
        if len(self.__current_hit_streak) == 1:
            y_idx,x_idx = self.__current_hit_streak[0]
            return self.__get_surround(y_idx,x_idx)
        elif len(self.__current_hit_streak) > 1:
            possible_targets = []
            # This Should be refactored and Put this in a function
            # This Does Not Work If Two Ships Are Lined up Next To Each Other
            # Some How This Returned A Negative Number For ONe of The Options
            # Needs Test Data
            y_max = max(self.__current_hit_streak, key=lambda target: target[0])
            y_min = min(self.__current_hit_streak, key=lambda target: target[0])
            x_max = max(self.__current_hit_streak, key=lambda target: target[1])
            x_min = min(self.__current_hit_streak, key=lambda target: target[1])
            image_len = len(self.__image)
            if y_max[0] == y_min[0]:
                # Horizontal
                if x_min[1]-1 > -1:
                    possible_targets.append([x_min[0],x_min[1]-1])
                if x_max[1]+1 < image_len:
                    possible_targets.append([x_max[0],x_max[1]+1])
            elif x_max[1] == x_min[1]:
                # vertical
                if y_min[1]-1 > -1:
                    possible_targets.append([y_min[0]-1,y_min[1]])
                if y_max[1]+1 < image_len:
                    possible_targets.append([y_max[0]+1,y_max[1]])
            return possible_targets

    def __get_surround(self, y, x):
        surrounding = []
        image_len = len(self.__image)
        if y-1 > -1 and self.__image[y-1][x] > 0:
            surrounding.append([y-1,x])
        if y+1 < image_len and self.__image[y+1][x] > 0:
            surrounding.append([y+1,x])
        if x-1 > -1 and self.__image[y][x-1] > 0:
            surrounding.append([y,x-1])
        if x+1 < image_len and self.__image[y][x+1] > 0:
            surrounding.append([y,x+1])
        return surrounding

    @staticmethod
    def __build_image(width=10,height=10):
        return [[0]*width for i in range(height)]

    def __update_image(self, **kwargs):
        # new_image, boat_sizes, condition
        boat_sizes = kwargs['boat_sizes']
        new_image = kwargs['new_image']
        condition = kwargs['condition']
        image_len = len(self.__image)
        image_zone = range(image_len)
        for y in image_zone:
            for x in image_zone:
                if not condition(self.__image[y][x]):
                    continue
                for size in boat_sizes:
                    if x + (size-1) < image_len:
                        if all(condition(self.__image[y][inc]) for inc in range(x+1,x+size)):
                            for increment in range(size):
                                new_image[y][x+increment]+=1
                    if y + (size-1) < image_len:
                        if all(condition(self.__image[inc][x]) for inc in range(y+1,y+size)):
                            for increment in range(size):
                                new_image[y+increment][x]+=1
        self.__image = new_image

class Ship:
    def __init__(self, tag, name, size):
        self.tag = tag
        self.name = name
        self.__size = size
        self.__hits = 0
    
    def get_size(self):
        return self.__size

    def hit(self):
        self.__hits += 1
    
    def is_sunk(self):
        if self.__hits == self.__size:
            return self.__size
        return False

# Haven't Tested target
# Or place_ship 
class Board:
    # needs a method to handle a shot at the board
    def __init__(self, size=10, hit="~X~", miss="~O~", sea="~~~"):
        self.size = size
        self.__hit_place_holder = hit
        self.__miss_place_holder = miss
        self.__sea_place_holder = sea
        self.__locations = self.create_board()
    

    def create_board(self):
        return [[chr(65+j)+str(i+1) for i in range(self.size)] for j in range(self.size)]

    def target(self, x_idx, y_idx):
        value = self.__locations[y_idx][x_idx]
        if isinstance(value, str):
            if value == self.__hit_place_holder or value == self.__miss_place_holder:
                return dict(valid=True,executed=False,hit=False,sunk=False)
            else:
                self.__locations[y_idx][x_idx] = self.__miss_place_holder
                return dict(valid=True,executed=True,hit=False,sunk=False)
        else:
            value.hit()
            self.__locations[y_idx][x_idx] = self.__hit_place_holder
            return dict(valid=True,executed=True,hit=True,sunk=value.is_sunk())
    # if isinstance(self.__locations[y][x_idx],str)
    # make this a lambda function
    # or pass in a version of the board
    def empty_spaces(self, x, y, ship):
        results = []
        size = ship.get_size()
        if not -1 < x < self.size or not -1 < y < self.size: 
            return None, None
        if x + (size-1) < self.size:
            spaces = [self.__locations[y][x_idx] for x_idx in range(x,x+size) if isinstance(self.__locations[y][x_idx],str)]
            if len(spaces) == size:
                results.append(spaces)
        if x - (size-1) > -1:
            spaces = [self.__locations[y][x_idx] for x_idx in range(x-(size-1),x+1) if isinstance(self.__locations[y][x_idx],str)]
            if len(spaces) == size:
                results.append(spaces)
        if y + (size-1) < self.size:
            spaces = [self.__locations[y_idx][x] for y_idx in range(y,y+size) if isinstance(self.__locations[y_idx][x],str)]
            if len(spaces) == size:
                results.append(spaces)
        if y - (size-1) > -1:
            spaces = [self.__locations[y_idx][x] for y_idx in range(y-(size-1),y+1) if isinstance(self.__locations[y_idx][x],str)]
            if len(spaces) == size:
                results.append(spaces)
        if not results:
            return None, None
        def place_ship(choice):
            if not -1 < choice < len(results):
                return None
            for point in results[choice]:
                y_idx = ord(point[0])-65
                x_idx = int(point[1:])-1
                self.__locations[y_idx][x_idx] = ship
            return ship
        return results, place_ship

    # temporary until i find a home for this 
    def display_for_owner(self):
        outer = [0]*self.size
        for i in range(self.size):
            inner = [0]*self.size
            for j in range(self.size):
                if isinstance(self.__locations[i][j], Ship):
                    inner[j] = "~{}~".format(self.__locations[i][j].tag)
                else:
                    if not self.__locations[i][j][0].isalpha():
                        inner[j] = self.__locations[i][j]
                    else:
                        inner[j] = self.__sea_place_holder
            outer[i] = inner
        return outer
        # return ["|".join([self.__locations[i][j] if isinstance(self.__locations[i][j],str) else self.__locations[i][j].name for j in range(self.size)]) for i in range(self.size)]

    def display_for_opponent(self):
        outer = [0]*self.size
        for i in range(self.size):
            inner = [0]*self.size
            for j in range(self.size):
                if isinstance(self.__locations[i][j],str):
                    if not self.__locations[i][j][0].isalpha():
                        inner[j] = self.__locations[i][j]
                    else:
                        inner[j] = self.__sea_place_holder
                else:
                    inner[j] = self.__sea_place_holder
            outer[i] = inner
        return outer
        # return ["|".join([self.__locations[i][j] if isinstance(self.__locations[i][j],str) else chr(65+j)+str(i+1) for j in range(self.size)]) for i in range(self.size)]

# Questions
# Do i create a fully valid user before making an instance of the game
# Or Use get_current_player to check if that player is ready
# Need A game over method

class BattleShipGame:
    def __init__(self):
        self.players = []
        self.ship_classifications = []
        self.__current_turn = 0
        self.num_players = 0

    def add_player(self, player):
        self.players.append(player)
        self.num_players += 1

    def add_ship_clasification(self, tag, name, size):
        self.ship_classifications.append(dict(tag=tag,name=name,size=size))

    def get_current_player(self):
        return self.players[self.__current_turn]

    def get_opponent(self):
        return self.players[(self.__current_turn-1) % self.num_players]

    def display_opponents_board(self, opponent):
        return opponent.board.display_for_opponent()

    def display_player_board(self, player):
        return player.board.display_for_owner()

    def choose_ship_location(self, point, ship_spec, player):
        specs = self.ship_classifications[ship_spec]
        ship = Ship(specs['tag'], specs['name'], specs['size'])
        x,y = self.check_point(point, player.board)
        if x is None or y is None:
            return None, None
        return player.board.empty_spaces(x,y,ship)

    def check_point(self, point, board):
        x_in = int(point[1:])-1
        y_in = ord(point[0])-65
        if not -1 < y_in < board.size or not -1 < x_in < board.size:
            return None, None
        return x_in, y_in

    def add_ship_to_player(self, ship, player):
        # player = self.get_current_player()
        player.add_ship(ship)

    def fire_shot(self, target, opponent):
        # opponent = self.get_opponent()
        x, y = self.check_point(target, opponent.board)
        if x is None or y is None:
            print("Line 287")
            return dict(valid=False,executed=False,hit=False,sunk=False,target=target)
        # Fire The Shot
        result = opponent.board.target(x,y)
        result['target'] = target
        if result['executed']:
            self.end_turn()
            return result
        return result

    def end_turn(self):
        self.__current_turn = (self.__current_turn+1) % self.num_players

    def game_over(self):
        return any(player.fleet_sunk() for player in self.players)

