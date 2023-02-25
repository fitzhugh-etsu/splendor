from collections import namedtuple

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
            "command_selection"
        ])

    widgets = Widgets(
        command_selection=root.add_scroll_menu(
            'Available Actions',
            0,
            0,
            row_span=14,
            column_span=6)
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

def update_ui(widgets, tabletop):
    widgets.command_selection.clear()
    widgets.command_selection.add_item_list([a.name for a in actions.valid_actions(tabletop)])


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
