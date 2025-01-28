class AssembleError(Exception):
    def __init__(self, char: str, rule: str):
        self.char = char
        self.rule = rule

    def __str__(self):
        return f"Cannot assemble \"{self.char}\" in rule \"{self.rule}\""

class RuleError(Exception):
    def __init__(self, rule: str):
        self.rule = rule

    def __str__(self):
        return f"Incorrect rule \"{self.rule}\""

class TerminalError(Exception):
    def __init__(self, char: str, rule: str):
        self.char = char
        self.rule = rule

    def __str__(self):
        return f"\"{self.char}\" in rule \"{self.rule}\": A rule must start with nonterminal"

class StartError(Exception):
    def __init__(self, rule: str):
        self.rule = rule

    def __str__(self):
        return f"\"{self.rule}\": not nonterminal cannot be the start"