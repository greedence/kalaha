# -*- coding: utf-8 -*-
"""
@author: Anonymous

"""

import unittest
import unittest.mock

import kalaha_library

class TestKalahaLibrary(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        classmethod setUpClass is run once befora all tests.
        """

    @classmethod
    def tearDownClass(cls):
        """
        classmethod tearDownClass is run once befora all tests.
        """
        pass
    
    def setUp(self):
        """
        method setUp is run once befora every test.
        """
        pass
 
    def tearDown(self):
        """
        method tearDown is run once befora every test.
        """
        pass

    def test_check_victory_condition(self):
        '''
        
        Algorithm
        ---------
        Tests if victory condition is met. If all cups on either side are empty
        assert True, assert False otherwise.
        
        Returns
        -------
        None.

        '''
        board = kalaha_library.Board(kalaha_library.Player(kalaha_library.PLAYER_ONE), kalaha_library.AI(kalaha_library.PLAYER_TWO), 3, kalaha_library.PLAYER_ONE)
        board.cups = [[0, 3, 3, 3, 3, 3, 3], [0, 3, 3, 3, 3, 3, 3]]
        self.assertFalse(board.check_victory_condition())
        board.cups = [[0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 3, 3, 3]]
        self.assertTrue(board.check_victory_condition())
        
        
    def test_make_a_turn(self):
        '''
        
        Algorithm
        ---------
        Testing a single move.

        Returns
        -------
        None.

        '''
        board = kalaha_library.Board(kalaha_library.Player(kalaha_library.PLAYER_ONE), kalaha_library.AI(kalaha_library.PLAYER_TWO), 3, kalaha_library.PLAYER_ONE)
        board.cups = [[0, 3, 3, 3, 3, 3, 3], [0, 3, 3, 3, 3, 3, 3]]
        with unittest.mock.patch('builtins.input', return_value = '4'):
            self.assertEqual(board.make_a_turn(), False)
        self.assertEqual(board.cups[0], [0, 4, 4, 4, 0, 3, 3])
        self.assertEqual(board.cups[1], [0, 3, 3, 3, 3, 3, 3])

    def test_play_a_game(self):
        '''
        
        Algorithm
        ---------
        Testing a whole game based on the moves in the file test_moves.txt.

        Returns
        -------
        None.

        '''
        board = kalaha_library.Board(kalaha_library.Player(kalaha_library.PLAYER_ONE), kalaha_library.Player(kalaha_library.PLAYER_TWO), 6, kalaha_library.PLAYER_ONE)
        try:
            with open('test_moves.txt', 'r') as h:
                moves = h.readline()
                for move in moves.split(','):
                    with unittest.mock.patch('builtins.input', return_value = str(move)):
                        board.make_a_turn()
                self.assertEqual(board.cups[kalaha_library.PLAYER_ONE][kalaha_library.NEST], 48)
                self.assertEqual(board.cups[kalaha_library.PLAYER_TWO][kalaha_library.NEST], 24)
        except:
            print('play a game - test failed')

    def test_run_simulations(self):
        '''
        
        Algorithm
        ---------
        Testing all variant of computer simulations and creating an output file
        to show the percentage of wins and ties. Used for analysis.

        Returns
        -------
        None.

        '''
        # a list containing 32 lists (configurations). Each list describes:
        # pos 0: strategy of player one
        # pos 1: strategy of player two
        # pos 2: number of starting beads
        # pos 3: which player starts the game
        sim_configs =  [[1, 1, 3, 1],
                        [1, 2, 3, 1],
                        [2, 1, 3, 1],
                        [2, 2, 3, 1],
                        [1, 1, 3, 2],
                        [1, 2, 3, 2],
                        [2, 1, 3, 2],
                        [2, 2, 3, 2],
                        [1, 1, 4, 1],
                        [1, 2, 4, 1],
                        [2, 1, 4, 1],
                        [2, 2, 4, 1],
                        [1, 1, 4, 2],
                        [1, 2, 4, 2],
                        [2, 1, 4, 2],
                        [2, 2, 4, 2],
                        [1, 1, 5, 1],
                        [1, 2, 5, 1],
                        [2, 1, 5, 1],
                        [2, 2, 5, 1],
                        [1, 1, 5, 2],
                        [1, 2, 5, 2],
                        [2, 1, 5, 2],
                        [2, 2, 5, 2],
                        [1, 1, 6, 1],
                        [1, 2, 6, 1],
                        [2, 1, 6, 1],
                        [2, 2, 6, 1],
                        [1, 1, 6, 2],
                        [1, 2, 6, 2],
                        [2, 1, 6, 2],
                        [2, 2, 6, 2]]
        try:
            h = open('simulations.txt', 'w')
            h.write('P.1 str. & P.2 str. & Beads & Start & P.1 wins & P.2 wins & Ties' + '\\' + '\\' + '\n')
            for i in range(len(sim_configs)):
                p1_wins = 0
                p2_wins = 0
                p_ties = 0
                # run 1000 simulations per configuration (32000 simulations in total)
                for j in range(100):
                    board = kalaha_library.Board(kalaha_library.AI(kalaha_library.PLAYER_ONE), kalaha_library.AI(kalaha_library.PLAYER_TWO), sim_configs[i][2], sim_configs[i][3] - 1)
                    board.players[kalaha_library.PLAYER_ONE].strategy = sim_configs[i][0]
                    board.players[kalaha_library.PLAYER_TWO].strategy = sim_configs[i][1]
                    board.play()
                    if board.winner == kalaha_library.PLAYER_ONE:
                        p1_wins += 1
                    elif board.winner == kalaha_library.PLAYER_TWO:
                        p2_wins += 1
                    elif board.winner == kalaha_library.GAME_TIED:
                        p_ties += 1
                h.write(str(sim_configs[i][0]) + ' & ' + str(sim_configs[i][1]) + ' & ' + str(sim_configs[i][2]) + ' & ' + str(sim_configs[i][3]) + ' & ' + str(p1_wins) + '$\%$ & ' + str(p2_wins) + '$\%$ & ' + str(p_ties) + '$\%$' + '\\' + '\\' + '\n')
            h.close()
        except:
            print('run_simulations - writing to file failed')

    def test_pick_up_beads(self):
        '''
        
        Algorithm
        ---------
        Testing that picking up beads from a cup gives the right number
        of beads.

        Returns
        -------
        None.

        '''
        board = kalaha_library.Board(kalaha_library.Player(kalaha_library.PLAYER_ONE), kalaha_library.AI(kalaha_library.PLAYER_TWO), 3, kalaha_library.PLAYER_ONE)
        board.cups = [[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6]]
        self.assertEqual(board._pick_up_beads(kalaha_library.PLAYER_ONE, 5), 5)
        board.cups = [[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 9, 4, 5, 6]]
        self.assertEqual(board._pick_up_beads(kalaha_library.PLAYER_TWO, 3), 9)

    def test_drop_a_bead(self):
        '''
        
        Algorithm
        ---------
        Testing that dropping a bead in a cup increments that cup.

        Returns
        -------
        None.

        '''
        board = kalaha_library.Board(kalaha_library.Player(kalaha_library.PLAYER_ONE), kalaha_library.AI(kalaha_library.PLAYER_TWO), 3, kalaha_library.PLAYER_ONE)
        board.cups = [[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6]]
        self.assertEqual(board._drop_a_bead(10, kalaha_library.PLAYER_ONE, 3), 9)

    def test_choose_a_cup(self):
        '''
        
        Algorithm
        ---------
        Testing that chosing a specific cup returns that value.

        Returns
        -------
        None.

        '''
        board = kalaha_library.Board(kalaha_library.Player(kalaha_library.PLAYER_ONE), kalaha_library.AI(kalaha_library.PLAYER_TWO), 3, kalaha_library.PLAYER_ONE)
        with unittest.mock.patch('builtins.input', return_value = '1'):
            self.assertEqual(board._choose_a_cup(), 1)
    
    def test_is_opponents_nest(self):
        '''
        
        Algorithm
        ---------
        Testing if supplied board side and cup number is the opponents nest.

        Returns
        -------
        None.

        '''
        board = kalaha_library.Board(kalaha_library.Player(kalaha_library.PLAYER_ONE), kalaha_library.AI(kalaha_library.PLAYER_TWO), 3, kalaha_library.PLAYER_ONE)
        board.cups = [[0, 1, 2, 3, 4, 5, 6], [1, 1, 2, 3, 4, 5, 6]]
        self.assertEqual(board._is_opponents_nest(0, 0), False)
        self.assertEqual(board._is_opponents_nest(1, 0), True)
        self.assertEqual(board._is_opponents_nest(0, 1), False)
        self.assertEqual(board._is_opponents_nest(1, 1), False)
    
    def test_toggle_bit(self):
        '''
        
        Algorithm
        ---------
        Testing that 1 is returned if 0 is supplied and the other way around.

        Returns
        -------
        None.

        '''
        board = kalaha_library.Board(kalaha_library.Player(kalaha_library.PLAYER_ONE), kalaha_library.AI(kalaha_library.PLAYER_TWO), 3, kalaha_library.PLAYER_ONE)
        board.cups = [[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6]]
        self.assertEqual(kalaha_library.toggle_bit(kalaha_library.PLAYER_ONE), kalaha_library.PLAYER_TWO)

    def test_is_input_integer(self):
        '''
        
        Algorithm
        ---------
        Testing if supplied argument is an integer (in string format) or not.

        Returns
        -------
        None.

        '''
        self.assertFalse(kalaha_library.is_input_integer([]))
        self.assertFalse(kalaha_library.is_input_integer(''))
        self.assertFalse(kalaha_library.is_input_integer('foo'))
        self.assertTrue(kalaha_library.is_input_integer('1'))
        self.assertTrue(kalaha_library.is_input_integer('2'))
        self.assertTrue(kalaha_library.is_input_integer('3'))
        self.assertTrue(kalaha_library.is_input_integer('4'))

    def test_format_cup(self):
        '''
        
        Algorithm
        ---------
        Testing that the funtion returns a 3 char long string.

        Returns
        -------
        None.

        '''
        self.assertEqual(kalaha_library.format_cup(2), '  2')
        self.assertEqual(kalaha_library.format_cup(10), ' 10')

    def test_check_non_empty_cups(self):
        '''
        
        Algorithm
        ---------
        Testing that only non-empty positions are returns in a list.

        Returns
        -------
        None.

        '''
        self.assertEquals(kalaha_library.check_non_empty_cups([0, 2, 3, 6, 0, 1, 4]), [1, 2, 3, 5, 6])

    def test_check_max_cups(self):
        '''
        
        Algorithm
        ---------
        Testing that the positions of the largest element(s) are returned.

        Returns
        -------
        None.

        '''
        self.assertEquals(kalaha_library.check_max_cups([0, 2, 3, 4, 0, 1, 4]), [3, 6])
        self.assertEquals(kalaha_library.check_max_cups([0, 2, 3, 4, 0, 1, 1]), [3])
        self.assertEquals(kalaha_library.check_max_cups([5, 2, 3, 4, 0, 1, 1]), [3])
    
    def test_choose_cup_based_on_strategy(self):
        '''
        
        Algorithm
        ---------
        Testing that the random value is in the right range and that it never,
        or at least in a 1000 tries, does not return a position where the 
        element is zero for strategy 1 or a non-max value for strategy 2.

        Returns
        -------
        None.

        '''
        self.assertTrue(kalaha_library.choose_cup_based_on_strategy(1, [0, 2, 3, 4, 0, 1, 4]) in range(1, 7))
        for i in range(1000):
            self.assertNotEqual(kalaha_library.choose_cup_based_on_strategy(1, [0, 2, 3, 4, 0, 1, 4]), 4)
        self.assertTrue(kalaha_library.choose_cup_based_on_strategy(1, [0, 1, 0, 0, 0, 0, 0]) in range(1, 2))
        self.assertTrue(kalaha_library.choose_cup_based_on_strategy(2, [0, 2, 3, 4, 0, 1, 4]) in range(3, 7))
        for i in range(1000):
            self.assertNotEqual(kalaha_library.choose_cup_based_on_strategy(2, [0, 2, 3, 4, 0, 1, 4]), 1)
            self.assertNotEqual(kalaha_library.choose_cup_based_on_strategy(2, [0, 2, 3, 4, 0, 1, 4]), 2)
            self.assertNotEqual(kalaha_library.choose_cup_based_on_strategy(2, [0, 2, 3, 4, 0, 1, 4]), 4)
            self.assertNotEqual(kalaha_library.choose_cup_based_on_strategy(2, [0, 2, 3, 4, 0, 1, 4]), 5)
        self.assertTrue(kalaha_library.choose_cup_based_on_strategy(2, [0, 1, 0, 0, 0, 0, 0]) in range(1, 2))

    def test_ask_player_is_human(self):
        '''
        
        Algorithm
        ---------
        Tests user input function.

        Returns
        -------
        None.

        '''
        with unittest.mock.patch('builtins.input', return_value = 'y'):
            self.assertEqual(kalaha_library.ask_player_is_human(0), True)
        with unittest.mock.patch('builtins.input', return_value = 'n'):
            self.assertEqual(kalaha_library.ask_player_is_human(0), False)

    def test_ask_ai_strategy(self):
        '''
        
        Algorithm
        ---------
        Tests user input function.

        Returns
        -------
        None.

        '''
        with unittest.mock.patch('builtins.input', return_value = '1'):
            self.assertEqual(kalaha_library.ask_ai_strategy(0), 1)

    def test_ask_no_of_games(self):
        '''
        
        Algorithm
        ---------
        Tests user input function.

        Returns
        -------
        None.

        '''
        with unittest.mock.patch('builtins.input', return_value = '100'):
            self.assertEqual(kalaha_library.ask_no_of_games(), 100)

if __name__ == '__main__':
    unittest.main()
