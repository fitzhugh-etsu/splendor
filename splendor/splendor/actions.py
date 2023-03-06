from enum import Enum

import splendor.defs as d
from splendor.types import Bank, Game, Gems, Noble, PerformedAction, Player


def _new_turn(game):
    return game._replace(turn=game.turn + 1)

def _new_table_bank(game, bank):
    return game._replace(bank=bank)

def _new_table_player(game, player_i, player):
    return Game.replace_player(game, player_i, player)

def _update(
    old_game,
    new_turn=False,
    new_player=None,
    new_player_bank=None,
    accept_noble=None,
    remove_card=None,
        new_bank=None):

    game = old_game

    if new_turn:
        game = game._replace(turn=game.turn + 1)

    if remove_card:
        (tier, card_i) = remove_card
        game = Game.remove_card_from_deck(game, tier, card_i)

    if new_player:
        (player_i, player) = new_player

        game = _new_table_player(game, player_i, player)

    if accept_noble:
        (player_i, noble_i) = accept_noble
        noble = game.nobles_deck[noble_i]
        game = Game.remove_noble_from_deck(game, noble_i)

        player = Player.add_noble(
            game.players[player_i],
            noble)

        game = _new_table_player(
            game,
            player_i,
            player)

    if new_player_bank:
        (player_i, player_bank) = new_player_bank
        player = Player.update_bank(
            # Add the card to their purchased
            game.players[player_i],
            player_bank)
        game = _new_table_player(game, player_i, player)

    if new_bank:
        game = _new_table_bank(game, new_bank)
    return game

def _get_player(game):
    player_i = game.turn % len(game.players)
    player = game.players[player_i]

    return (player_i, player)

def pick_gems(game, gems):
    player_i, player = _get_player(game)

    # Are you pickup too many?
    if sum(gems) > d.BANK_TOTAL_GEM_PICKUP_AMOUNT:
        return None

    # You can't pickup multiples when the threshold for that gem type is too low
    if any([True for i in range(len(Gems()))
            if gems[i] > 1 and game.bank[i] < d.BANK_THRESHOLD_FOR_DOUBLE_GEMS]):
        return None

    # You can't pick up multiple > 1 gems
    if len([gems[i] for i in range(len(Gems())) if (gems[i] > 1)]) > 1:
        return None

    # Does the game bank stay solvent?
    new_table_bank = Bank.subtract_gems(game.bank, gems)

    if Bank.is_solvent(new_table_bank):
        return _update(
            game,
            new_turn=True,
            new_bank=new_table_bank,
            new_player=(player_i, Player.add_gems(player, gems)))

    return None

def reserve_card(game, tier, card_i=None):
    player_i, player = _get_player(game)

    # Pull from the top of the deck
    hidden = not card_i
    # If we have None index, pull top of deck
    card_i = card_i or d.VISIBLE_TOP_DECK_CARDS

    # Can we reserve?
    if Player.can_reserve_card(player):
        # Is the card available in the deck?
        if (card := Game.get_card(game, tier, card_i)):
            # We can reserve this card (it exists!)

            # Give card to player
            new_player = Player.add_card_to_reserved(player, card, hidden=hidden)

            # Remove it from the game
            new_game = Game.remove_card_from_deck(game, tier, card_i)

            # Now we try to pickup gold.
            # We can try to get a gold
            new_table_bank = Bank.pickup_gold(game.bank, gold=d.GOLD_RESERVATION_AMOUNT)
            # If the bank had it... then we can proceed
            if Bank.is_solvent(new_table_bank):
                # Bank was reduced gold.
                new_game = new_game._replace(bank=new_table_bank)

                # Player bank was added gold
                new_game = _update(
                    new_game,
                    new_bank=new_table_bank,
                    new_player=(
                        player_i,
                        new_player._replace(
                            bank=Bank.add_gold(
                                new_player.bank,
                                gold=d.GOLD_RESERVATION_AMOUNT))))
            else:
                # Table bank didn't change
                # Player gold didn't change
                # But player was given card (above)
                pass

            # Update the changes to the player
            return _new_turn(new_game)
    return None

def buy_reserved(game, reserved_i):
    player_i, player = _get_player(game)

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
                game.bank,
                Bank.difference(
                    player.bank,
                    new_player_bank))

            # Update the whole game
            return _update(
                game,
                new_turn=True,
                new_bank=new_table_bank,
                new_player=(
                    player_i,
                    # Charge the cost to the player's bank
                    Player.update_bank(
                        # Remove card from reserved
                        Player.remove_card_from_reserved(
                            # Add card to purchased
                            Player.add_card_to_purchased(player, card),
                            reserved_i),
                        new_player_bank)))

