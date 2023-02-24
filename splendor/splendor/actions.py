from enum import Enum

from splendor.types import Bank, Gems, Player, Tabletop


def _get_player(tabletop):
    player_i = tabletop.turn % len(tabletop.players)
    player = tabletop.players[player_i]

    return (player_i, player)

def pick_gems(tabletop, gems):
    player_i, player = _get_player(tabletop)

    # Does the tabletop bank stay solvent?
    new_bank = Bank.subtract_gems(tabletop.bank, gems)
    if Bank.is_solvent(new_bank):
        # Add to the player's bank
        new_player_bank = Bank.add_gems(
            tabletop.players[player_i].bank,
            gems)

        new_player = player._replace(bank=new_player_bank)

        new_players = Tabletop.replace_player(tabletop, player_i, new_player)

        return tabletop._replace(
            bank=new_bank,
            players=new_players)

    for i in range(len(Gems())):
        if tabletop.bank[i] < gems[i]:
            return False
    return True

def reserve_card(tabletop, tier, card=None):
    raise Exception("Implement reserving cards!")
    # Handle if the card is hidden to start with (only the player can see it?) flag?!?!

    return None

def buy_card(tabletop, tier, card_i):
    player_i, player = _get_player(tabletop)

    card = tabletop.decks[tier][card_i]

    # Can player afford this card?
    new_player_bank = Bank.pay_gems(
        player.bank,
        Player.get_bonus(player),
        card.cost)

    if Bank.is_solvent(new_player_bank):
        # Remove the card from the deck
        return Tabletop.remove_card_from_deck(
            # Replace the player (with updated)
            Tabletop.replace_player(
                tabletop,
                player_i,
                # Charge the cost to the player's bank
                Player.replace_bank(
                    # Add the card to their purchased
                    Player.add_card_to_purchased(player, card),
                    new_player_bank)),
            tier,
            card_i)
    else:
        return None

class ValidPlayerActions(Enum):
    PICK_DSE = (pick_gems, (Gems(diamond=1, sapphire=1, emerald=1),))
    PICK_DSR = (pick_gems, (Gems(diamond=1, sapphire=1, ruby=1),))
    PICK_DSO = (pick_gems, (Gems(diamond=1, sapphire=1, onyx=1),))
    PICK_DER = (pick_gems, (Gems(diamond=1, emerald=1, ruby=1),))
    PICK_DEO = (pick_gems, (Gems(diamond=1, emerald=1, onyx=1),))
    PICK_DRO = (pick_gems, (Gems(diamond=1, ruby=1, onyx=1),))
    PICK_SER = (pick_gems, (Gems(sapphire=1, emerald=1, ruby=1),))
    PICK_SEO = (pick_gems, (Gems(sapphire=1, emerald=1, onyx=1),))
    PICK_SRO = (pick_gems, (Gems(sapphire=1, ruby=1, onyx=1),))
    PICK_ERO = (pick_gems, (Gems(emerald=1, ruby=1, onyx=1),))
    PICK_DD = (pick_gems, (Gems(diamond=2),))
    PICK_SS = (pick_gems, (Gems(sapphire=2),))
    PICK_EE = (pick_gems, (Gems(emerald=2),))
    PICK_RR = (pick_gems, (Gems(ruby=2),))
    PICK_OO = (pick_gems, (Gems(onyx=2),))

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
