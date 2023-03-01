from enum import Enum

import splendor.defs as d
from splendor.types import Bank, Gems, Noble, Player, Tabletop


def _get_player(tabletop):
    player_i = tabletop.turn % len(tabletop.players)
    player = tabletop.players[player_i]

    return (player_i, player)

def pick_gems(tabletop, gems):
    player_i, player = _get_player(tabletop)

    # Are you pickup too many?
    if sum(gems) > d.BANK_TOTAL_GEM_PICKUP_AMOUNT:
        return None

    # You can't pickup multiples when the threshold for that gem type is too low
    if any([True for i in range(len(Gems()))
            if gems[i] > 1 and tabletop.bank[i] < d.BANK_THRESHOLD_FOR_DOUBLE_GEMS]):
        return None

    # You can't pick up multiple > 1 gems
    if len([gems[i] for i in range(len(Gems())) if (gems[i] > 1)]) > 1:
        return None

    # Does the tabletop bank stay solvent?
    new_table_bank = Bank.subtract_gems(tabletop.bank, gems)
    if Bank.is_solvent(new_table_bank):
        # Add to the player's bank
        new_player_bank = Bank.add_gems(
            tabletop.players[player_i].bank,
            gems)

        new_player = player._replace(bank=new_player_bank)

        return Tabletop.replace_player(
            tabletop,
            player_i,
            new_player)._replace(
                bank=new_table_bank)

    return None

def reserve_card(tabletop, tier, card_i=None):
    player_i, player = _get_player(tabletop)

    # Pull from the top of the deck
    card_i = card_i or d.VISIBLE_TOP_DECK_CARDS

    # Can we reserve?
    if Player.can_reserve_card(player):
        # Is the card available in the deck?
        if (card := Tabletop.get_card(tabletop, tier, card_i)):
            # We can reserve this card!

            # Give card to player
            new_player = Player.add_card_to_reserved(player, card)

            # Remove it from the tabletop
            new_tabletop = Tabletop.remove_card_from_deck(tabletop, tier, card_i)

            # Now we try to pickup gold.

            # We can try to get a gold
            new_table_bank = Bank.pickup_gold(tabletop.bank, gold=d.GOLD_RESERVATION_AMOUNT)
            if Bank.is_solvent(new_table_bank):
                # Bank was reduced gold.
                new_tabletop = new_tabletop._replace(bank=new_table_bank)
                # Player bank was added gold
                new_player = new_player._replace(
                    bank=Bank.add_gold(
                        new_player.bank,
                        gold=d.GOLD_RESERVATION_AMOUNT))
            else:
                # Table bank didn't change
                # Player gold didn't change
                # But player was given card (above)
                pass

            # Update the changes to the player
            return Tabletop.replace_player(
                new_tabletop,
                player_i,
                new_player)
    return None

def buy_reserved(tabletop, reserved_i):
    player_i, player = _get_player(tabletop)

    # Is reserved card existent?
    if (card := Player.get_reserved(player, reserved_i)):
        # The card exists!

        # Can player afford this card?
        new_player_bank = Bank.pay_gems(
            player.bank,
            Player.get_bonus(player),
            card.cost)

        if Bank.is_solvent(new_player_bank):
            # Add things back to table bank
            new_table_bank = Bank.receive_bank(
                tabletop.bank,
                Bank.difference(
                    player.bank,
                    new_player_bank))

            # Update the whole tabletop
            return Tabletop.replace_player(
                tabletop._replace(
                    # Add the new bank in
                    bank=new_table_bank),
                player_i,
                # Charge the cost to the player's bank
                Player.update_bank(
                    # Remove card from reserved
                    Player.remove_card_from_reserved(
                        # Add card to purchased
                        Player.add_card_to_purchased(player, card),
                        reserved_i),
                    new_player_bank))

def buy_card(tabletop, tier, card_i):
    player_i, player = _get_player(tabletop)
    # Not enough cacrds!
    if len(tabletop.decks[tier]) <= card_i:
        return None

    card = tabletop.decks[tier][card_i]

    # Can player afford this card?
    new_player_bank = Bank.pay_gems(
        player.bank,
        Player.get_bonus(player),
        card.cost)

    if Bank.is_solvent(new_player_bank):
        # Add things back to table bank
        new_table_bank = Bank.receive_bank(
            tabletop.bank,
            Bank.difference(
                player.bank,
                new_player_bank))

        # Remove the card from the deck
        return Tabletop.remove_card_from_deck(
            # Replace the player (with updated)
            Tabletop.replace_player(
                tabletop._replace(
                    # Add the new bank in
                    bank=new_table_bank),
                player_i,
                # Charge the cost to the player's bank
                Player.update_bank(
                    # Add the card to their purchased
                    Player.add_card_to_purchased(player, card),
                    new_player_bank)),
            tier,
            card_i)

    return None

