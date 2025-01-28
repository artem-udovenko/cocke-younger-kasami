from src.grammar.grammar import Grammar
from src.grammar.wrapper import Wrapper
from tools.grammar_traits import GrammarTraits
from tools.queue import Queue
from typing import Set

class Chomsky:
    @staticmethod
    def to_chomsky_normal_form(grammar: Grammar):
        Chomsky.remove_right_start(grammar)
        Chomsky.remove_mixed_rules(grammar)
        Chomsky.remove_long_rules(grammar)
        Chomsky.remove_eps_producing(grammar)
        Chomsky.remove_single_rules(grammar)
        Chomsky.remove_bad_nonterminals(grammar)
        return grammar

    @staticmethod
    def remove_right_start(grammar: Grammar):
        new_start = GrammarTraits.new_chr(grammar.terminals | grammar.nonterminals)
        grammar.add_nonterminal(new_start)
        grammar.add_rule(GrammarTraits.unite_rule(new_start, Wrapper(grammar.start)))
        grammar.change_start(new_start)
        return grammar

    @staticmethod
    def remove_mixed_rules(grammar: Grammar):
        changes = dict()
        for nt in grammar.rules.keys():
            for i in range(len(grammar.rules[nt])):
                occurred = set(str(grammar.rules[nt][i]))
                if len(grammar.rules[nt][i]) > 1 and occurred & grammar.terminals:
                    for ch in grammar.rules[nt][i].string:
                        if ch in grammar.terminals and ch not in changes:
                            changes[ch] = GrammarTraits.new_chr(grammar.terminals | grammar.nonterminals)
                            grammar.add_nonterminal(changes[ch])
                    grammar.rules[nt][i] = grammar.rules[nt][i].image(changes)
        for tm in changes:
            grammar.add_rule(GrammarTraits.unite_rule(changes[tm], Wrapper(tm)))
        return grammar

    @staticmethod
    def remove_long_rules(grammar: Grammar):
        new_rules = []
        for nt in grammar.rules.keys():
            for i in range(len(grammar.rules[nt])):
                if len(grammar.rules[nt][i]) > 2:
                    string = grammar.rules[nt][i].string
                    left = GrammarTraits.new_chr(grammar.terminals | grammar.nonterminals)
                    grammar.add_nonterminal(left)
                    grammar.rules[nt][i].string = string[0] + left
                    for j in range(1, len(string) - 2):
                        new_nt = GrammarTraits.new_chr(grammar.terminals | grammar.nonterminals)
                        grammar.add_nonterminal(new_nt)
                        new_rules.append(f"{left}->{string[j]}{new_nt}")
                        left = new_nt
                    new_rules.append(f"{left}->{string[-2]}{string[-1]}")
        for rule in new_rules:
            grammar.add_rule(rule)
        return grammar

    @staticmethod
    def detect_producing(grammar: Grammar, patterns: Set[str]):
        mask = []
        prod = dict()
        address = dict()
        for nt in grammar.nonterminals:
            address[nt] = set()
            prod[nt] = False
        queue = Queue()
        for nt, right in GrammarTraits.iterate_rules(grammar):
            if right in patterns:
                prod[nt] = True
                queue.push(nt)
            elif right[0] in grammar.nonterminals:
                mask.append([nt, set(right)])
                for ch in right:
                    address[ch].add(len(mask) - 1)
        while not queue.empty():
            nt = queue.pop()
            for i in address[nt]:
                mask[i][1] -= {nt}
                if len(mask[i][1]) == 0 and not prod[mask[i][0]]:
                    prod[mask[i][0]] = True
                    queue.push(mask[i][0])
        return prod

    @staticmethod
    def remove_eps_producing(grammar: Grammar):
        eps_prod = Chomsky.detect_producing(grammar, {""})
        new_rules = []
        for nt, right in GrammarTraits.iterate_rules(grammar):
            if right != "":
                new_rules.append(f"{nt}->{right}")
            if set(right) & grammar.nonterminals:
                for i in range(len(right)):
                    if eps_prod[right[i]]:
                        new_right = right[:i] + right[i + 1:]
                        if len(new_right) != 0:
                            new_rules.append(f"{nt}->{new_right}")
        if eps_prod[grammar.start]:
            new_rules.append(f"{grammar.start}->")
        new_grammar = Grammar(
            "".join(grammar.nonterminals),
            "".join(grammar.terminals),
            new_rules,
            grammar.start
        )
        grammar.rules = new_grammar.rules
        return grammar

    @staticmethod
    def dfs(visited, tree, nt):
        visited.add(nt)
        for new_nt in tree[nt]:
            if new_nt not in visited:
                Chomsky.dfs(visited, tree, new_nt)

    @staticmethod
    def remove_single_rules(grammar: Grammar):
        tree = dict()
        for nt in grammar.nonterminals:
            tree[nt] = []
        for nt, right in GrammarTraits.iterate_rules(grammar):
            if str(right) in grammar.nonterminals:
                tree[nt].append(str(right))
        new_rules = []
        for nt in grammar.nonterminals:
            attainable = set()
            Chomsky.dfs(attainable, tree, nt)
            # attainable -= {nt}
            for new_nt in attainable:
                if new_nt in grammar.rules:
                    for right in grammar.rules[new_nt]:
                        if str(right) not in grammar.nonterminals:
                            new_rules.append(f"{nt}->{right}")
        new_grammar = Grammar(
            "".join(grammar.nonterminals),
            "".join(grammar.terminals),
            new_rules,
            grammar.start
        )
        grammar.rules = new_grammar.rules
        return grammar

    @staticmethod
    def remove_bad_nonterminals(grammar: Grammar):
        Chomsky.remove_nonproductive(grammar)
        Chomsky.remove_unattainable(grammar)
        return grammar

    @staticmethod
    def remove_nonproductive(grammar: Grammar):
        prod = Chomsky.detect_producing(grammar, {""} | grammar.terminals)
        prod = set([nt for nt in prod if prod[nt]])
        non_prod = grammar.nonterminals - prod
        new_rules = []
        for nt, right in GrammarTraits.iterate_rules(grammar):
            if not (set(nt) & non_prod or set(right) & non_prod):
                new_rules.append(f"{nt}->{right}")
        new_grammar = Grammar(
            "".join(grammar.nonterminals),
            "".join(grammar.terminals),
            new_rules,
            grammar.start
        )
        grammar.rules = new_grammar.rules
        grammar.nonterminals = (grammar.nonterminals - non_prod) | {grammar.start}
        return grammar

    @staticmethod
    def remove_unattainable(grammar: Grammar):
        tree = dict()
        for nt in grammar.nonterminals:
            tree[nt] = set()
        for nt, right in GrammarTraits.iterate_rules(grammar):
            tree[nt] |= set(right) & grammar.nonterminals
        attainable = set()
        Chomsky.dfs(attainable, tree, grammar.start)
        non_attainable = grammar.nonterminals - attainable
        for nt in non_attainable:
            if nt in grammar.rules:
                grammar.rules.pop(nt)
        grammar.nonterminals -= non_attainable
        return grammar
