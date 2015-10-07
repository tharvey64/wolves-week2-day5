class View:
    def __init__(self):
       pass

    def welcome_screen(self):
        print("Welcome to Battleship.")

    def start_new_game(self):
        print("_"*75)
        print("Would you like to start a new game? (y or n)")
        return input()

    def single_or_multiplayer(self):
        print("_"*75)
        print("Enter the number of players:")
        return input()

    def get_player_name(self, number):
        print("_"*75)
        print("Please enter your name player {}: ".format(number))
        return input()

    def fleet_status(self):
        print("_"*75)
        print("Before we begin, you must position your fleet strategically.")
        print("Your armada consists of an aircraft carrier, battleship, submarine, destroyer and patrol boat.")
        # print("Are you ready for battle?")

    def position_starting_coordinate(self, ship):
        print("_"*75)
        print("Enter the coordinates to place your {name}:({size} spaces)".format(**ship))
        return input()

    def position_selection(self, options):
        print("_"*75)
        print("Select the position you would like:")
        for idx in range(len(options)):
            print("{}: {}".format(idx, options[idx]))
        return input()

    def enter_firing_coordinates(self):
        print("_"*75)
        print("Enter the location to fire upon:")
        return input()

    def coordinates_invalid(self):
        print("_"*75)
        print("The coordinates you have entered are invalid.")

    def previous_target(self):
        print("_"*75)
        print("You have already fired at this position.\nWe advise that you select another position.")

    def target_missed(self):
        print("_"*75)
        print("Your shot was off-target.")

    def target_hit(self):
        print("_"*75)
        print("Bullseye!")

    def ship_sunk(self):
        print("_"*75)
        print("A ship has been sunk!")

    def defeat_game_over(self):
        print("_"*75)
        print("Your ships are gone!\nGame over!")

    def victory_game_over(self):
        print("_"*75)
        print("You sank all of the enemy's ships.  The day is won!")
    
    def display_game(self, player_name, current_board):
        print("_"*75)
        letters = ['A','B','C','D','E','F','G','H','I','J']
        print("\t {}".format(player_name))
        print(" |"+(" {} |"*9 + " {}").format(*list(range(1,11))))
        for idx in range(len(current_board)):
            print(letters[idx]+"|" + "|".join(current_board[idx]))
        input()
