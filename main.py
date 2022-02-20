"""
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

Scoring Function:
    word score: sum of (percent of words from bank with letter in same position as guess) for each letter

    bias: percentage of the word that is unique vowels, used if we do not know a vowel yet
          weighted against words with duplicate letters

"""
import string

WORDLEN = 5
GUESSES = 6

#parse all words of the correct length into list
fname = 'wordlist.txt'
with open(fname) as file:
    wordbank = [line.strip() for line in file if len(line.strip())==WORDLEN]
# print(str(len(wordbank)) + " words read into wordbank")

#set represents all current possible letters for that position, pattern is same length as WORDLEN
pattern = [set(string.ascii_lowercase) for x in range(WORDLEN)]
yellowLetters = set()

def print_pattern():
    for x in pattern:
        print(x)


#update pattern with feedback of guess
def new_feedback(guess, feedback):
    assert ((len(guess) == WORDLEN) and (len(feedback) == WORDLEN))
    for i in range(WORDLEN):
        if feedback[i]=='b':
            for x in pattern:
                if(len(x)>1):
                    x.discard(guess[i])
        elif feedback[i]=='y':
            yellowLetters.add(guess[i])
            pattern[i].discard(guess[i])
        elif feedback[i]=='g':
            pattern[i] = {guess[i]}
    # print("Pattern after "+guess+": ")
    # print_pattern()
    # print()

#check if a word satisfies pattern (filter)
def check_guess(word):
    assert (len(word) == WORDLEN)
    for x in yellowLetters:
        if(x not in set(word)):
            return False
    for i in range(WORDLEN):
        if word[i] not in pattern[i]:
            return False
    return True

#calculates score by checking how many words share the letter in each position of the target
#weighted towards words with more unique characters
#possibly add a bias towards unique vowels if no vowels have been found
def score_word(word):
    assert(len(word)==WORDLEN)
    score = 0.0
    for y in wordbank:
        for p in range(WORDLEN):
            if y[p]==word[p]:
                score+=1/len(wordbank)
    score *= len(set(word))/5
    return score

#return max score word that matches pattern
def suggest_guess():
    curMaxScore = 0
    curBestGuess = "1z1z1"
    for y in wordbank:
        if(check_guess(y)):
            print(y+": "+str(score_word(y)))
            if(score_word(y)>curMaxScore):
                curMaxScore = score_word(y)
                curBestGuess = y
    return (curBestGuess)


#PLAY A GAME
def playWordle():
    print("Welcome to Wordle Solver!")
    curGuess = "salet"
    actualGuess = ""
    for i in range(1, GUESSES):
        print("\n"+"Best Guess: " + curGuess)
        actualGuess = input("Enter the word you guessed: ")
        feedback = input("Enter the color of each tile (b, y, or g): ")
        if (feedback == "ggggg"):
            print("Wordle Completed!")
            return
        print("Possible Words (with score): ")
        new_feedback(actualGuess, feedback)
        curGuess = suggest_guess()
        if (i == GUESSES-1):
            print("Best Guess: " + curGuess)
    print("Out of attempts. Sorry!")

playWordle()

