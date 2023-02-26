from collections import namedtuple
from termcolor import colored
import py_cui

import splendor.actions as actions
from splendor.actions import ValidPlayerActions
from splendor.types import Tabletop

TABLETOP = None
def set_current_tabletop(new_tabletop):
    global TABLETOP
    TABLETOP = new_tabletop

def get_current_tabletop():
    global TABLETOP
    return TABLETOP

def setup_ui(root, update_fn):
    root.toggle_unicode_borders()
    root.set_title("Splendor")
    Widgets = namedtuple(
        "Widgets",
        [
            "command_selection",
            "table_bank"
        ])

    widgets = Widgets(
        command_selection=root.add_scroll_menu(
            'Available Actions',
            0,
            0,
            row_span=14,
            column_span=6),
        table_bank=dict(
            label=root.add_label(
                'Bank',
                4,
                6,
                row_span=1,
                column_span=1),
            gold=root.add_label('G', 4, 7, row_span=1, column_span=1),
            diamond=root.add_label('D', 4, 8, row_span=1, column_span=1),
            emerald=root.add_label('E', 4, 9, row_span=1, column_span=1),
            sapphire=root.add_label('S', 4, 10, row_span=1, column_span=1),
            ruby=root.add_label('R', 4, 11, row_span=1, column_span=1),
            onyx=root.add_label('O', 4, 12, row_span=1, column_span=1))
    )

    def perform_action(widget):
        action = ValidPlayerActions[widget.get()]

        set_current_tabletop(actions.apply_action(get_current_tabletop(), action))

        update_fn(widgets, get_current_tabletop())

    widgets.command_selection.add_key_command(
        py_cui.keys.KEY_ENTER,
        lambda: perform_action(widgets.command_selection))

    root.move_focus(widgets.command_selection)

    update_fn(widgets, get_current_tabletop())

def update_bank_widget(widget, count, color):
    widget.set_title(f"{count} ●")
    if (count > 0):
        widget.set_color(color)
    else:
        widget.set_color(py_cui.RED_ON_WHITE)

def update_ui(widgets, tabletop):
    widgets.command_selection.clear()
    widgets.command_selection.add_item_list([a.name for a in actions.valid_actions(tabletop)])

    update_bank_widget(widgets.table_bank['gold'], tabletop.bank.gold, py_cui.YELLOW_ON_BLACK)
    update_bank_widget(widgets.table_bank['emerald'], tabletop.bank.emerald, py_cui.GREEN_ON_BLACK)
    update_bank_widget(widgets.table_bank['diamond'], tabletop.bank.diamond, py_cui.CYAN_ON_BLACK)
    update_bank_widget(widgets.table_bank['sapphire'], tabletop.bank.sapphire, py_cui.BLUE_ON_BLACK)
    update_bank_widget(widgets.table_bank['ruby'], tabletop.bank.ruby, py_cui.RED_ON_BLACK)
    update_bank_widget(widgets.table_bank['onyx'], tabletop.bank.onyx, py_cui.BLACK_ON_WHITE)


if __name__ == "__main__":
    import sys
    seed = None
    players = 4
    if len(sys.argv) > 2:
        players = int(sys.argv[1])
    if len(sys.argv) > 2:
        seed = int(sys.argv[2])

    root = py_cui.PyCUI(14, 20)
    set_current_tabletop(Tabletop.setup_game(players=players, seed=seed))

    setup_ui(root, update_ui)

    root.start()
