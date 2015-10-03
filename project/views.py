class View:
    def __init__(self):
       pass
    def welcome_screen(self):
        print("Welcome to Battleship.")

    def start_new_game(self):
        print("Would you like to start a new game? (y or n)")
        return input()

    def get_player_name(self, number):
        print("Please enter your name player {}: ".format(number))
        return input()

    def fleet_status(self):
        print("Before we begin, you must position your fleet strategically.")
        print("Your armada consists of an aircraft carrier, battleship, submarine, destroyer and patrol boat.")
        # print("Are you ready for battle?")

    def position_starting_coordinate(self):
        print("Enter the coordinates to place your ship:")
        return input()

    def position_selection(self, options):
        print("Select the position you would like:")
        print(options)
        return input()
    def enter_firing_coordinates(self):
        print("Enter the location to fire upon:")
        return input()

    def coordinates_invalid(self):
        print("The coordinates you have entered conflict with a previous set which was entered.")

    def previous_target(self):
        print("You have already fired at this position.  We advise that you select another position.")

    def target_missed(self):
        print("Your shot was off-target.")

    def target_hit(self):
        print("Bullseye!")

    def ship_sunk(self):
        print("A ship has been sunk!")

    def defeat_game_over(self):
        print("Your ships are gone!  Game over!")

    def victory_game_over(self):
        print("You sank all of the enemy's ships.  The day is won!")
    
    def display_game(self, current_board):
        [print("".join(line)) for line in current_board]

