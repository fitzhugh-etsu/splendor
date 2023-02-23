# Game Functions State

##

tier-decks (1, 2, 3)

game_state

## Need to:

* NN for what action to take (from valid actions)
* NN for what noble to allow
* NN for what tokens to return

* NN for what to pay with (gold? colors?) - meh

## TODO
change to ctypes to push into NNs easier?

import splendor.data as d

def get_available_gem_options(tabletop):
    # Get 3 gems of different colors
    # Get 2 gems of a single color (if there are >= 4 tokens)

