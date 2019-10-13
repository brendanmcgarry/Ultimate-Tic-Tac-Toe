import argparse
import copy
from contextlib import contextmanager
import importlib
import signal

from game import Game

#
from collections import Counter


def raise_timeout(signum, frame):
    raise TimeoutError


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="CS GAMES 2020 AI Tryout")
    parser.add_argument("bot1", type=str, help="filename")
    parser.add_argument("bot2", type=str, help="filename")
    parser.add_argument("--verbose", "-v", action="store_true", help="display the gameboard")
    parser.add_argument("--rounds", "-r", type=int, help="number of games to be played")
    parser.add_argument("--alternate", "-a", help="whether player order alternates between games")
    args = parser.parse_args()
    
    # Import bot class
    bots = list()
    mod = importlib.import_module(args.bot1)
    bot1 = getattr(mod, "bot")
    bots.append(bot1())
    
    mod = importlib.import_module(args.bot2)
    bot2 = getattr(mod, "bot")
    bots.append(bot2())
    
    if bots[0].team_name == bots[1].team_name:
        bots[0].team_name += '1'
        bots[1].team_name += '2'
    
    winners = []
    rounds = args.rounds or 100
    for game_num in range(rounds):
        bots = bots[::-1]
        
        # Start game
        game = Game()
        TIME_OUT_TIME = 1
        if args.verbose:
            TIME_OUT_TIME = 300
            
        timed_out = False
        draw = False
        forced_move = list(game.map_tile)
        
        while True:
            
            # Next player's turn
            game.player_turn = (game.player_turn + 1) % 2
            if args.verbose:
                game.status()
                input()
                
            if timed_out:
                print(f"\n{game_num}: {bots[game.player_turn].team_name} won!!!")
                draw = True
                break  # Opponent timed out
                
            timed_out = True
            # Validate player's move
            # while True:
            for _ in range(10):
                player_move = bots[game.player_turn].move(
                    copy.deepcopy(game.board), copy.deepcopy(forced_move)
                )
                if player_move[0] not in forced_move:
                    continue
                    
                try:
                    if game.make_move(*player_move):
                        forced_move = game.next_tile
                        timed_out = False
                        break
                except Exception:
                    print("Invalid move")
            
            # Check for win
            if game.check_win(game.board[Game.map_tile[player_move[0]]]):
                tick = "X" if game.player_turn == 0 else "O"
                game.win_status[Game.map_tile[player_move[0]]] = tick
                
                if player_move[0] == player_move[1]:
                    game.next_tile = [
                        tile
                        for i, tile in enumerate(Game.map_tile.keys())
                        if game.win_status[i] is None
                    ]
                    forced_move = game.next_tile
                    
                if game.check_win(game.win_status):
                    print(
                        f"\n{game_num}: {bots[game.player_turn].team_name} won!!!"
                    )  # Winning sequence
                    break
        
        winners.append('Draw' if draw else bots[game.player_turn].team_name)
    
    c = Counter(winners)
    print(c)
    for b in range(2):
        print('{}: {}%'.format(bots[b].team_name,
            (c[bots[b].team_name ] + c['Draw'] / 2) / args.rounds * 100))
    
