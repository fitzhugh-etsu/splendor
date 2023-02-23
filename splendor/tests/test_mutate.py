import unittest

import splendor.data as d
import splendor.mutate as m


class TestMutate(unittest.TestCase):
    def test_purchase_card(self):
        decks = (
            (d.Card(points=1), d.Card(points=2), d.Card(points=3)),
            (d.Card(points=11), d.Card(points=12), d.Card(points=13)),
            (d.Card(points=21), d.Card(points=22), d.Card(points=23)))
        self.assertEqual((
            (d.Card(points=2), d.Card(points=3)),
            (d.Card(points=11), d.Card(points=12), d.Card(points=13)),
            (d.Card(points=21), d.Card(points=22), d.Card(points=23))),
            m.remove_card_from_deck(decks, 0, 0))

        self.assertEqual((
            (d.Card(points=1), d.Card(points=2), d.Card(points=3)),
            (d.Card(points=11), d.Card(points=13)),
            (d.Card(points=21), d.Card(points=22), d.Card(points=23))),
            m.remove_card_from_deck(decks, 1, 1))

        self.assertEqual((
            (d.Card(points=1), d.Card(points=2), d.Card(points=3)),
            (d.Card(points=11), d.Card(points=12), d.Card(points=13)),
            (d.Card(points=21), d.Card(points=22))),
            m.remove_card_from_deck(decks, 2, 2))

    @unittest.skip("Unimplemented")
    def test_player_purchase_card(self):
        pass

    @unittest.skip("Unimplemented")
    def test_update_players(self):
        pass
