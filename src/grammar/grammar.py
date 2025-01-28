from src.grammar.wrapper import Wrapper
from tools.errors import AssembleError, RuleError, TerminalError, StartError
from typing import List


class Grammar:
    def __init__(self, nonterminals: str, terminals: str, rules: List[str], start: str):
        self.nonterminals = set(nonterminals.replace(" ", ""))
        self.terminals = set(terminals.replace(" ", ""))
        self.rules = dict()
        for rule in rules:
            self.process_rule(rule)
        if start not in self.nonterminals:
            raise StartError(start)
        self.start = start

    def process_rule(self, rule_src: str):
        rule = rule_src.replace(" ", "").split("->")
        if len(rule) != 2:
            raise RuleError(rule_src)
        if rule[0] not in self.nonterminals:
            raise TerminalError(rule[0], rule_src)
        for char in rule[1]:
            if char not in self.terminals | self.nonterminals:
                raise AssembleError(char, rule_src)
        if rule[0] not in self.rules.keys():
            self.rules[rule[0]] = [Wrapper(rule[1])]
        else:
            self.rules[rule[0]].append(Wrapper(rule[1]))

    def add_terminal(self, terminal: str):
        self.terminals.add(terminal)

    def add_nonterminal(self, nonterminal: str):
        self.nonterminals.add(nonterminal)

    def add_rule(self, rule: str):
        self.process_rule(rule)

    def change_start(self, start: str):
        if start not in self.nonterminals:
            raise StartError(start)
        self.start = start

    def __str__(self):
        return\
f"""Σ : {self.terminals}
N : {self.nonterminals}
S : {self.start}
Δ :\n{"\n".join([f"{i}->{j}" for i in self.rules.keys() for j in self.rules[i]])}"""