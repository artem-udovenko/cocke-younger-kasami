from src.grammar.grammar import Grammar
from src.chomsky import Chomsky
from tools.grammar_traits import GrammarTraits
from src.cyk import CYK

def main():
    # grammar = Grammar(
    #     "SA",
    #     "ab",
    #     ["S->ba", "A->b"],
    #     "S"
    # )
    # print(grammar)
    # Chomsky.remove_mixed_rules(grammar)
    # grammar = GrammarTraits.rename(grammar)
    # print(grammar)
    # grammar = Grammar(
    #     "SABCD",
    #     "abcd",
    #     ["S->ABC", "A->BCD"],
    #     "S"
    # )
    # print(grammar)
    # Chomsky.remove_long_rules(grammar)
    # grammar = GrammarTraits.rename(grammar)
    # print(grammar)
    # grammar = Grammar(
    #     "SAB",
    #     "",
    #     ["S->AB", "A->", "B->"],
    #     "S"
    # )
    # print(grammar)
    # Chomsky.remove_eps_producing(grammar)
    # grammar = GrammarTraits.rename(grammar)
    # print(grammar)
    # grammar = Grammar(
    #     "SABC",
    #     "",
    #     ["S->A", "A->B", "A->C", "B->BC", "C->AC"],
    #     "S"
    # )
    # print(grammar)
    # Chomsky.remove_single_rules(grammar)
    # print(grammar)
    # grammar = Grammar(
    #     "SABC",
    #     "c",
    #     ["S->A", "A->B", "C->c"],
    #     "S"
    # )
    # print(grammar)
    # Chomsky.remove_nonproductive(grammar)
    # print(grammar)
    # grammar = Grammar(
    #     "SABCD",
    #     "",
    #     ["S->A", "A->BC", "D->BC"],
    #     "S"
    # )
    # print(grammar)
    # Chomsky.remove_unattainable(grammar)
    # print(grammar)

    # grammar = Grammar(
    #     "STUVXY",
    #     "ab",
    #     ["S->TaT",
    #      "T->UV",
    #      "T->XbX",
    #      "U->XY",
    #      "X->Xa",
    #      "X->",
    #      "X->TXT"],
    #     "S"
    # )
    # print(grammar)
    # Chomsky.to_chomsky_normal_form(grammar)
    # grammar = GrammarTraits.rename(grammar)
    # print(grammar)
    # grammar = Grammar(
    #     "SAB",
    #     "ab",
    #     ["S->A", "S->AB", "A->a", "B->b", "A->AA"],
    #     "S"
    # )
    # print(grammar)
    # predict = CYK.parser(grammar)
    # print(predict("baaab"))
    n, s, p = map(int, input().split())
    nonterminals = input()
    terminals = input()
    rules = []
    for _ in range(p):
        rules.append(input())
    start = input()
    grammar = Grammar(nonterminals, terminals, rules, start)
    predict = CYK.parser(grammar)
    m = int(input())
    for _ in range(m):
        word = input()
        if predict(word):
            print("Yes")
        else:
            print("No")

if __name__ == '__main__':
    main()
