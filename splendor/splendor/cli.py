import itertools
import pickle
import sys
import time

import lmdb
import py_cui
from dotted_dict import DottedDict

import splendor.actions as actions
from splendor.models import Game, Noble, Player

TABLETOP = None
DB = lmdb.open(f"games/{int(time.time())}.splendor")

def set_current_game(new_game):
    global TABLETOP
    if not TABLETOP:
        with DB.begin(write=True) as in_txn:
            in_txn.put(
                pickle.dumps(None),
                pickle.dumps((None, new_game)))

    TABLETOP = new_game

def get_current_game():
    global TABLETOP
    return TABLETOP

def update_game(action):
    with DB.begin(write=True) as in_txn:
        in_txn.put(
            pickle.dumps(get_current_game().turn),
            pickle.dumps((action, get_current_game())))

    set_current_game(action.game)

def bank_widgets(root, label, row, col):
    widget = DottedDict(dict(
        label=root.add_label(
            label,
            row,
            col,
            row_span=1,
            column_span=1),
        gold=root.add_label('G', row, col + 1),
        diamond=root.add_label('D', row, col + 2),
        emerald=root.add_label('E', row, col + 3),
        sapphire=root.add_label('S', row, col + 4),
        ruby=root.add_label('R', row, col + 5),
        onyx=root.add_label('O', row, col + 6)))

    widget.gold.set_color(py_cui.YELLOW_ON_BLACK)
    widget.emerald.set_color(py_cui.GREEN_ON_BLACK)
    widget.diamond.set_color(py_cui.CYAN_ON_BLACK)
    widget.sapphire.set_color(py_cui.BLUE_ON_BLACK)
    widget.ruby.set_color(py_cui.RED_ON_BLACK)
    widget.onyx.set_color(py_cui.BLACK_ON_WHITE)

    return widget

def bonus_widgets(root, row, col):
    widget = DottedDict(
        dict(
            label=root.add_label(
                "🏆",
                row,
                col,
                row_span=1,
                column_span=1),
            points=root.add_label('☆', row, col + 1, row_span=1, column_span=1),
            diamond=root.add_label('D', row, col + 2, row_span=1, column_span=1),
            emerald=root.add_label('E', row, col + 3, row_span=1, column_span=1),
            sapphire=root.add_label('S', row, col + 4, row_span=1, column_span=1),
            ruby=root.add_label('R', row, col + 5, row_span=1, column_span=1),
            onyx=root.add_label('O', row, col + 6, row_span=1, column_span=1)))

    widget.points.set_color(py_cui.WHITE_ON_BLACK)
    widget.emerald.set_color(py_cui.GREEN_ON_BLACK)
    widget.diamond.set_color(py_cui.CYAN_ON_BLACK)
    widget.sapphire.set_color(py_cui.BLUE_ON_BLACK)
    widget.ruby.set_color(py_cui.RED_ON_BLACK)
    widget.onyx.set_color(py_cui.BLACK_ON_WHITE)
    return widget

def card_widget(root, row, col):
    label = DottedDict(
        dict(
            bonus=root.add_label("", row, col),
            points=root.add_label("", row, col + 1),
            costs=[
                root.add_label("", row, col + 2),
                root.add_label("", row, col + 3),
                root.add_label("", row, col + 4),
                root.add_label("", row, col + 5),
                root.add_label("", row, col + 6)]))

    label.bonus.add_text_color_rule('G', py_cui.YELLOW_ON_BLACK, 'endswith')
    label.bonus.add_text_color_rule('E', py_cui.GREEN_ON_BLACK, 'endswith')
    label.bonus.add_text_color_rule('D', py_cui.CYAN_ON_BLACK, 'endswith')
    label.bonus.add_text_color_rule('S', py_cui.BLUE_ON_BLACK, 'endswith')
    label.bonus.add_text_color_rule('R', py_cui.RED_ON_BLACK, 'endswith')
    label.bonus.add_text_color_rule('O', py_cui.BLACK_ON_WHITE, 'endswith')

    for cost in label.costs:
        cost.add_text_color_rule('G', py_cui.YELLOW_ON_BLACK, 'endswith')
        cost.add_text_color_rule('E', py_cui.GREEN_ON_BLACK, 'endswith')
        cost.add_text_color_rule('D', py_cui.CYAN_ON_BLACK, 'endswith')
        cost.add_text_color_rule('S', py_cui.BLUE_ON_BLACK, 'endswith')
        cost.add_text_color_rule('R', py_cui.RED_ON_BLACK, 'endswith')
        cost.add_text_color_rule('O', py_cui.BLACK_ON_WHITE, 'endswith')

    return label

