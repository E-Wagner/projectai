from api import State  # , Deck
from api.util import *
import random


class Bot:

    def __init__(self):
        self.switched = False
        self.trump_count = 0
        pass

    def get_move(self, state):
        # type: (State) -> (int, int)

        # All legal moves
        # smaller values means higher card value, so sorted array
        moves = sorted(state.moves(), key=lambda tup: (tup[0] is None, tup[0]))

        trump_suit = state.get_trump_suit()
        trump_in_hand = []
        non_trump_jack_in_hand = []

        king_or_queen = []  # unsure about this one. what's the supposed use?

        # only one marriage? check logic!!
        def marriage(): return None
        marriage.seen = False
        marriage.move = ()

        for move in moves:
            # first check if move is marriage, if so, store it
            if type(move[0]) == int and type(move[1]) == int:
                marriage.seen = True
                marriage.move = move

            # None on index zero indicates trump jack exchange (might be interesting to use this last)
            if move[0] is not None:
                if get_suit(move[0]) == trump_suit:
                    # store trump card
                    trump_in_hand.append(move)

            # add NTJs
            if move[0] is not None and move[0] % 5 == 4 and get_suit(move[0]) != trump_suit:
                non_trump_jack_in_hand.append(move)

        # Beginner strategy
        # When your opponent is on lead and the stock is open

        # question stock size > 0 means stock open?
        # answer: yes, but I think using state.get_phase is equal and better
        if state.whose_turn() == 1 and state.get_phase() == 1 and state.leader() == 2:
            opponent_played = state.get_opponents_played_card()
            # check if opponent leads a trump card (we can't win/do not want to win)

            if marriage.seen:
                return marriage.move

            # unsure how to implement: "If your opponent leads a trump or a card that you can not or do not want to win
            # according to the guidelines above.."
            for move in moves:
                if state.get_prev_trick() and state.get_prev_trick()[0] is not None:
                    if get_suit(state.get_prev_trick()[0]) == trump_suit:
                        if len(non_trump_jack_in_hand) != 0:
                            return non_trump_jack_in_hand[0]

                        # Kings and Queens
                        if move[0] % 5 == 2 or move[0] % 5 == 3:
                            if marriage.seen and get_suit(move[0]) != get_suit(marriage.move[0]):
                                return move

            for move in moves:
                # Ten of suit
                if move[0] % 5 == 1 and get_suit(move[0]) == trump_suit:
                    # print(move)
                    return move
                # Ace of suit
                if move[0] % 5 == 0 and get_suit(move[0]) == trump_suit:
                    # print(move)
                    return move

            # check if opponent played a non-trump Ace or Ten and we have a trump
            if opponent_played is not None and len(trump_in_hand) != 0:
                if opponent_played % 5 == 1 or opponent_played % 5 == 0 \
                        and get_suit(opponent_played) != trump_suit:
                    return trump_in_hand[0]

            return moves[0]  # finally, just return the adjacent card ?

        # When you are on lead and the stock is open (simple and passive)
        if state.whose_turn() == 1 and state.leader() == 1 and state.get_phase() == 1:

            if marriage.seen:
                return marriage.move

            for move in moves:
                if marriage.seen:
                    if move in trump_in_hand and move[0] % 5 in (0, 1, 2):
                        return move
                    else:
                        return marriage.move
                # Non-trump Jack, Queen or King (marriage can't be seen here, as if it was, you returned it)
                if move[0] is not None and move[0] % 5 in (2, 3, 4) and get_suit(move[0]) != trump_suit:
                    return move

            return moves[0]  # finally, just return the adjacent card ?

        # IMPLEMENTING Marriages and trump exchange

        # IMPLEMENTING When the stock is no longer open
        if state.get_phase() == 2:
            if not self.switched:
                self.trump_count = len(trump_in_hand)
                self.switched = True

            if self.trump_count > 2 and len(trump_in_hand) > 0:
                return trump_in_hand[0]
            else:
                return moves[-1]  # lowest card



        # bullshit code ahead REMOVE before final

        chosen = random.choice(moves)
        if state.get_opponents_played_card() is not None:
            value = state.get_opponents_played_card() % 5

            for move in moves:
                if move[0] % 5 > value:
                    chosen = move
                    break

        else:

            t_suit = trump_suit

            for move in moves:
                if Deck.get_suit(move[0]) == t_suit:
                    chosen = move
                    break

        return chosen
