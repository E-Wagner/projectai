# Import the API objects
from api import State, Deck,  util
from api import State, Deck
import random

class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]

        # All legal moves
        # smaller values means higher card value, so sorted array
        moves = sorted(state.moves(), key=lambda tup: (tup[0] is None, tup[0])) 
        chosen = random.choice(moves)

        trump_in_hand = []

        # Beginner strategy, when your opponent is on lead and the stock is open

        # question stock size > 0 means stock open? 
        if state.whose_turn() == 1 and state.get_stock_size() > 0 and state.leader() == 2:
            opponent_played = state.get_opponents_played_card()
            print(opponent_played)
            for move in moves:
                # first check if move is marriage, if so continue on
                if type(move[0]) == int and type(move[1]) == int:
                    continue
                # else check if move is a 10 of suit
                if move[0] == 1 or move[0] == 6 or move[0] == 11 or move[0] == 16 and util.get_suit(move[0]) == state.get_trump_suit():
                    print(move)
                    return move
                # else check if move is an ace of suit      
                if move[0] == 0 or move[0] == 5 or move[0] == 10 or move[0] == 15 and util.get_suit(move[0]) == state.get_trump_suit(): 
                    print(move)
                    return move
                if move[0] is not None:    
                    if util.get_suit(move[0]) == state.get_trump_suit(): # store possible trump card 
                        trump_in_hand.append(move)
            # check if opponent played a nontrump ace or ten and we have a trump
            if opponent_played != None and len(trump_in_hand) != 0:
                if opponent_played == 1 or opponent_played == 6 or opponent_played == 11 or opponent_played == 16 or opponent_played % 5 == 0 and util.get_suit(opponent_played) != state.get_trump_suit(): 
                    return trump_in_hand[0]
       
            return moves[0] # finally, just return the adjacent card ?



        if state.get_opponents_played_card() is not None:
            value = state.get_opponents_played_card() % 5

            for move in moves:
                if move[0] % 5 > value:
                    chosen = move
                    break

        else:

            t_suit = state.get_trump_suit()

            for move in moves:
                if Deck.get_suit(move[0]) == t_suit:
                    chosen = move
                    break

        return chosen