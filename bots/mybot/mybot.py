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

        non_trump_jack_in_hand = []

        king_or_queen = [] # unsure about this one

        marriage_seen = False
        marriage_suit = ""

        # Beginner strategy, when your opponent is on lead and the stock is open

        # question stock size > 0 means stock open? 
        if state.whose_turn() == 1 and state.get_stock_size() > 0 and state.leader() == 2:
            opponent_played = state.get_opponents_played_card()
            # check if opponent leads a trump card (we can't win/do not want to win)
           
            if marriage_seen == False:
                for move in moves:
                    # first check if move is marriage, if so play it on                
                    if type(move[0]) == int and type(move[1]) == int:
                        marriage_seen = True
                        marriage_suit = util.get_suit(move[0])
                        return move

            # unsure how to implement: "If your opponent leads a trump or a card that you can not or do not want to win according to the guidelines above.."
            for move in moves:
                if state.get_prev_trick() and state.get_prev_trick()[0] != None:
                    if util.get_suit(state.get_prev_trick()[0]) == state.get_trump_suit():
                        if len(non_trump_jack_in_hand) != 0:
                            return non_trump_jack_in_hand[0]
                        if move[0] == 2 or move[0] ==  7 or move[0] ==  12 or move[0] ==  17 or move[0] ==  3 or move[0] ==  8 or move[0] ==  13 or move[0] ==  18:
                            if marriage_seen == True and util.get_suit(move[0]) != marriage_suit:
                                return move

            for move in moves:
                if move[0] == 4 or move[0] == 9 or move[0] == 14 or move[0] == 19 and util.get_suit(move[0]) != state.get_trump_suit():
                    non_trump_jack_in_hand.append(move)
                # else check if move is a 10 of suit
                if move[0] == 1 or move[0] == 6 or move[0] == 11 or move[0] == 16 and util.get_suit(move[0]) == state.get_trump_suit():
                    print(move)
                    return move
                # else check if move is an ace of suit      
                if move[0] == 0 or move[0] == 5 or move[0] == 10 or move[0] == 15 and util.get_suit(move[0]) == state.get_trump_suit(): 
                    print(move)
                    return move
                if move[0] is not None:   # None on index zero indicates trump jack exchange (might be interesting to use this last) 
                    if util.get_suit(move[0]) == state.get_trump_suit(): # store possible trump card 
                        trump_in_hand.append(move)


             

            # check if opponent played a nontrump ace or ten and we have a trump
            if opponent_played != None and len(trump_in_hand) != 0:
                if opponent_played == 1 or opponent_played == 6 or opponent_played == 11 or opponent_played == 16 or opponent_played % 5 == 0 and util.get_suit(opponent_played) != state.get_trump_suit(): 
                    return trump_in_hand[0]


                        
            return moves[0] # finally, just return the adjacent card ?

        #When you are on lead and the stock is open (simple and passive)
        if state.whose_turn() == 1 and state.leader() == 1 and state.get_stock_size() > 0:
            if marriage_seen == False:
                for move in moves:
                    if type(move[0]) == int and type(move[1]) == int:
                        marriage_seen = True
                        marriage_suit = util.get_suit(move[0])
                        return move  
            for move in moves:
                # Check if move is a jack and not a trump
                if move[0] == 4 or move[0] == 9 or move[0] == 14 or move[0] == 19 and util.get_suit(move[0]) != state.get_trump_suit():
                    return move
                # Check if move is queen and not a trump and marriage has been seen
                if move[0] == 3 or move[0] == 8 or move[0] == 13 or move[0] == 18 and util.get_suit(move[0]) != state.get_trump_suit() and marriage_seen == True:
                    return move
                # Check if move is king and not a trump and marriage has been seen
                if move[0] == 2 or move[0] == 7 or move[0] == 12 or move[0] == 17 and util.get_suit(move[0]) != state.get_trump_suit() and marriage_seen == True:
                    return move



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