def noble_widget(root, row, col):
    label = DottedDict(
        dict(
            points=root.add_label("", row, col),
            costs=[
                root.add_label("", row, col + 1),
                root.add_label("", row, col + 2),
                root.add_label("", row, col + 3),
                root.add_label("", row, col + 4),
                root.add_label("", row, col + 5)]))

    for cost in label.costs:
        cost.add_text_color_rule('G', py_cui.YELLOW_ON_BLACK, 'endswith')
        cost.add_text_color_rule('E', py_cui.GREEN_ON_BLACK, 'endswith')
        cost.add_text_color_rule('D', py_cui.CYAN_ON_BLACK, 'endswith')
        cost.add_text_color_rule('S', py_cui.BLUE_ON_BLACK, 'endswith')
        cost.add_text_color_rule('R', py_cui.RED_ON_BLACK, 'endswith')
        cost.add_text_color_rule('O', py_cui.BLACK_ON_WHITE, 'endswith')

    return label

def reserved_widgets(root, row, col):
    labels = dict(
        labels=[
            root.add_label("-", row + 0, col),
            root.add_label("-", row + 1, col),
            root.add_label("-", row + 2, col)],
        reserved=[
            card_widget(root, row + 0, col + 1),
            card_widget(root, row + 1, col + 1),
            card_widget(root, row + 2, col + 1)])
    return labels

def nobles_widgets(root, row, col):
    labels = dict(
        label=root.add_block_label(
            "♔",
            row,
            col,
            row_span=1,
            column_span=1),
        nobles=[
            noble_widget(root, row + 0, col + 2),
            noble_widget(root, row + 1, col + 2),
            noble_widget(root, row + 2, col + 2),
            noble_widget(root, row + 3, col + 2),
            noble_widget(root, row + 4, col + 2)])

    return labels

def tier_widgets(root, row, col):
    return dict(
        label=root.add_label(
            "🂠",
            row,
            col,
            row_span=1,
            column_span=1),
        cards=[
            card_widget(root, row + 0, col + 2),
            card_widget(root, row + 1, col + 2),
            card_widget(root, row + 2, col + 2),
            card_widget(root, row + 3, col + 2)])

def setup_ui(root, update_fn):
    root.toggle_unicode_borders()
    root.set_title("Splendor")

    widgets = DottedDict(
        dict(
            turns=root.add_label("", 0, 0),
            command_selection=root.add_scroll_menu(
                'Available Actions', 1, 0,
                row_span=14, column_span=6),
            players=[
                dict(
                    bank=bank_widgets(root, "P 0", 0, 6),
                    bonus=bonus_widgets(root, 1, 6),
                    reserved=reserved_widgets(root, 2, 6)),
                dict(
                    bank=bank_widgets(root, "P 1", 5, 6),
                    bonus=bonus_widgets(root, 6, 6),
                    reserved=reserved_widgets(root, 7, 6)),
                dict(
                    bank=bank_widgets(root, "P 2", 10, 6),
                    bonus=bonus_widgets(root, 11, 6),
                    reserved=reserved_widgets(root, 12, 6)),
                dict(
                    bank=bank_widgets(root, "P 3", 15, 6),
                    bonus=bonus_widgets(root, 16, 6),
                    reserved=reserved_widgets(root, 17, 6))],

            table_bank=bank_widgets(root, "Table", 0, 15),
            nobles=nobles_widgets(root, 1, 15),
            tiers=[
                tier_widgets(root, 8, 15),
                tier_widgets(root, 13, 15),
                tier_widgets(root, 18, 15)]))

    def perform_action(widget):
        action = widget.get()

        update_game(action)

        update_fn(widgets, get_current_game())

    widgets.command_selection.add_key_command(
        py_cui.keys.KEY_ENTER,
        lambda: perform_action(widgets.command_selection))

    root.move_focus(widgets.command_selection)

    update_fn(widgets, get_current_game())


def update_gem_widget(widget, count, color, blank_color=None):
    widget.set_title(f"{int(count)}●")
    if (count > 0):
        widget.set_color(color)
    else:
        widget.set_color(blank_color or color)

def update_bonus(collection, player):
    bonus = Player.get_bonus(player)
    points = Player.points(player)
    collection.points.set_title(f"{points}☆")

    update_gem_widget(
        collection.emerald,
        bonus.emerald,
        py_cui.GREEN_ON_BLACK,
        None)

    update_gem_widget(
        collection.diamond,
        bonus.diamond,
        py_cui.CYAN_ON_BLACK,
        None)

    update_gem_widget(
        collection.sapphire,
        bonus.sapphire,
        py_cui.BLUE_ON_BLACK,
        None)

    update_gem_widget(
        collection.ruby,
        bonus.ruby,
        py_cui.RED_ON_BLACK,
        None)

    update_gem_widget(
        collection.onyx,
        bonus.onyx,
        py_cui.BLACK_ON_WHITE,
        None)

def card_cost(card):
    costs = []

    if card.cost.emerald:
        costs.append(f"{int(card.cost.emerald)}E")
    if card.cost.diamond:
        costs.append(f"{int(card.cost.diamond)}D")
    if card.cost.sapphire:
        costs.append(f"{int(card.cost.sapphire)}S")
    if card.cost.ruby:
        costs.append(f"{int(card.cost.ruby)}R")
    if card.cost.onyx:
        costs.append(f"{int(card.cost.onyx)}O")
    return costs