def return_gold(tabletop, gold_number):
    player_i = (tabletop.turn - 1) % len(tabletop.players)
    player = tabletop.players[player_i]
    if sum(player.bank) > d.MAX_PLAYER_TOKENS:
        new_player_bank = player.bank._replace(gold=player.bank.gold - gold_number)
        if Bank.is_solvent(new_player_bank):
            new_table_bank = tabletop.bank._replace(
                gold=tabletop.bank.gold + gold_number)

            return Tabletop.replace_player(
                tabletop._replace(
                    # Add the new bank in
                    bank=new_table_bank),
                player_i,
                # Charge the cost to the player's bank
                Player.update_bank(
                    # Add the card to their purchased
                    player,
                    new_player_bank)),

def return_gem(tabletop, gems):
    player_i = (tabletop.turn - 1) % len(tabletop.players)
    player = tabletop.players[player_i]
    
    if sum(player.bank) > d.MAX_PLAYER_TOKENS:
        new_player_bank = Bank.pay_gems(
            player.bank,
            None,
            gems,
            # Don't allow us to pay with gold to cover this cost
            allow_gold=False)
        if Bank.is_solvent(new_player_bank):
            new_table_bank = Bank.receive_bank(
                tabletop.bank,
                Bank(*gems))

            return Tabletop.replace_player(
                tabletop._replace(
                    # Add the new bank in
                    bank=new_table_bank),
                player_i,
                # Charge the cost to the player's bank
                Player.update_bank(
                    # Add the card to their purchased
                    player,
                    new_player_bank))

def accept_noble(tabletop, noble_i):
    player_i = (tabletop.turn - 1) % len(tabletop.players)
    player = tabletop.players[player_i]
    if noble_i < Noble.number_visible(tabletop.players):
        try:
            noble = tabletop.nobles_deck[noble_i]
            if Noble.would_visit(noble, player):
                return Tabletop.replace_player(
                    # Remove noble from the tabletop
                    Tabletop.remove_noble_from_deck(tabletop, noble_i),
                    # Player to replace (i)
                    player_i,
                    # Add noble to player
                    Player.add_noble(player, noble))
        except IndexError:
            return None
    else:
        return None

class ValidNobleActions(Enum):
    NOBLE_0 = (accept_noble, (0, ))
    NOBLE_1 = (accept_noble, (1, ))
    NOBLE_2 = (accept_noble, (2, ))
    NOBLE_3 = (accept_noble, (3, ))
    NOBLE_4 = (accept_noble, (4, ))

class ValidGemPaybackActions(Enum):
    RETURN_D = (return_gem, (Gems(diamond=1),))
    RETURN_E = (return_gem, (Gems(emerald=1),))
    RETURN_S = (return_gem, (Gems(sapphire=1),))
    RETURN_R = (return_gem, (Gems(ruby=1),))
    RETURN_O = (return_gem, (Gems(onyx=1),))
    RETURN_G = (return_gold,(1, ))

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

    # Buy your reserved files for a turn
    BUY_RESERVED_0 = (buy_reserved, (0, ))
    BUY_RESERVED_1 = (buy_reserved, (1, ))
    BUY_RESERVED_2 = (buy_reserved, (2, ))

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

def apply_action(tabletop, action):
    new_tabletop = action.value[0](tabletop, *action.value[1])
    if new_tabletop:
        return new_tabletop._replace(turn=tabletop.turn + 1)
    else:
        return None

def valid_actions(tabletop):
    for action in ValidPlayerActions:
        new_tabletop = action.value[0](tabletop, *action.value[1])
        if new_tabletop:
            yield action

def valid_payback_actions_for_last_player(tabletop):
    for action in ValidGemPaybackActions:
        new_tabletop = action.value[0](tabletop, *action.value[1])
        if new_tabletop:
            yield action

def apply_payback_action_for_last_player(tabletop, action):
    new_tabletop = action.value[0](tabletop, *action.value[1])
    if new_tabletop:
        return new_tabletop
    else:
        return None

def valid_nobles_for_last_player(tabletop):
    for action in ValidNobleActions:
        new_tabletop = action.value[0](tabletop, *action.value[1])
        if new_tabletop:
            yield action

def apply_noble_for_last_player(tabletop, action):
    new_tabletop = action.value[0](tabletop, *action.value[1])
    if new_tabletop:
        return new_tabletop
    else:
        return None

def next_game_actions(tabletop):
    # If there are > 10 we need to give some gems back
    if (actions := list(valid_payback_actions_for_last_player(tabletop))):
        return (False, actions)
    # If there are nobles, we need to accept some
    if (actions := list(valid_nobles_for_last_player(tabletop))):
        return (False, actions)

    # Otherwise 
    return (True, list(valid_actions(tabletop)))

def apply_game_actions(tabletop, action):
    if isinstance(action, ValidGemPaybackActions):
        return apply_payback_action_for_last_player(tabletop, action)

    elif isinstance(action, ValidNobleActions):
        return apply_noble_for_last_player(tabletop, action)

    elif isinstance(action, ValidPlayerActions):
        return apply_action(tabletop, action)

    import pudb; pudb.set_trace()
    raise Exception("What?", action)
