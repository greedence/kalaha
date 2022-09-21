# -*- coding: utf-8 -*-
"""
@author: Anonymous

"""

from time import sleep
from random import randrange
import matplotlib.pyplot as plt

''' --- CONSTANTS --- '''
PLAYER_ONE = 0 # used as a constant. 0 is used for player 1 due to Python indexing starts on 0
PLAYER_TWO = 1 # used as a constant. 1 is used for player 2 due to Python indexing starts on 0
GAME_TIED = 2 # used to represent the winner if a game is tied.
SINGLE_GAME = 0 # used as a constant for the first game (the only game in play-mode) of a list of games.
NEST = 0 # used as a constant to represent the first (index 0) cup of each player.

class GameManager:
    '''
    This is the main class for the game Kalaha. This game manager class shows
    a menu and from this class, one or more, games (class Board) are
    created and executed.

    The four main methods that can be used are called from this class.
    1: Play a game
    2: Simulate strategy
    3: See rules
    4: Quit game
    '''
    def __init__(self):
        '''
        Initialization of the GameManager class. A dictionary containing the
        game meny is created.
        '''
        self.menu = {'1': 'Play a game',
                     '2': 'Simulate strategy',
                     '3': 'See rules',
                     '4': 'Quit game'}

    def show_menu(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Enter a loop that will break when user chooses to quit, based on 
        user choice call corresponding methods.
    
        Returns
        -------
        None.
    
        '''
        exit_condition = False # loop until this condition is set to True
        while not exit_condition:
            # clear_console()
            print()
            print()
            print('----- Kalaha menu -----')
            print()
            for key in self.menu:
                print(str(key) + '. ' + self.menu[key])
            print()
            menu_choice = input('What do you want to do? ')
            if menu_choice == '1':
                self.play_a_game()
            elif menu_choice == '2':
                self.simulate_strategy()
            elif menu_choice == '3':
                self.see_rules()
            elif menu_choice == '4' or menu_choice.lower() == 'q':
                self._quit_game()
                exit_condition = True
            else:
                invalid_choice()

    def play_a_game(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Method used when a user wants to play a single game against either a
        computer or a human opponent.
        Create an instance of the Board object and call the method .play()
    
        Returns
        -------
        None.
    
        '''
        self._configure_players()
        self._configure_game()
        self.game = Board(self._player_one,
                          self._player_two,
                          self._starting_beads,
                          self._first_move)
        self.game.play()

        ''' Clean up '''
        del self.game

    def simulate_strategy(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Method used for simulating games between computer players with 
        different strategies.
        Configure two computer players, and start looping over the number
        of games the user wants to simulate.
        After all games have been simulated, show statistics.
    
        Returns
        -------
        None.
    
        '''
        self.games = []
        self._configure_ais()
        self._configure_game()
        for game_no in range(self._no_of_games):
            self.games.append(Board(self._player_one,
                                    self._player_two,
                                    self._starting_beads,
                                    self._first_move))
        for game_no in range(self._no_of_games):
            self.games[game_no].play()
        self._show_statistics()

        ''' Clean up '''
        del self.games

    def see_rules(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Read rules from file and display them to the user.
    
        Returns
        -------
        None.
    
        '''
        try:
            print()
            print()
            with open('kalaha_rules.txt') as h:
                for line in h:
                    print(line)
            print()
            input('Press \'Enter\' to return.')
        except OSError:
            print()
            print('Cannot open file \'kalaha_rules.txt\'.')
            sleep(2)

    def _quit_game(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Thank the user for playing.
    
        Returns
        -------
        None.
    
        '''
        print()
        print('Thank you for playing Kalaha.')
    
    def _show_statistics(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Calculate how many wins and tied games the simulation has yielded.
        Print statistics to screen.
        Use matplotlib.pyplot to create a .pdf-file with a bar figure.
    
        Returns
        -------
        None.
    
        '''
        p1_wins = 0 # The number of simulated games won by player 1
        p2_wins = 0 # The number of simulated games won by player 2
        p_ties = 0 # The number of simulated games tied
        for game_number in range(len(self.games)):
            if self.games[game_number].winner == PLAYER_ONE:
                p1_wins += 1
            elif self.games[game_number].winner == PLAYER_TWO:
                p2_wins += 1
            elif self.games[game_number].winner == GAME_TIED:
                p_ties += 1

        print()
        print('Player one wins ' + str(p1_wins) + ' times.')
        print('Player two wins ' + str(p2_wins) + ' times.')
        print('The game is tied  ' + str(p_ties) + ' times.')

        # create the pdf with the plot
        try:
            plt.title('Kalaha experiment')
            plt.ylabel('Number of wins')
            plt.xlabel('Player')
            plt.bar(['Player 1',
                     'Player 2',
                     'Tied games'],
                    [p1_wins, p2_wins, p_ties])
            plt.savefig('kalaha_simulation.pdf')
            print()
            print('A plot was created in file \'kalaha_simulation.pdf\'')
        except:
            print()
            print('Kalaha strategy simulation could not create file.')

        print()
        input('Press \'Enter\' to return.')

    def _configure_players(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Ask the user for the player configuration.
        Possible choices will be:
            1. Human vs Human
            2. Human vs Computer (Strategy 1)
            3. Human vs Computer (Strategy 2)
            4. Computer (Strategy 1) vs Human
            5. Computer (Strategy 2) vs Human
    
        Returns
        -------
        None.
    
        '''
        if ask_player_is_human(PLAYER_ONE):
            ''' Human vs ... '''
            self._player_one = Player(PLAYER_ONE) 
            if ask_player_is_human(PLAYER_TWO):
                ''' Human vs Human '''
                self._player_two = Player(PLAYER_TWO) 
            else:
                ''' Human vs Computer '''
                self._player_two = AI(PLAYER_TWO)
                self._player_two.strategy = ask_ai_strategy(PLAYER_TWO)
        else:
            ''' Computer vs Human '''
            self._player_one = AI(PLAYER_ONE) 
            self._player_one.strategy = ask_ai_strategy(PLAYER_ONE)
            self._player_two = Player(PLAYER_TWO) 
        
    def _configure_ais(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Ask the user for the player configuration.
        Possible choices will be:
            1. Computer (Strategy 1) vs Computer (Strategy 1)
            2. Computer (Strategy 1) vs Computer (Strategy 2)
            3. Computer (Strategy 2) vs Computer (Strategy 1)
            4. Computer (Strategy 2) vs Computer (Strategy 2)
    
        Returns
        -------
        None.
    
        '''
        self._player_one = AI(PLAYER_ONE) 
        self._player_one.strategy = ask_ai_strategy(PLAYER_ONE)
        self._player_two = AI(PLAYER_TWO)
        self._player_two.strategy = ask_ai_strategy(PLAYER_TWO)
        self._no_of_games = ask_no_of_games()
        
    def _configure_game(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Ask the user for the number of beads to start with in each cup.
        Ask the user for which player starts the game.
    
        Returns
        -------
        None.
    
        '''
        self._starting_beads = ask_starting_beads()
        self._first_move = ask_first_move()

class Board:
    '''
    This is the class that creates and executes a single game of Kalaha. This
    class is in itself enough to create and play a Kalaha game.
    '''
    def __init__(self, player_one, player_two, starting_beads, first_move):
        '''

        Parameters
        ----------
        player_one : Player or AI object
            The boards player one object.
        player_two : Player or AI object
            The boards player two object.
        starting_beads : integer
            The number of beads the game shall start with in each cup.
        first_move : integer
            0 (player one) or 1 (player two). Which player shall start the game.

        Returns
        -------
        None.

        '''
        self.players = [player_one, player_two]
        self.cups = [[0] + 6 * [starting_beads], [0] + 6 * [starting_beads]]
        self._current_player = first_move

    def play(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Method called to start the game. The loop will iterate until a
        victory condition is met.
        Each iteration marks a players turn.
        If at least one player is human, before each turn, show the game board.
        When victory condition is met, end the game.
    
        Returns
        -------
        None.
    
        '''
        victory_condition = False # loop until victory condition is True
        while not victory_condition:
            if not self._is_ai_game():
                self.show()
            victory_condition = self.make_a_turn()
        self._end_game()

    def show(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Prints the current state of the game board to the screen. Calls
        format_cup() function to create the strings to print.
        There will be 3 strings created, one for each row of the game board.
    
        Returns
        -------
        None.
    
        '''
        print()
        print('Player 1 is on the top row with the nest on the left.')
        print('Player 2 is on the bottom row with the nest on the right.')
        print()
        print('The board looks like this:')
        print()
        row_1 = 3 * ' '
        for i in range(1, 7):
            row_1 += format_cup(self.cups[PLAYER_ONE][i])
        row_2 = format_cup(self.cups[PLAYER_ONE][NEST]) + (18 * ' ') + format_cup(self.cups[PLAYER_TWO][NEST])
        row_3 = 3 * ' '
        for i in range(6, 0, -1):
            row_3 += format_cup(self.cups[PLAYER_TWO][i])
        print(row_1)
        print(row_2)
        print(row_3)
    
    def make_a_turn(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Method called to drop beads in cups. The main loop:
            1. drops a bead in a cup
            2. configures next iteration
            3. checks victory condition
    
        Returns
        -------
        victory_condition : bool
            Will be True when there are no beads left in hand and the
            current players cups are all empty save for the nest.
    
        '''
        # Start a new turn by picking up beads
        victory_condition = False
        current_side = self._current_player # start every turn on the side of the player whos turn it is
        current_cup = self._choose_a_cup() # start every turn by asking for a cup
        beads_in_hand = self._pick_up_beads(current_side, current_cup) # pick up those beads
        current_side, current_cup = self._change_cup(current_side, current_cup) # go to the next cup
        # The main purpose of every loop is to drop a bead in a cup
        while not beads_in_hand == 0:
            # all cups except opponents nest
            if not self._is_opponents_nest(current_side, current_cup):
                # drop a bead
                beads_in_hand = self._drop_a_bead(beads_in_hand,
                                                  current_side,
                                                  current_cup)
            # when last bead on hand has been dropped (in own nest or a small cup)
            if beads_in_hand == 0:
                # check if victory condition is met
                victory_condition = self.check_victory_condition()
                # last bead was dropped, but not in own nest
                if not (current_cup == 0 and current_side == self._current_player):
                    # swap player
                    self._current_player = toggle_bit(self._current_player)
                    # end turn
                # last bead was dropped, in own nest
                else:
                    # do not swap player
                    # tell user it is his/hers turn again
                    if not victory_condition and not self._is_ai_game():
                        print()
                        print('The last bead was put in your own nest, please go again.')
                    # end turn
            # if there are still beads in hand (the last bead was not dropped 
            # in opponents nest)
            else:
                # swap cup
                current_side, current_cup = self._change_cup(current_side, current_cup)
                # continue turn
        return victory_condition
    
    def _is_ai_game(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Checks if player objects are AI object types.
    
        Returns
        -------
        bool
            True if both players are computer players.
            False otherwise.
    
        '''
        if type(self.players[PLAYER_ONE]) is AI and type(self.players[PLAYER_TWO]) is AI:
            return True
        else:
            return False

    def check_victory_condition(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Checks if the current players cups add up to zero. If they do, 
        take all the beads from the opponents side and put in the
        his or her nest.
    
        Returns
        -------
        bool
            True if victory condition is met.
            False otherwise.
    
        '''
        sum_of_beads = 0 # the number of beads in the current players cups (excluding his or her nest)
        for cup in range(1,7):
            sum_of_beads += self.cups[self._current_player][cup]
        if sum_of_beads == 0:
            for cup in range(1,7):
                sum_of_beads += self.cups[toggle_bit(self._current_player)][cup]
                self.cups[toggle_bit(self._current_player)][cup] = 0
            self.cups[toggle_bit(self._current_player)][NEST] += sum_of_beads
            return True
        else:
            return False

    def _end_game(self):
        '''
        
        Parameters
        ----------
        None.
    
        Algorithm
        ---------
        Checks which player has the most beads in his/her nest and sets
        that player to be the winner.
        If there are at least one human player, print the result to screen.
    
        Returns
        -------
        None.
    
        '''
        if self.cups[PLAYER_ONE][NEST] > self.cups[PLAYER_TWO][NEST]:
            self.winner = PLAYER_ONE
        elif self.cups[PLAYER_ONE][NEST] < self.cups[PLAYER_TWO][NEST]:
            self.winner = PLAYER_TWO
        elif self.cups[PLAYER_ONE][NEST] == self.cups[PLAYER_TWO][NEST]:
            self.winner = GAME_TIED
        if not self._is_ai_game():
            self.show()
            print()
            if self.winner == PLAYER_ONE:
                print('The winner is Player 1 with ' + str(self.cups[PLAYER_ONE][NEST]) + ' beads.')
            elif self.winner == PLAYER_TWO:
                print('The winner is Player 2 with ' + str(self.cups[PLAYER_TWO][NEST]) + ' beads.')
            elif self.winner == GAME_TIED:
                print('The game is a draw.')
            print()
            input('Press \'Enter\' to return.')

    def _pick_up_beads(self, current_side, current_cup):
        '''
        
        Parameters
        ----------
        current_side : integer
            The side of the board where beads are currently being picked
            up and dropped.
        current_cup : integer
            The cup next in turn from which to pick up beads.
    
        Algorithm
        ---------
        Picks up all beads in the current cup on the current side.
        
        Returns
        -------
        beads_in_hand : integer
            The number of beads picked up.

        '''
        beads_in_hand = self.cups[current_side][current_cup]
        self.cups[current_side][current_cup] = 0
        return beads_in_hand

    def _change_cup(self, current_side, current_cup):
        '''
        
        Parameters
        ----------
        current_side : integer
            The side of the board where beads are currently being picked
            up and dropped.
        current_cup : integer
            The cup next in turn from which to pick up beads.

        Algorithm
        ---------
        Changes the current cup to the next one in turn (-1) or if current
        cup is a nest it changes current side and sets current cup to 6.

        Returns
        -------
        current_side : integer
            The side of the board where beads are currently being picked
            up and dropped.
        current_cup : integer
            The cup next in turn from which to pick up beads.

        '''
        if current_cup == 0:
            current_side = toggle_bit(current_side)
            current_cup = 6
        else:
            current_cup -= 1
        return current_side, current_cup

    def _drop_a_bead(self, beads_in_hand, current_side, current_cup):
        '''
        
        Parameters
        ----------
        beads_in_hand : integer
            The number of beads currently in players hand.
        current_side : integer
            The side of the board where beads are currently being picked
            up and dropped.
        current_cup : integer
            The cup next in turn from which to pick up beads.

        Algorithm
        ---------
        Increment number of beads in the current cup.
        Decrement number of beads in hand.

        Returns
        -------
        beads_in_hand : integer
            The number of beads currently in players hand after one
            has been dropped in a cup.

        '''
        self.cups[current_side][current_cup] += 1
        beads_in_hand -= 1
        return beads_in_hand

    def _choose_a_cup(self):
        '''
        
        Parameters
        ----------
        None.
        
        Algorithm
        ---------
        If the current player is a human player, he/she will be asked to 
        choose a cup.
        If the current player is a computer player, a cup will be chosen based
        on the players strategy.
        If any player in the game is human, print user choice to screen.

        Returns
        -------
        current_cup : integer
            The cup chosen by the user.

        '''
        if type(self.players[self._current_player]) is Player:
            current_cup = ask_for_a_move(self._current_player,
                                         self.cups[self._current_player])
        elif type(self.players[self._current_player]) is AI:
            current_cup = choose_cup_based_on_strategy(self.players[self._current_player].strategy,
                                                       self.cups[self._current_player])
        if not self._is_ai_game():
            print()
            if type(self.players[self._current_player]) is Player:
                print('Your choice of cup was number:', current_cup)
            else:
                print('The computer chose cup number:', current_cup)
        return current_cup

    def _is_opponents_nest(self, current_side, current_cup):
        '''
        
        Parameters
        ----------
        current_side : integer
            The side of the board where beads are currently being picked
            up and dropped.
        current_cup : integer
            The cup next in turn from which to pick up beads.

        Algorithm
        ---------
        Check if current cup is a nest and if the current side is the 
        opponents side.

        Returns
        -------
        bool
            Returns True if the current cup is the opponents nest
            and False otherwise

        '''
        if current_cup == 0 and current_side != self._current_player:
            return True
        else:
            return False

class Player:
    '''
    This class represents a human player and is the super class for the AI player.
    '''
    def __init__(self, player_number):
        '''
        
        Parameters
        ----------
        player_number : integer
            0 (player one) or 1 (player two). Which player shall start the game.

        Returns
        -------
        None.

        '''
        self.player_number = player_number

class AI(Player):
    '''
    This class represents a computer player and inherits from the Player class.
    It contains also the chosen strategy for the computer player.
    '''
    def __init__(self, player_number):
        '''
        
        Parameters
        ----------
        player_number : integer
            0 (player one) or 1 (player two). Which player shall start the game.

        Returns
        -------
        None.

        '''
        super().__init__(player_number)
        self.strategy = None

def toggle_bit(bit):
    '''
    
    Parameters
    ----------
    bit : integer
        Can take on the value 0 or 1.

    Algorithm
    ---------
    Toggle the 0 to a 1 or the 1 to a 0.

    Returns
    -------
    bit : integer
        The toggled bit.

    '''
    if bit == 1: return 0
    elif bit == 0: return 1

def clear_console():
    '''
    
    Parameters
    ----------
    None.
    
    Algorithm
    ---------
    Clears the console and prints a Kalaha headline.

    Returns
    -------
    None.

    '''
    print('\033[H\033[J')
    print()
    print('----- Kalaha -----')

def invalid_choice():
    '''
    
    Parameters
    ----------
    None.
    
    Algorithm
    ---------
    Prints out that a choice that has been made is invalid and then sleeps
    for two seconds.

    Returns
    -------
    None.

    '''
    # clear_console()
    print()
    print('Invalid choice, try again...')
    sleep(2)

def format_cup(beads):
    '''
    
    Parameters
    ----------
    beads : integer
        The number of beads to be formatted as a 3 char string.

    Algorithm
    ---------
    Format the supplied integer to a 3 char string by filling blankspaces
    in the beginning of the string.

    Returns
    -------
    breads : string
        A formatted version of the supplied number of beads.

    '''
    if beads > 9:
        return ' ' + str(beads)
    elif beads <= 9:
        return '  ' + str(beads)
    
def is_input_integer(user_input):
    '''
    
    Parameters
    ----------
    user_input : string
        A user choice from an input command.

    Algorithm
    ---------
    Try to type cast the string to an integer. If it works, return True, but
    if an exception is raised, return False.

    Returns
    -------
    bool
        True if the string input can be type cast to an integer, False
        otherwise.

    '''
    try:
        int(user_input)
        return True
    except:
        return False

def ask_starting_beads():
    '''
    
    Parameters
    ----------
    None.
    
    Algorithm
    ---------
    Ask the user to choose from 3 to 6 starting beads.
    

    Returns
    -------
    beads : integer
        Returns the users choice of starting beads (3 - 6).

    '''
    # Ask user for the starting number of beads in each cup. 
    while True:
        starting_beads = input('How many beads do you want in each cup (3 - 6)? ')
        if is_input_integer(starting_beads) and int(starting_beads) >= 3 and int(starting_beads) <= 6:
            return int(starting_beads)
        else:
            invalid_choice()
            
def ask_player_is_human(player_number):
    '''
    
    Parameters
    ----------
    player_number : integer
        Player number one har the number 0 and player number two
        has the number 1.

    Algorithm
    ---------
    Ask the user if he/she wants the player to be a human player.

    Returns
    -------
    bool
        True if the user answers 'y' and False if the user answers 'n'.

    '''
    # Ask user if player is human or AI.
    while True:
        player_is_human = input('Is player ' + str(player_number + 1) + ' human (Y or N)? ')
        if player_is_human.lower() == 'y':
            return True
        elif player_is_human.lower() == 'n':
            return False
        else:
            invalid_choice()

def ask_ai_strategy(player_number):
    '''
    
    Parameters
    ----------
    player_number : integer
        Player number one har the number 0 and player number two
        has the number 1.

    Algorithm
    ---------
    Ask user for the computer players strategy.

    Returns
    -------
    ai_strategy : integer
        Strategy 1 or strategy 2 based on user input.

    '''
    # Ask user for AI strategy.
    while True:
        ai_strategy = input('What is the strategy of player ' + str(player_number + 1) + ' (1 or 2)? ')
        if is_input_integer(ai_strategy) and int(ai_strategy) >= 1 and int(ai_strategy) <= 2:
            return int(ai_strategy)
        else:
            invalid_choice()

def ask_no_of_games():
    '''
    
    Parameters
    ----------
    None.
    
    Algorithm
    ---------
    Ask the user how many games that should be simulated.

    Returns
    -------
    no_of_games : integer
        The number of games to be simulated.

    '''
    # Ask user how many games to play.
    while True:
        no_of_games = input('How many games do you want to simulate (1 - 1000)? ')
        if is_input_integer(no_of_games) and int(no_of_games) >= 1 and int(no_of_games) <= 1000:
            return int(no_of_games)
        else:
            invalid_choice()

def ask_first_move():
    '''
    
    Parameters
    ----------
    None.
    
    Algorithm
    ---------
    Ask the user which player shall start the game.

    Returns
    -------
    first_move : integer
        Returns 0 if player one chall start the game.
        Returns 1 if player two shall start the game.

    '''
    # Ask user for which player shall start the game.
    while True:
        first_move = input('Which player shall start the game (1 or 2)? ')
        if is_input_integer(first_move) and (int(first_move) == 1 or int(first_move) == 2):
            return int(first_move) - 1 # the number 0 if player 1 and the number 1 if player 2
        else:
            invalid_choice()

def ask_for_a_move(player_number, cups):
    '''
    
    Parameters
    ----------
    player_number : integer
        Player number one har the number 0 and player number two
        has the number 1.
    cups : list
        A list with 7 elements representing the players cups.

    Algorithm
    ---------
    Ask the user for which cup to puck up beads from. Make sure the user
    has chosen a non-empty cup.

    Returns
    -------
    cup_number : integer
        Returns the chosen cup.

    '''
    # Ask user to choose a cup.
    while True:
        user_input = input('Player ' + str(player_number + 1) + ', which cup do you choose (1 - 6, 1 is closest to your nest):? ')
        if is_input_integer(user_input) and int(user_input) in check_non_empty_cups(cups):
            return int(user_input)
        else:
            invalid_choice()

def check_non_empty_cups(cups):
    '''
    
    Parameters
    ----------
    cups : list
        A list with 7 elements representing the players cups.

    Algorithm
    ---------
    Create a list whose elements mark the cup numbers where the supplied
    list has non-empty cups.

    Returns
    -------
    out_list : list
        A list whose elements mark the cup numbers where the supplied
    list has non-empty cups.

    '''
    out_list = []
    for i in range(1, 7): # Check elements 1 - 6 (element 0 is the players Nest)
        if cups[i] > 0:
            out_list.append(i) # Add the element index to the out list
    return out_list

def check_max_cups(cups):
    '''
    
    Parameters
    ----------
    cups : list
        A list with 7 elements representing the players cups.

    Algorithm
    ---------
    1. Start with max_beads from the second element of the supplied list. The first
    element is the players nest and shall be ignored.
    2. Loop over elements 2 - 7 (representing cup number 1 - 6) and check if any 
    number is greater than the max_beads number.
    3. Create a list with all the cup numbers that
    hold max_beads (might be only one) number of beads.
    4. Return that list.

    Returns
    -------
    out_list : list
        A list with all the cup numbers that hold max_beads number of beads.

    '''
    out_list = []
    max_beads = cups[1]
    for i in range(1, 7): # Check elements 1 - 6 (element 0 is the players Nest)
        if cups[i] > max_beads:
            max_beads = cups[i]
    for i in range(1, 7): # Check elements 1 - 6 (element 0 is the players Nest)
        if cups[i] == max_beads:
            out_list.append(i)
    return out_list

def choose_cup_based_on_strategy(player_strategy, cups):
    '''
    
    Parameters
    ----------
    player_strategy : integer
        The strategy of the relevant computer player.
    cups : list
        A list with 7 elements representing the players cups.

    Algorithm
    ---------
    If the computer strategy is 1, choose randomly from all non-empty cups.
    If the computer strategy is 2, choose randomly from the cups with the most
    number of beads (can be only one).

    Returns
    -------
    cup_number : integer
        The randomly chosen cup number.

    '''
    valid_cups = []
    if player_strategy == 1:
        valid_cups = check_non_empty_cups(cups)
    if player_strategy == 2:
        valid_cups = check_max_cups(cups)
    return valid_cups[randrange(0, len(valid_cups))]
