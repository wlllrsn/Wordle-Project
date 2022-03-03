# Classes to receive input
# Will eventually create an algorithm to simulate guesses


class InputListener:

    def __init__(self, wordlist):
        self.wordlist = wordlist

    def getinput(self) -> str:
        return "string"


class UserListener(InputListener):

    def getinput(self) -> str:
        while True:
            guess = input("Please input a word: ")
            if guess in self.wordlist:
                return guess
            elif guess == 'quit' or guess == 'exit':
                return 'q'


class AutomatedListener(InputListener):
    # TODO create algorithm to solve games

    def getinput(self) -> str:
        return input("Please input a word: ")
