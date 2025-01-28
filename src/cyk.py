from src.grammar.grammar import Grammar
from tools.grammar_traits import GrammarTraits
from src.chomsky import Chomsky
from copy import deepcopy

class CYK:
    @staticmethod
    def parser(grammar: Grammar):
        new_grammar = deepcopy(grammar)
        Chomsky.to_chomsky_normal_form(new_grammar)
        # new_grammar = GrammarTraits.rename(new_grammar)
        def predict(word: str):
            if word == "":
                for right in new_grammar.rules[new_grammar.start]:
                    if str(right) == "":
                        return True
                return False
            dp = dict()
            for nt in new_grammar.nonterminals:
                dp[nt] = [[False] * len(word) for _ in range(len(word))]
            for i in range(len(word)):
                for nt in new_grammar.nonterminals:
                    for right in new_grammar.rules[nt]:
                        if str(right) == word[i]:
                            dp[nt][i][i] = True
            for d in range(len(word)):
                for i in range(len(word) - d):
                    j = i + d
                    for nt, right in GrammarTraits.iterate_rules(new_grammar):
                        if set(right) & new_grammar.nonterminals:
                            for k in range(i, j):
                                dp[nt][i][j] |= dp[right[0]][i][k] & dp[right[1]][k + 1][j]
            return dp[new_grammar.start][0][len(word) - 1]
        return predict
