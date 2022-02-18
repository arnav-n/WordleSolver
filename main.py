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
print(str(len(wordbank)) + " words read into wordbank")

#set represents all current possible letters for that position, pattern is same length as WORDLEN
pattern = [set(string.ascii_lowercase) for x in range(WORDLEN)]

def print_pattern():
    for x in pattern:
        print(x)


#update pattern with feedback of guess
def new_feedback(feedback, guess):
    assert ((len(guess) == WORDLEN) and (len(feedback) == WORDLEN))
    for i in range(WORDLEN):
        if feedback[i]=='b':
            for x in pattern:
                x.discard(guess[i])
        elif feedback[i]=='y':
            pattern[i].discard(guess[i])
        elif feedback[i]=='g':
            pattern[i] = {guess[i]}

#check if a word satisfies pattern
def check_guess(word):
    assert (len(word) == WORDLEN)
    for i in range(WORDLEN):
        if word[i] not in pattern[i]:
            return False
    return True

#calculates score by checking how many words share the letter in each position of the target
#possibly add a bias towards unique vowels if no vowels have been found
def score_word(word):
    assert(len(word)==WORDLEN)
    score = 0.0
    for p in range(WORDLEN):
        for y in wordbank:
            if y[p]==word[p]:
                score+=1/len(wordbank)
    return score

def suggest_guess():
    curMaxScore = 0
    curBestGuess = "1z1z1"
    for y in wordbank:
        # print(check_guess(y))
        if(check_guess(y)):
            # if(score_word(y)>curMaxScore):
            #     curMaxScore = score_word(y)
            #     curBestGuess = y
            print(y)
    return curBestGuess

#
new_feedback("bbbbg", "crane")
new_feedback("byybb", "peons")
new_feedback("bgbyy","toled")
new_feedback("bgbbg", "noise")
new_feedback("ggbbg", "douse")
# print_pattern()

print(suggest_guess())
#TO DO
#   should I fix yellow logic as follows?: guesses MUST contain all yellow and green letters
#   implement a loop that does the following:
#       find word with max score that matches pattern
#       suggest word
#       accept feedback from user
#       update pattern accordingly and find the new top word
#       repeat until feedback is all green

