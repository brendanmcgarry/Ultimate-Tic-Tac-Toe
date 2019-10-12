"""
This is the ONLY file you should modify.

(1) Name this file with your teamname:
    Do not include space in the filename.

(2) Send this file at the end of the tryout for submission.

"""

from random import randint

class bot:
    
    mapping = ['NW', 'N', 'NE', 'W', 'C', 'E', 'SW', 'S', 'SE']
    map_tile = {'NW': 0, 'N': 1, 'NE': 2,
                'W':  3, 'C': 4, 'E':  5,
                'SW': 6, 'S': 7, 'SE': 8}
    
    def __init__(self):
        self.team_name = "RandBot"
        
    def move(self, game, forced_move):
        "Logic for your bot"
        
        # return self.map_tile[forced_move[randint(0, len(forced_move) - 1)]], self.mapping[randint(0, 8)]
        return self.mapping[randint(0, 8)], self.mapping[randint(0, 8)]

