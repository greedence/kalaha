# -*- coding: utf-8 -*-
"""
@author: Anonymous

"""

from kalaha_library import GameManager

def main():
    '''
    
    Parameters
    ----------
    None.

    Algorithm
    ---------
    Create an instance of the GameManager class
    and show the game menu.

    Returns
    -------
    None.

    '''
    game_mgr = GameManager()
    game_mgr.show_menu()

if __name__ == '__main__':
    main()
