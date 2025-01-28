from src.grammar.grammar import Grammar
from tools.grammar_traits import GrammarTraits
from src.chomsky import Chomsky
import unittest

class TestChomsky(unittest.TestCase):
    def test_remove_right_start(self):
        grammar = Grammar(
            "S",
            "",
            ["S->SS"],
            "S"
        )
        Chomsky.remove_right_start(grammar)
        self.assertEqual(len(grammar.nonterminals), 2)

    def test_remove_mixed_rules(self):
        grammar = Grammar(
            "S",
            "a",
            ["S->Sa"],
            "S"
        )
        Chomsky.remove_mixed_rules(grammar)
        for nt, right in GrammarTraits.iterate_rules(grammar):
            self.assertFalse(set(right) & grammar.nonterminals and set(right) & grammar.terminals)

    def test_remove_long_rules(self):
        grammar = Grammar(
            "SABCD",
            "",
            ["S->ABCD"],
            "S"
        )
        Chomsky.remove_long_rules(grammar)
        for nt, right in GrammarTraits.iterate_rules(grammar):
            self.assertTrue(len(right) < 3)

    def test_remove_eps_producing(self):
        grammar = Grammar(
            "SA",
            "",
            ["S->A", "A->"],
            "S"
        )
        Chomsky.remove_eps_producing(grammar)
        self.assertEqual("", str(grammar.rules["S"][1]))
        self.assertNotIn("A", grammar.rules)

    def test_remove_single_rules(self):
        grammar = Grammar(
            "SABC",
            "",
            ["S->A", "A->BC"],
            "S"
        )
        Chomsky.remove_single_rules(grammar)
        for nt, right in GrammarTraits.iterate_rules(grammar):
            self.assertFalse(set(right) & grammar.nonterminals and len(right) == 1)

    def test_remove_nonproductive(self):
        grammar = Grammar(
            "SA",
            "",
            ["S->A"],
            "S"
        )
        Chomsky.remove_nonproductive(grammar)
        self.assertEqual(len(grammar.nonterminals), 1)
        self.assertEqual(len(grammar.rules), 0)

    def test_remove_unattainable(self):
        grammar = Grammar(
            "SABC",
            "",
            ["S->A", "B->C"],
            "S"
        )
        Chomsky.remove_unattainable(grammar)
        self.assertEqual(len(grammar.nonterminals), 2)

if __name__ == '__main__':
    unittest.main()