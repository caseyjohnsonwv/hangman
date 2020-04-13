from random import choice as randomChoice
from string import ascii_uppercase as validLetters

class HangmanError(Exception): pass
class LetterAlreadyGuessedError(HangmanError): pass
class InvalidGuessError(HangmanError): pass

class HangmanGame:
    def __init__(self, language):
        self.language = language.lower().strip()
        with open("./dictionaries/{}.txt".format(language)) as f:
            wordList = f.readlines()
        self.answer = randomChoice(wordList).upper().strip()
        self.blanks = ''.join(["_ "]*len(self.answer)).strip()
        self.guesses = set()
        self.wrong = frozenset(list(validLetters)).difference(list(self.answer))

    def to_json():
        """Used to serialize data in the browser session between requests"""
        pass

    def from_json():
        """Used to deserialize data from the browser session after a request"""
        pass

    def _sanitize_guess_(self, letter):
        letter = letter.upper().strip()
        if len(letter) != 1:
            raise InvalidGuessError()
        elif letter in self.guesses:
            raise LetterAlreadyGuessedError()
        else:
            self.guesses.add(letter)
        return letter

    def guess(self, letter):
        letter = self._sanitize_guess_(letter)
        # check guess
        if letter in self.wrong:
            return False
        # update game data
        for i in range(len(self.answer)):
            if self.answer[i] == letter:
                # strings are immutable - use a list, I guess :/
                blanks_temp = list(self.blanks)
                blanks_temp[i*2] = letter
                self.blanks = ''.join(blanks_temp)
        return True
