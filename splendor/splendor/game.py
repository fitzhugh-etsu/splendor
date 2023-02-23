import splendor.data as d
import splendor.decks as decks


def setup_game(seed=0, players=4):
    gem_count = 7
    if players == 3:
        gem_count = 5
    elif players == 2:
        gem_count = 4

    return d.Tabletop(
        noble_deck=decks.nobles_deck(seed=seed),
        decks=(decks.tier_0_deck(seed=seed),
               decks.tier_1_deck(seed=seed),
               decks.tier_2_deck(seed=seed)),
        bank=d.Bank(
            gold=5,
            diamond=gem_count,
            sapphire=gem_count,
            emerald=gem_count,
            ruby=gem_count,
            onyx=gem_count),
        players=(d.Player(),) * players)

print(setup_game(players=4))
