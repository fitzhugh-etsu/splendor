from splendor.types import Bank, Gems, Player


def can_afford(player, card):
    # Pay with bank (pay with your gems, but this *can* go negative (requiring gold to make up the difference))
    cost_after_payment = Bank.subtract_gems(
        player.bank,
        # Discount from bonus (cost of a card after bonus can't go negative, so max to 0)
        Gems.subtract(
            card.cost,
            Player.player_bonus(player),
            allow_negative=False),
        allow_negative=True)

    # Cover any deficit with gold
    # For each cost which is negative, can we cover the cost?
    new_bank = Bank(
        # Assuming all debts are covered, we max(0,...)  the error will play out in gold < > 0
        *[max(0, cost_after_payment[i]) for i in range(len(Gems()))],
        # Gold remaining is previous + any deficit spending we did.
        gold=player.bank.gold + sum([deficit for deficit in cost_after_payment if deficit < 0]))

    # if it's a valid bank - return it!
    if Bank.is_solvent(new_bank):
        return player._replace(bank=new_bank)
    else:
        return None
