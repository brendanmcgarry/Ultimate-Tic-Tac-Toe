"""
This is the ONLY file you should modify.

(1) Name this file with your teamname:
    Do not include space in the filename.

(2) Send this file at the end of the tryout for submission.

"""

from random import randint

EMPTY = '.'

class bot:
    
    mapping = ['NW', 'N', 'NE', 'W', 'C', 'E', 'SW', 'S', 'SE']
    map_tile = {'NW': 0, 'N': 1, 'NE': 2,
                'W':  3, 'C': 4, 'E':  5,
                'SW': 6, 'S': 7, 'SE': 8}
    
    def __init__(self):
        self.team_name = "RandBot"
        
    def move(self, game, forced_move):
        "Logic for your bot"
        
        try:
        
            attempts = 0
            outer = self.map_tile[forced_move[randint(0, len(forced_move) - 1)]] if len(forced_move) else randint(0, 8)
            inner = randint(0, 8)
            while game[outer][inner] != EMPTY and attempts < 100:
                attempts += 1
                outer = self.map_tile[forced_move[randint(0, len(forced_move) - 1)]] if len(forced_move) else randint(0, 8)
                inner = randint(0, 8)
            
            if game[outer][inner] != EMPTY:
                valid_found = False
                for o in range(9):
                    for i in range(9):
                        if game[o][i] == EMPTY and self.mapping[o] in forced_move:
                            outer, inner = o, i
                            valid_found = True
                            break
                    if valid_found:
                        break
        except Exception as e:
            print(e)
            print(outer)
        
        return self.mapping[outer], self.mapping[inner]

