from src.grammar.grammar import Grammar
from src.grammar.wrapper import Wrapper


class GrammarTraits:
    @staticmethod
    def new_chr(chars: set) -> str:
        for i in range(0x10FFFF):
            if chr(i) not in chars:
                return chr(i)

    @staticmethod
    def rename(grammar: Grammar) -> Grammar:
        if len(grammar.nonterminals) > 26:
            return grammar
        def standard():
            for ch in "ABCDEFGHIJKLMNOPQRTUVWXYZ":
                yield ch
        bijection = {grammar.start: "S"}
        standard = standard()
        for tm in grammar.terminals:
            bijection[tm] = tm
        for nt in grammar.nonterminals:
            if nt != grammar.start:
                bijection[nt] = next(standard)
        new_nonterminals = [bijection[nt] for nt in grammar.nonterminals]
        new_start = bijection[grammar.start]
        new_rules = []
        for i, j in [(i, j) for i in grammar.rules.keys() for j in grammar.rules[i]]:
            new_rules.append(f"{bijection[i]}->{j.image(bijection)}")
        return Grammar("".join(new_nonterminals), "".join(grammar.terminals), new_rules, new_start)

    @staticmethod
    def unite_rule(nt: str, right: Wrapper):
        return f"{nt}->{right.string}"

    @staticmethod
    def iterate_rules(grammar: Grammar):
        for nt, right in [(i, j.string) for i in grammar.rules.keys() for j in grammar.rules[i]]:
            yield nt, right
