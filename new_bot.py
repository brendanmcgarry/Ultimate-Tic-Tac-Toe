"""
This is the ONLY file you should modify.

(1) Name this file with your teamname:
    Do not include space in the filename.

(2) Send this file at the end of the tryout for submission.

"""

import numpy as np
from random import randint, random
from collections import Counter


EMPTY = '.'

class bot:
    
    mapping = ['NW', 'N', 'NE', 'W', 'C', 'E', 'SW', 'S', 'SE']
    map_tile = {'NW': 0, 'N': 1, 'NE': 2,
                'W':  3, 'C': 4, 'E':  5,
                'SW': 6, 'S': 7, 'SE': 8}
    
    def __init__(self):
        self.team_name = "NewBot"
        self.tick = None
    
    def move(self, board, forced_moves):
        if not self.tick:
            self._set_tick(board)
        
        print(self.team_name + ' moving')
        
        return self.mcts(board, forced_moves)
    
    def _move(self, board, forced_moves):
        """Logic for your bot"""
        if not self.tick:
            self._set_tick(board)
        
        for novant in forced_moves:
            coords = self.can_win_novant_square(board, novant)
            if coords:
                return coords
        
        for novant in forced_moves:
            coords = self.can_win_novant_square(board, novant, self._opposite_tick())
            if coords:
                return coords
        
        novant =  forced_moves[randint(0, len(forced_moves) - 1)] \
                  if len(forced_moves) \
                  else self.mapping[randint(0, 8)]
        if self.get_novant_square(board, novant)[self.map_tile['C']] == EMPTY:
            cell = 'C'
        else:
            cell = self.mapping[randint(0, 8)]
        
        if board[self.map_tile[novant]][self.map_tile[cell]] != EMPTY:
            moves = self.get_all_moves(board, forced_moves)
            novant, cell = moves[randint(0, len(moves) - 1)]
        
        return novant, cell
    
    def get_novant_square(self, board, novant):
        return board[self.mapping.index(novant)]
    
    def can_win_novant_square(self, board, novant, tick=None):
        """Check if a novant can be won in one move.
        
        Parameters:
            board (np.array(dtype='<U1')): 9x9 game board
            novant (str): Enum of which 9th of the board being used
            tick (str): The char symbol for the player being evaluated for.
        
        Returns:
            tuple(str): Novant coords for winning move if they exist, else None.
        """
        square = self.get_novant_square(board, novant)
        if tick == None:
            tick = self.tick
        
        # Check horizontal
        for i in (1, 2, 0):
            matches = {}
            for ind, x in enumerate(square[i * 3 : (i * 3) + 3]):
                matches[x] = (1, i * 3 + ind) if x not in matches else (matches[x][0] + 1,)
            if matches.get(tick) and matches.get(tick)[0] == 2 \
            and matches.get(EMPTY) and matches.get(EMPTY)[0] == 1:
                return novant, self.mapping[matches.get(EMPTY)[1]]
        
        # Check vertical
        for i in (1, 2, 0):
            matches = {}
            for ind, x in enumerate(square[[i, i + 3, i + 6]]):
                matches[x] = (1, i + ind * 3) if x not in matches else (matches[x][0] + 1,)
            if matches.get(tick) and matches.get(tick)[0] == 2 \
            and matches.get(EMPTY) and matches.get(EMPTY)[0] == 1:
                return novant, self.mapping[matches.get(EMPTY)[1]]
        
        # Check NW-to-SE slash
        slash = Counter(x for x in square[[0, 4, 8]])
        if slash.get(tick) == 2 and slash.get(EMPTY) == 1:
            cell_coord = self.mapping[square[[0, 4, 8]].tolist().index(EMPTY) * 4]
            return novant, cell_coord
        
        # Check NE-to-SW slash
        backslash = Counter(x for x in square[[2, 4, 6]])
        if backslash.get(tick) == 2 and backslash.get(EMPTY) == 1:
            cell_coord = self.mapping[(square[[2, 4, 6]].tolist().index(EMPTY) + 1) * 2]
            return novant, cell_coord
        
        return None
    
    def get_square_state(self, square, tick=None):
        if tick is None:
            tick = self.tick
        
        opposite = self._opposite_tick(tick)
        
        # Horizontal
        for i in range(3):
            # Win
            if all(x == tick for x in square[i * 3 : (i * 3) + 3]):
                return tick
                
            # Loss
            elif all(x == opposite for x in square[i * 3 : (i * 3) + 3]):
                return opposite
                
        # Vertical
        for i in range(3):
            if all(x == tick for x in square[[i, i + 3, i + 6]]):
                return tick
            elif all(x == opposite for x in square[i * 3 : (i * 3) + 3]):
                return opposite
                
        # Diagonal
        if all(x == tick for x in square[[0, 4, 8]]) \
        or all(x == tick for x in square[[2, 4, 6]]):
            return tick
        
        if all(x == opposite for x in square[[0, 4, 8]]) \
        or all(x == opposite for x in square[[2, 4, 6]]):
            return opposite
        
        if any(x == EMPTY for x in square):
            return EMPTY
        
        # Draw
        return 'Draw'
    
    def _set_tick(self, board):
        for y in range(9):
            for x in range(9):
                if board[y, x] != EMPTY:
                    self.tick = 'O'
                    self.enemy_tick = 'X'
                    return
        
        self.tick = 'X'
        self.enemy_tick = 'O'
    
    def _opposite_tick(self, tick=None):
        return 'X' if (tick or self.tick) == 'O' else 'O'
    
    def board_str(self, board):
        s = ''
        for i in range(3):
            s += "-" * 25 + '\n'
            for j in range(3):
                s += (
                    "| "
                    + " ".join(board[i * 3][j * 3 : (j * 3) + 3])
                    + " | "
                    + " ".join(board[(i * 3) + 1][j * 3 : (j * 3) + 3])
                    + " | "
                    + " ".join(board[(i * 3) + 2][j * 3 : (j * 3) + 3])
                    + " |\n"
                )
        s += "-" * 25 + '\n'
        return s
    
    def get_all_moves(self, board, forced_moves):
        if not isinstance(forced_moves, list):
            forced_moves = [forced_moves]
        
        moves = []
        for novant in forced_moves:
            square = self.get_novant_square(board, novant)
            for i, cell in enumerate(square):
                if cell == EMPTY:
                    moves.append((novant, self.mapping[i]))
        return moves
    
    def game_over(self, board):
        square_states = []
        for nv in self.mapping:
            square_state = self.get_square_state(self.get_novant_square(board, nv))
            square_states.append(square_state)
        
        game_state = self.get_square_state(np.array(square_states))
        return game_state if game_state in ('X', 'O', 'Draw') else False
    
    def grabbing_move(self, board, forced_moves, rand_ratio=0.1):
        if random() < 0.1:
            return self._rand_move(board, forced_moves)
        else:
            return self._move(board, forced_moves)
    
    def _rand_move(self, board, forced_moves):
        # for _ in range(100):
        #     novant =  forced_moves[randint(0, len(forced_moves) - 1)] \
        #               if len(forced_moves) \
        #               else randint(0, 8)
        #     cell = self.mapping[randint(0, 8)]
        #     if board[self.map_tile[novant]][self.map_tile[cell]] == EMPTY:
        #         break
        # return novant, cell
        moves = self.get_all_moves(board, forced_moves)
        if moves:
            return moves[randint(0, len(moves) - 1)]
        else:
            print(board)
            return False
    
    def _get_forced_moves(self, board, novant):
        if self.get_square_state(self.get_novant_square(board, novant)) == EMPTY:
            return novant
        
        return [nv for nv in self.mapping if self.get_square_state(self.get_novant_square(board, nv)) == EMPTY]
    
    def _make_move(self, board, move, tick):
        if board[self.map_tile[move[0]]][self.map_tile[move[1]]] != EMPTY:
            raise ValueError(f'Cannot make move in tile {move}; it is not empty.')
        
        board[self.map_tile[move[0]]][self.map_tile[move[1]]] = tick
        return self._get_forced_moves(board, move[1])
    
    def mcts(self, old_board, forced_moves):
        moves = self.get_all_moves(old_board, forced_moves)
        strengths = {}
        
        for _ in range(1):
            for move in moves:
                tick = self.tick
                board = np.copy(old_board)
                
                fm = self._make_move(board, move, tick)
                tick = self.enemy_tick
                
                game_over_status = self.game_over(board)
                while not game_over_status:
                    m = self.grabbing_move(board, fm)
                    fm = self._make_move(board, m, tick)
                    
                    tick = self._opposite_tick(tick)
                    game_over_status = self.game_over(board)
                
                val = 1 if game_over_status == self.tick else \
                      (-1) if game_over_status == self.enemy_tick else \
                      0
                if move not in strengths:
                    strengths[move] = [val]
                else:
                    strengths[move].append(val)
        
        try:
            strengths = {m: np.average(strengths[m]) for m in strengths}
            move = max(strengths, key=lambda key: strengths[key])
            print({move: strengths[move]})
            return move
        except:
            print('random move')
            move = self._rand_move(old_board, forced_moves)
            return move or (self.map_tile[randint(0, 8)], self.map_tile[randint(0, 8)])
                
