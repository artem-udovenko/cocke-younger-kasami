from src.grammar.grammar import Grammar
from src.cyk import CYK
import unittest

class TestCYK(unittest.TestCase):
    def test_small_cyk(self):
        grammar = Grammar(
            "SAB",
            "ab",
            ["S->AB", "A->a", "B->b"],
            "S"
        )
        predict = CYK.parser(grammar)
        self.assertTrue(predict("ab"))
        self.assertFalse(predict("a"))

    def test_big_cyk(self):
        grammar = Grammar(
            "SAB",
            "ab",
            ["S->AB", "A->AA", "A->a", "B->b"],
            "S"
        )
        predict = CYK.parser(grammar)
        self.assertTrue(predict("aaaaaab"))
        self.assertFalse(predict("aaaaaaa"))

    def test_long_cyk(self):
        grammar = Grammar(
            "SAB",
            "abo",
            ["S->B", "A->oba", "B->baAb"],
            "S"
        )
        predict = CYK.parser(grammar)
        self.assertTrue(predict("baobab"))
        self.assertFalse(predict("bab"))

    def test_eps_cyk(self):
        grammar = Grammar(
            "SAB",
            "ab",
            ["S->AB", "A->a", "B->b", "S->A", "A->"],
            "S"
        )
        predict = CYK.parser(grammar)
        self.assertTrue(predict(""))

    def test_mixed_cyk(self):
        grammar = Grammar(
            "SABCD",
            "abo",
            ["S->BC", "A->oba", "B->baAb", "C->", "C->DD", "D->", "D->baobab", "D->aboba"],
            "S"
        )
        predict = CYK.parser(grammar)
        self.assertTrue(predict("baobabbaobab"))
        self.assertTrue(predict("baobababobabaobab"))


if __name__ == '__main__':
    unittest.main()