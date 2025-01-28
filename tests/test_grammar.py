from src.grammar.grammar import Grammar
from tools.errors import AssembleError
import unittest

class TestGrammar(unittest.TestCase):
    def test_init(self):
        grammar = Grammar(
            "SA",
            "ab",
            ["S->ba", "A->b"],
            "S"
        )
        self.assertTrue("a" in grammar.terminals)
        self.assertTrue("A" in grammar.nonterminals)
        self.assertEqual(len(grammar.rules["S"]), 1)
        with self.assertRaises(AssembleError):
            grammar = Grammar(
                "SA",
                "a",
                ["S->ba", "A->b"],
                "S"
            )

    def test_interaction(self):
        grammar = Grammar(
            "SA",
            "a",
            ["S->", "A->a"],
            "S"
        )
        grammar.add_terminal("b")
        self.assertTrue("b" in grammar.terminals)
        grammar.add_nonterminal("B")
        self.assertTrue("B" in grammar.nonterminals)
        grammar.add_rule("B->")
        self.assertEqual(len(grammar.rules["B"]), 1)
        grammar.change_start("B")
        self.assertEqual(grammar.start, "B")
        self.assertIn("S->", str(grammar))

if __name__ == '__main__':
    unittest.main()