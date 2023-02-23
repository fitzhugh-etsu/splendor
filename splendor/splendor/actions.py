from enum import Enum

import splendor.buy as buy
import splendor.data as d
import splendor.mutate as m


def pick_gems(tabletop, gems):
    raise Exception("Implement picking gems")
    return True

def reserve_card(tabletop, tier, card=None):
    raise Exception("Implement reserving cards!")
    # Handle if the card is hidden to start with (only the player can see it?) flag?!?!

    return None

def buy_card(tabletop, tier, card_i):
    current_player = tabletop.turn % len(tabletop.players)
    card = tabletop.decks[tier][card_i]

    # Can player afford this card?
    new_player = buy.can_afford(tabletop.players[current_player], card)

    if new_player:
        # Remove the card from the deck
        new_decks = m.remove_card_from_deck(tabletop.decks, tier, card_i)

        # Add the card to their purchased
        new_player = m.player_purchase_card(new_player, card)

        return tabletop._replace(
            decks=new_decks,
            players=m.update_players(tabletop, current_player, new_player))
    else:
        return None

class ValidPlayerActions(Enum):
    PICK_DSE = (pick_gems, (d.Gems(diamond=1, sapphire=1, emerald=1),))
    PICK_DSR = (pick_gems, (d.Gems(diamond=1, sapphire=1, ruby=1),))
    PICK_DSO = (pick_gems, (d.Gems(diamond=1, sapphire=1, onyx=1),))
    PICK_DER = (pick_gems, (d.Gems(diamond=1, emerald=1, ruby=1),))
    PICK_DEO = (pick_gems, (d.Gems(diamond=1, emerald=1, onyx=1),))
    PICK_DRO = (pick_gems, (d.Gems(diamond=1, ruby=1, onyx=1),))
    PICK_SER = (pick_gems, (d.Gems(sapphire=1, emerald=1, ruby=1),))
    PICK_SEO = (pick_gems, (d.Gems(sapphire=1, emerald=1, onyx=1),))
    PICK_SRO = (pick_gems, (d.Gems(sapphire=1, ruby=1, onyx=1),))
    PICK_ERO = (pick_gems, (d.Gems(emerald=1, ruby=1, onyx=1),))
    PICK_DD = (pick_gems, (d.Gems(diamond=2),))
    PICK_SS = (pick_gems, (d.Gems(sapphire=2),))
    PICK_EE = (pick_gems, (d.Gems(emerald=2),))
    PICK_RR = (pick_gems, (d.Gems(ruby=2),))
    PICK_OO = (pick_gems, (d.Gems(onyx=2),))

    BUY_TIER_0_0 = (buy_card, (0, 0))
    BUY_TIER_0_1 = (buy_card, (0, 1))
    BUY_TIER_0_2 = (buy_card, (0, 2))
    BUY_TIER_0_3 = (buy_card, (0, 3))
    BUY_TIER_1_0 = (buy_card, (1, 0))
    BUY_TIER_1_1 = (buy_card, (1, 1))
    BUY_TIER_1_2 = (buy_card, (1, 2))
    BUY_TIER_1_3 = (buy_card, (1, 3))
    BUY_TIER_2_0 = (buy_card, (0, 1))
    BUY_TIER_2_1 = (buy_card, (0, 1))
    BUY_TIER_2_2 = (buy_card, (0, 1))
    BUY_TIER_2_3 = (buy_card, (0, 1))

    # Reserve TIER
    RESERVE_TIER_0 = (reserve_card, (0,))
    RESERVE_TIER_0_0 = (reserve_card, (0, 0))
    RESERVE_TIER_0_1 = (reserve_card, (0, 1))
    RESERVE_TIER_0_2 = (reserve_card, (0, 2))
    RESERVE_TIER_0_3 = (reserve_card, (0, 3))

    # Reserve random card from top of tier 1 deck
    RESERVE_TIER_1 = (reserve_card, (1,))
    RESERVE_TIER_1_0 = (reserve_card, (1, 0))
    RESERVE_TIER_1_1 = (reserve_card, (1, 1))
    RESERVE_TIER_1_2 = (reserve_card, (1, 2))
    RESERVE_TIER_1_3 = (reserve_card, (1, 3))

    # Reserve random card from top of tier 2 deck
    RESERVE_TIER_2 = (reserve_card, (2,))
    RESERVE_TIER_2_0 = (reserve_card, (2, 0))
    RESERVE_TIER_2_1 = (reserve_card, (2, 1))
    RESERVE_TIER_2_2 = (reserve_card, (2, 2))
    RESERVE_TIER_2_3 = (reserve_card, (2, 3))

def valid_actions(tabletop):
    for action in ValidPlayerActions:

        print(action.value)
        if action.value[0](tabletop, *action.value[1]):
            yield action
