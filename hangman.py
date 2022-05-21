"""
Lucas Jensen
CS372
EC portion of Portfolio Project
"""

import random
from assets import gallows, words


class Hangman:
    def __init__(self):
        self._guessed_letters = set()
        self._board_index = 0
        self._word = random.choice(words)
        self._status = 'playing'

    def get_status(self):
        return self._status

    def get_board(self) -> object:
        word_status = ['_' for _ in self._word]
        for i in range(len(word_status)):
            if self._word[i] in self._guessed_letters:
                word_status[i] = self._word[i]

        guess = ''.join(word_status)

        msg = f"{gallows[self._board_index]}\n" \
              f"WORD: {guess}\n" \
              f"GUESSES: {self._guessed_letters}\n"

        if guess == self._word:
            self._status = 'You won!'
            msg += self._status
            msg += "\nEnter 'chat' to return to chatting"
        elif self._board_index == len(gallows) - 1:
            self._status = 'You lost!'
            msg += f"{self._status} The word was: {self._word}"
            msg += "\nEnter 'chat' to return to chatting"

        return msg

    def make_guess(self, letter: str):
        if len(letter) != 1:
            return False

        letter = letter.lower()
        self._guessed_letters.add(letter)
        if letter not in self._word:
            self.advance_hanging()

        return True

    def advance_hanging(self):
        self._board_index += 1

