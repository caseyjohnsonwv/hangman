from random import choice as randomChoice
from string import ascii_uppercase as validLetters

class HangmanError(Exception): pass
class LetterAlreadyGuessedError(HangmanError): pass
class InvalidGuessError(HangmanError): pass

class HangmanGame:
    def __init__(self, language):
        self.language = language.lower().strip()
        with open("../dictionaries/{}.txt".format(self.language)) as f:
            wordList = f.readlines()
        self.answer = randomChoice(wordList).upper().strip()
        self.blanks = ''.join(["_ "]*len(self.answer)).strip()
        self.guesses = set()
        self.wrong = frozenset(list(validLetters)).difference(list(self.answer))

    def sanitize_guess(self, letter):
        letter = letter.upper().strip()
        if len(letter) != 1:
            raise InvalidGuessError()
        elif letter in self.guesses:
            raise LetterAlreadyGuessedError()
        return letter

    def guess(self, letter):
        letter = self.sanitize_guess(letter)
        self.guesses.add(letter)
        # check guess
        if letter in self.wrong:
            return False
        # update game data
        blanks_temp = list(self.blanks)
        for i in range(len(self.answer)):
            if self.answer[i] == letter:
                blanks_temp[i*2] = letter
        self.blanks = ''.join(blanks_temp)
        # return True if word is complete, False if not
        return self.blanks[::2] == self.answer

    def __from_json__(data):
        g = HangmanGame(data['language'])
        g.answer = data['answer']
        g.blanks = data['blanks']
        g.guesses = set(data['guesses'])
        g.wrong = set(data['wrong'])
        return g

    def from_json(data):
        """Used to deserialize data from the browser after a request"""
        return HangmanGame.__from_json__(data)

    def to_json(self):
        """Used to serialize data in the browser session between requests"""
        j = {}
        j['language'] = self.language
        j['answer'] = self.answer
        j['blanks'] = self.blanks
        j['guesses'] = list(self.guesses)
        j['wrong'] = list(self.wrong)
        return j
