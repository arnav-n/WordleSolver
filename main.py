"""
Ideas:
    https://towardsdatascience.com/wordle-solver-using-python-3-3c3bccd3b4fb
    https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python

Wordle assistant:
    It will suggest the most optimal word, then the user
    gives feedback in the form of 'bbygb', describing the
    color of each of the five tiles: black, yellow, or
    green. The solver will take this feedback into account,
    then suggest the most optimal word that could match
    the given pattern. This will be repeated until the
    correct word is found, or all 6 guesses have been used.

Two Steps Required:
    Filtering: filter out words which do not match the pattern
    Scoring Function: some way of assigning a numerical value to a word
        independent scoring function allows for easy improvement/testing


Filtering:
    eliminate any word containing black letters
    eliminate any word without all yellow/green letters
    eliminate any word with yellow letters in the same spot
    eliminate any word without green letters in the expected spots

Possible Scoring Function:
    word score: sum of (percent of words from bank with letter in same position as guess) for each letter

    bias: percentage of the word that is unique vowels, used if we do not know a vowel yet

"""
import string

WORDLEN = 5
GUESSES = 6

#parse all words of the correct length into list
fname = 'wordlist.txt'
with open(fname) as file:
    wordbank = [line.strip() for line in file if len(line.strip())==WORDLEN]
print(len(wordbank))

#set represents all current possible letters for that position, pattern is same length as WORDLEN
pattern = [set(string.ascii_lowercase) for x in range(WORDLEN)]

#update pattern with feedback of guess
def newFeedback(feedback, guess):
    for i in range(WORDLEN):
        if(feedback[i]=='b'):
            for x in pattern:
                x.remove(guess[i])
        elif(feedback[i]=='y'):
            pattern[i].remove(guess[i])
        elif(feedback[i]=='g'):
            pattern[i] = {guess[i]}

#check if a word satisfies pattern
def checkGuess(word):
    for i in range(WORDLEN):
        if(word[i] not in pattern[i]):
            return False
    return True



#TO DO
#   implement scoreWord(word) function
#   implement a loop that does the following:

#       find word with max score that matches pattern
#       suggest word
#       accept feedback from user
#       update pattern accordingly and find the new top word
#       repeat until feedback is all green