def noble_cost(noble):
    costs = []

    if noble.cost.emerald:
        costs.append(f"{noble.cost.emerald}E")
    if noble.cost.diamond:
        costs.append(f"{noble.cost.diamond}D")
    if noble.cost.sapphire:
        costs.append(f"{noble.cost.sapphire}S")
    if noble.cost.ruby:
        costs.append(f"{noble.cost.ruby}R")
    if noble.cost.onyx:
        costs.append(f"{noble.cost.onyx}O")
    return costs

def card_bonus_str(bonus):
    costs = []

    if bonus.emerald:
        costs.append(f"+{int(bonus.emerald)}E")
    if bonus.diamond:
        costs.append(f"+{int(bonus.diamond)}D")
    if bonus.sapphire:
        costs.append(f"+{int(bonus.sapphire)}S")
    if bonus.ruby:
        costs.append(f"+{int(bonus.ruby)}R")
    if bonus.onyx:
        costs.append(f"+{int(bonus.onyx)}O")
    return "".join(costs)

def update_bank(collection, bank):
    update_gem_widget(collection.gold, bank.gold, py_cui.YELLOW_ON_BLACK)
    update_gem_widget(collection.emerald, bank.emerald, py_cui.GREEN_ON_BLACK)
    update_gem_widget(collection.diamond, bank.diamond, py_cui.CYAN_ON_BLACK)
    update_gem_widget(collection.sapphire, bank.sapphire, py_cui.BLUE_ON_BLACK)
    update_gem_widget(collection.ruby, bank.ruby, py_cui.RED_ON_BLACK)
    update_gem_widget(collection.onyx, bank.onyx, py_cui.BLACK_ON_WHITE)

def update_card(widget, card, is_turn=False):
    if card:
        if card.hidden and not is_turn:
            for widget_c in widget.costs:
                widget_c.set_title("?")

            widget.bonus.set_title("?")
            widget.points.set_title("?")
        else:
            for (cost_val, widget_c) in itertools.zip_longest(card_cost(card), widget.costs):
                if cost_val:
                    widget_c.set_title(cost_val)
                else:
                    widget_c.set_title("")
            widget.bonus.set_title(card_bonus_str(card.bonus))
            widget.points.set_title(f"{card.points}☆")
    else:
        for widget_c in widget.costs:
            widget_c.set_title('')
        widget.bonus.set_title('')
        widget.points.set_title('')

def update_reserved(collection, player, is_turn=False):
    for i in range(0, 3):
        widget = collection.reserved[i]
        try:
            reserved = player.reserved[i]
            update_card(widget, reserved, is_turn=is_turn)
        except Exception:
            update_card(widget, None)

def update_noble(collection, noble):
    if noble:
        collection.points.set_title(f"{noble.points}☆")

        for (cost_val, widget_c) in itertools.zip_longest(noble_cost(noble), collection.costs):
            if cost_val:
                widget_c.set_title(cost_val)
            else:
                widget_c.set_title("")
    else:
        collection.points.set_title("")

        for widget_c in collection.costs:
            widget_c.set_title("")

def update_nobles(collection, number_visible, nobles):
    total = len(nobles)

    collection.label.set_title(f"{total-number_visible}♔")
    for i in range(number_visible):
        try:
            update_noble(collection.nobles[i], nobles[i])
        except IndexError:
            update_noble(collection.nobles[i], None)

def update_tier(tier, cards):
    total = max(0, len(cards) - 4)

    tier.label.set_title(f"{total}🂠")

    for i in range(4):
        if len(cards) > i:
            update_card(tier.cards[i], cards[i])
        else:
            update_card(tier.cards[i], None)

def update_ui(widgets, game):
    widgets.turns.set_title(f"Turn {game.turn}")

    for (i, player) in enumerate(game.players):
        if Player.won(player):
            raise Exception(f"Player {i} Won in {game.turn} turns")

    widgets.command_selection.clear()
    turn_completed, actions_list = actions.next_game_actions(game)
    widgets.command_selection.add_item_list(actions_list)

    for (i, player) in enumerate(game.players):
        if (turn_completed and Player.is_turn(game, i)) or (not turn_completed and Player.is_turn(game, i + 1)):
            widgets.players[i].bank.label.set_color(py_cui.BLACK_ON_WHITE)
        else:
            widgets.players[i].bank.label.set_color(py_cui.WHITE_ON_BLACK)

        update_bank(widgets.players[i].bank, player.bank)
        update_bonus(widgets.players[i].bonus, player)
        update_reserved(widgets.players[i].reserved, player, is_turn=Player.is_turn(game, i))

    update_bank(widgets.table_bank, game.bank)
    # Update nobles cards
    update_nobles(
        widgets.nobles,
        Noble.number_visible(game.players),
        game.nobles_deck)
    for (i, tier) in enumerate(reversed(game.decks)):
        update_tier(widgets.tiers[i], tier)

if __name__ == "__main__":
    seed = None
    players = 4
    if len(sys.argv) > 2:
        players = int(sys.argv[1])
    if len(sys.argv) > 2:
        seed = int(sys.argv[2])

    root = py_cui.PyCUI(30, 30)
    set_current_game(Game.setup_game(players=players, seed=seed))

    setup_ui(root, update_ui)

    root.start()
