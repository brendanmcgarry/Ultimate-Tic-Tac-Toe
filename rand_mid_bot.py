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
        self.team_name = "RandMidBot"
    
    def move(self, board, forced_moves):
        """Logic for your bot"""
        
        novant = forced_moves[randint(0, len(forced_moves) - 1)]
        cell = 'C' if self.get_novant(board, novant)[self.map_tile['C']] == '.' else self.mapping[randint(0, 8)]
        
        return novant, cell
    
    def get_novant(self, board, novant):
        return board[self.mapping.index(novant)]
