"""
This is the ONLY file you should modify.

(1) Name this file with your teamname:
    Do not include space in the filename.

(2) Send this file at the end of the tryout for submission.

"""

from random import randint
from collections import Counter


EMPTY = '.'

class bot:
    
    mapping = ['NW', 'N', 'NE', 'W', 'C', 'E', 'SW', 'S', 'SE']
    map_tile = {'NW': 0, 'N': 1, 'NE': 2,
                'W':  3, 'C': 4, 'E':  5,
                'SW': 6, 'S': 7, 'SE': 8}
    
    def __init__(self):
        self.team_name = "CroninBot"
        self.tick = None
    
    def move(self, board, forced_moves):
        """Logic for your bot"""
        if not self.tick:
            self.set_tick(board)
        
        for novant in forced_moves:
            coords = self.can_win_novant_square(board, novant)
            if coords:
                return coords
        
        novant =  forced_moves[randint(0, len(forced_moves) - 1)] \
                  if len(forced_moves) \
                  else randint(0, 8)
        cell = 'C' if self.get_novant_square(board, novant)[self.map_tile['C']] == EMPTY else self.mapping[randint(0, 8)]
        
        return novant, cell
    
    def get_novant_square(self, board, novant):
        return board[self.mapping.index(novant)]
    
    def can_win_novant_square(self, board, novant):
        """Check if a novant can be won in one move.
        
        Parameters:
            board (np.array(dtype='<U1')): 9x9 game board
            novant (str): Enum of which 9th of the board being used
        
        Returns:
            Novant coords for winning move if they exist, else None.
        """
        square = self.get_novant_square(board, novant)
        
        # Check horizontal
        for i in (1, 2, 0):
            matches = {}
            for ind, x in enumerate(square[i * 3 : (i * 3) + 3]):
                matches[x] = (1, i * 3 + ind) if x not in matches else (matches[x][0] + 1,)
            if matches.get(self.tick) and matches.get(self.tick)[0] == 2 \
            and matches.get(EMPTY) and matches.get(EMPTY)[0] == 1:
                return novant, self.mapping[matches.get(EMPTY)[1]]
        
        # Check vertical
        for i in (1, 2, 0):
            matches = {}
            for ind, x in enumerate(square[[i, i + 3, i + 6]]):
                matches[x] = (1, i + ind * 3) if x not in matches else (matches[x][0] + 1,)
            if matches.get(self.tick) and matches.get(self.tick)[0] == 2 \
            and matches.get(EMPTY) and matches.get(EMPTY)[0] == 1:
                return novant, self.mapping[matches.get(EMPTY)[1]]
        
        # Check NW-to-SE slash
        slash = Counter(x for x in square[[0, 4, 8]])
        if slash.get(self.tick) == 2 and slash.get(EMPTY) == 1:
            cell_coord = self.mapping[square[[0, 4, 8]].tolist().index(EMPTY) * 4]
            return novant, cell_coord
        
        # Check NE-to-SW slash
        backslash = Counter(x for x in square[[2, 4, 6]])
        if backslash.get(self.tick) == 2 and backslash.get(EMPTY) == 1:
            cell_coord = self.mapping[(square[[2, 4, 6]].tolist().index(EMPTY) + 1) * 2]
            return novant, cell_coord
        
        return None
    
    def set_tick(self, board):
        for y in range(9):
            for x in range(9):
                if board[y, x] != EMPTY:
                    self.tick = 'O'
                    return
        
        self.tick = 'X'
