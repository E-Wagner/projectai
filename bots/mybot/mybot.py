# Import the API objects
from api import State, Deck
import random


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]

        # All legal moves
        moves = state.moves()
        chosen = random.choice(moves)

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