def buy_card(game, tier, card_i):
    player_i, player = _get_player(game)
    # Not enough cacrds!
    if len(game.decks[tier]) <= card_i:
        return None

    card = game.decks[tier][card_i]

    # Can player afford this card?
    new_player_bank = Bank.pay_gems(
        player.bank,
        Player.get_bonus(player),
        card.cost)

    if Bank.is_solvent(new_player_bank):
        # Add things back to table bank
        new_table_bank = Bank.receive_bank(
            game.bank,
            Bank.difference(
                player.bank,
                new_player_bank))

        return _update(
            game,
            new_turn=True,
            remove_card=(tier, card_i),
            new_bank=new_table_bank,
            new_player=(
                player_i,
                # Charge the cost to the player's bank
                Player.update_bank(
                    # Add the card to their purchased
                    Player.add_card_to_purchased(player, card),
                    new_player_bank)))

    return None

def return_gold(game, gold_number):
    player_i = (game.turn - 1) % len(game.players)
    player = game.players[player_i]
    if sum(player.bank) > d.MAX_PLAYER_TOKENS:
        new_player_bank = player.bank._replace(gold=player.bank.gold - gold_number)
        if Bank.is_solvent(new_player_bank):
            new_table_bank = game.bank._replace(
                gold=game.bank.gold + gold_number)

            return _update(
                game,
                new_bank=new_table_bank,
                new_player_bank=(player_i, new_player_bank))

def return_gem(game, gems):
    player_i = (game.turn - 1) % len(game.players)
    player = game.players[player_i]

    try:
        if sum(player.bank) > d.MAX_PLAYER_TOKENS:
            new_player_bank = Bank.pay_gems(
                player.bank,
                None,
                gems,
                # Don't allow us to pay with gold to cover this cost
                allow_gold=False)
            if Bank.is_solvent(new_player_bank):
                # Charge the cost to the player's bank
                new_table_bank = Bank.receive_bank(
                    game.bank,
                    Bank(*gems))

                return _update(
                    game,
                    new_bank=new_table_bank,
                    new_player_bank=(player_i, new_player_bank))
    except TypeError:
        import pudb; pudb.set_trace()
        pass

def accept_noble(game, noble_i):
    player_i = (game.turn - 1) % len(game.players)
    player = game.players[player_i]
    if noble_i < Noble.number_visible(game.players):
        try:
            noble = game.nobles_deck[noble_i]
            if Noble.would_visit(noble, player):
                return _update(
                    game,
                    accept_noble=(player_i, noble_i))
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
    RETURN_G = (return_gold, (1, ))

class ValidPlayerActions(Enum):
    # 3 combos
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

    # 2 combos
    PICK_DS = (pick_gems, (Gems(diamond=1, sapphire=1),))
    PICK_DE = (pick_gems, (Gems(diamond=1, emerald=1),))
    PICK_DR = (pick_gems, (Gems(diamond=1, ruby=1),))
    PICK_DO = (pick_gems, (Gems(diamond=1, onyx=1),))
    PICK_SE = (pick_gems, (Gems(sapphire=1, emerald=1),))
    PICK_SR = (pick_gems, (Gems(sapphire=1, ruby=1),))
    PICK_SO = (pick_gems, (Gems(sapphire=1, onyx=1),))
    PICK_ER = (pick_gems, (Gems(emerald=1, ruby=1),))
    PICK_EO = (pick_gems, (Gems(emerald=1, onyx=1),))
    PICK_RO = (pick_gems, (Gems(ruby=1, onyx=1),))

    # 1 Combos
    PICK_D = (pick_gems, (Gems(diamond=1),))
    PICK_E = (pick_gems, (Gems(emerald=1),))
    PICK_S = (pick_gems, (Gems(sapphire=1),))
    PICK_R = (pick_gems, (Gems(ruby=1),))
    PICK_O = (pick_gems, (Gems(onyx=1),))

    # doubles
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

def eval_action(game, action_enum):
    return action_enum.value[0](game, *action_enum.value[1])

def valid_actions(game):
    for action in ValidPlayerActions:
        new_game = eval_action(game, action)
        if new_game:
            yield PerformedAction(action=action, game=new_game)

def valid_payback_actions_for_last_player(game):
    for action in ValidGemPaybackActions:
        new_game = eval_action(game, action)
        if new_game:
            yield PerformedAction(action=action, game=new_game)

def valid_nobles_for_last_player(game):
    for action in ValidNobleActions:
        new_game = eval_action(game, action)
        if new_game:
            yield PerformedAction(action=action, game=new_game)

def next_game_actions(game):
    # If there are > 10 we need to give some gems back
    if (actions := list(valid_payback_actions_for_last_player(game))):
        return (False, actions)
    # If there are nobles, we need to accept some
    if (actions := list(valid_nobles_for_last_player(game))):
        return (False, actions)

    # Otherwise
    return (True, list(valid_actions(game)))
