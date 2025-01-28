class Wrapper:
    def __init__(self, string: str):
        self.string = string

    def __getitem__(self, i: int):
        return self.string[i]

    def image(self, bijection: dict):
        return Wrapper("".join([bijection[i] if i in bijection else i for i in self.string]))

    def __str__(self):
        return self.string

    def __len__(self):
        return len(self.string)

    def __eq__(self, other):
        return self.string == other.string