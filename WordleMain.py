import InputListener as listener
from random import randint
from termcolor import colored, cprint
import colorama
import sys
import os
import dill


class Wordle:

    lifetime_games = 0
    lifetime_wins = 0
    lifetime_losses = 0

    total_games = 0
    wins = 0
    losses = 0

    def __init__(self, solutionlist: list, guesslist: list, automated: bool=False):

        if automated:
            self.listener = listener.AutomatedListener(guesslist)
        else:
            self.listener = listener.UserListener(guesslist)

        self.number_of_turns = 6
        self.current_turn = 1

        self.solutionlist = solutionlist
        self.WORD = self.selectWord(self.solutionlist)

        self.guesses = []

        self.greens = []
        self.yellows = []
        self.unused = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z']

        self.lifetime_games = 0
        self.lifetime_wins = 0
        self.lifetime_losses = 0
        self.longest_streak = 0

        self.total_games = 0
        self.wins = 0
        self.losses = 0
        self.streak = 0

    def selectWord(self, wordlist: list) -> str:
        return wordlist[randint(0, len(wordlist) - 1)]

    def checkCorrectness(self, word):
        # should take in a 5 letter string, and compare it to the WORD
        # returns the 5-character hint about the word
        returnstring = ""

        for i in range(5):
            letter = word[i]

            if letter == self.WORD[i]:
                returnstring += colored(letter, 'green')

                if letter in self.unused:
                    self.unused.remove(letter)

                if letter in self.yellows:
                    self.yellows.remove(letter)

                if letter not in self.greens:
                    self.greens.append(letter)

            elif letter in self.WORD:
                returnstring += colored(letter, 'yellow')

                if letter in self.unused:
                    self.unused.remove(letter)

                if letter not in self.greens and letter not in self.yellows:
                    self.yellows.append(letter)

            else:
                returnstring += colored(letter, 'white')

                if letter in self.unused:
                    self.unused.remove(letter)
        return returnstring

    def printLetters(self):
        print("Current Streak: " + str(self.streak))
        print("\n")
        print("\t+-------+")
        for line in self.guesses:
            print('\t| ' + ''.join(line) + ' |')
        for x in range(self.number_of_turns - len(self.guesses)):
            print('\t|       |')
        print("\t+-------+")

        print("\n")
        print("Correct letters: " + colored(' '.join(self.greens), 'green'))
        print(colored("Close letters: ", 'white') + colored(' '.join(self.yellows), 'yellow'))
        print(colored("Unused letters: ", 'white') + colored(' '.join(self.unused), 'white'))
        print("\n")

    def isCorrect(self, word):
        if word == self.WORD:
            return True
        else:
            return False

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        self.printLetters()

        while self.current_turn <= self.number_of_turns:

            guess = self.listener.getinput()
            if guess == 'q':
                return
            self.guesses.append(self.checkCorrectness(guess))

            os.system('cls' if os.name == 'nt' else 'clear')

            self.printLetters()

            if self.isCorrect(guess):
                print("You won!")
                print("You guessed the word in " + str(self.current_turn) + " guesses")
                self.total_games += 1
                self.wins += 1
                self.lifetime_games += 1
                self.lifetime_wins += 1
                self.streak += 1
                if self.streak > self.longest_streak:
                    self.longest_streak = self.streak
                return

            self.current_turn += 1

        print("You lost :(")
        print("The correct word was: " + self.WORD)
        self.total_games += 1
        self.losses += 1
        self.lifetime_games += 1
        self.lifetime_losses += 1

    def newgame(self):
        self.current_turn = 1

        self.WORD = self.selectWord(self.solutionlist)

        self.guesses = []

        self.greens = []
        self.yellows = []
        self.unused = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z']

    def newsession(self):
        self.total_games = 0
        self.wins = 0
        self.losses = 0
        self.streak = 0


if __name__ == '__main__':
    colorama.init()

    cprint("\n\tWORDLE", 'green')

    # attempt to load past game
    # if successful, enter into gameplay loop
    # if fails, load data into new game and start fresh

    try:
        game = dill.load(open("savedata.p", "rb"))
        game.newsession()

    except:
        solutionlist = []
        guesslist = []

        with open("C:/Users/Will/Documents/WordleProject/solutions.txt", "r") as solutions:
            for word in solutions:
                solutionlist.append(word.strip())
                guesslist.append(word.strip())

        with open("C:/Users/Will/Documents/WordleProject/guesses.txt", "r") as guesses:
            for word in guesses:
                guesslist.append(word.strip())

        game = Wordle(solutionlist, guesslist, False)

    print("\nLifetime games played: " + str(game.lifetime_games))
    print("Lifetime wins: " + str(game.lifetime_wins))
    print("Lifetime losses: " + str(game.lifetime_losses))
    print("Longest streak: " + str(game.longest_streak))

    a = input("\nPress Enter to Continue...")

    while True:

        game.newgame()
        game.run()

        answer = input("Play again? ")
        if answer.lower() in ["y", "yes"]:
            continue
        else:
            dill.dump(game, open("savedata.p", "wb"))
            break

    print("\n- - - - - - - Session Ended - - - - - - -")
    print("Games played: " + str(game.total_games))
    print("Total wins: " + str(game.wins))
    print("Total losses: " + str(game.losses))

    print("\n- - - - - - - Lifetime Stats - - - - - - -")
    print("Lifetime games played: " + str(game.lifetime_games))
    print("Lifetime wins: " + str(game.lifetime_wins))
    print("Lifetime losses: " + str(game.lifetime_losses))
    print("Longest streak: " + str(game.longest_streak) + "\n")
