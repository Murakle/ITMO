class ngramm:
    def __init__(self, words):
        self.words = words

    def __eq__(self, other):
        if (len(self.words) != len(other.words)):
            return False
        for i in range(len(self.words)):
            if (self.words[i] != other.words[i]):
                return False
        return True

    def __hash__(self):
        if (len(self.words) == 1):
            return hash((self.words[0]))
        if (len(self.words) == 2):
            return hash((self.words[0], self.words[1]))
        else:
            return hash((self.words[0], self.words[1], self.words[2]))
