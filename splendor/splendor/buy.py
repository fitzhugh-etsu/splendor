import splendor.data as d


def is_solvent(bank):
    return all([v >= 0 for v in bank])

def player_bonus(player):
    return d.Gems(*[sum([card.bonus[i] for card in player.purchased]) for i in range(len(d.Gems()))])

def can_afford(player, card):
    # Calculate our player's current bonus
    bonus = player_bonus(player)

    # Discount from bonus (cost of a card can't go negative, so max to 0)
    cost_after_bonus = d.Gems(*[max(0, card.cost[i] - bonus[i]) for i in range(len(d.Gems()))])

    # Pay with bank (pay with your gems, but this *can* go negative (requiring gold to make up the difference))
    cost_after_payment = d.Gems(*[player.bank[i] - cost_after_bonus[i] for i in range(len(d.Gems()))])

    # Cover any deficit with gold
    # For each cost which is negative, can we cover the cost?
    new_bank = d.Bank(
        # Assuming all debts are covered, we max(0,...)  the error will play out in gold < > 0
        *[max(0, cost_after_payment[i]) for i in range(len(d.Gems()))],
        # Gold remaining is previous + any deficit spending we did.
        gold=player.bank.gold + sum([deficit for deficit in cost_after_payment if deficit < 0]))

    # if it's a valid bank - return it!
    if is_solvent(new_bank):
        return player._replace(bank=new_bank)
    else:
        return None
