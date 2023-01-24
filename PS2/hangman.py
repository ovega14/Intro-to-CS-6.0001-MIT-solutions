# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_letters = set([char for char in secret_word])
    return (secret_letters.issubset(set(letters_guessed)))



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    partial_word = secret_word
    for char in partial_word:
        if char not in letters_guessed:
            partial_word = partial_word.replace(char, '_ ')
        else:
            pass
    return partial_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = string.ascii_lowercase
    for letter in available_letters:
        if letter in letters_guessed:
            available_letters = available_letters.replace(letter, "")
        else:
            pass
    return available_letters

    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    play = True
    while play:
        guesses_left = 6
        letters_guessed = []
        warnings = 3
        score = 0
        victory = False
        print("Welcome to the game Hangman!")
        print(f"I am thinking of a word that is {len(secret_word)} letters long.")
        print("-------------")
        
        # allow player to keep guessing until they run out of guesses
        while guesses_left > 0 and not victory:
            print(f"You have {guesses_left} guesses left.")
            print("Available letters:", get_available_letters(letters_guessed))
            guess = input("Please guess a letter: ").lower()
            while guess in letters_guessed:
                # penalize player for guessing same character more than once
                warnings -= 1
                if warnings < 0:
                    guesses_left -= 1
                    print(f"Oops! You've already guessed that letter. You have no warnings left.")
                    print('so you lose one guess:', get_guessed_word(secret_word, letters_guessed))
                else:
                     print(f"Oops! You've already guessed that letter. You have {warnings} warnings left: ")
                     print(get_guessed_word(secret_word, letters_guessed))
                break
            if guess not in string.ascii_lowercase:
                # penalize player for guessing invalid character
                warnings -= 1
                if warnings < 0:
                    guesses_left -= 1
                    print(f"Oops! That is not a valid letter. You have no warnings left.")
                    print('so you lose one guess:', get_guessed_word(secret_word, letters_guessed))
                else:
                    print(f"Oops! That is not a valid letter. You have {warnings} warnings left: ")
                    print(get_guessed_word(secret_word, letters_guessed))
            elif guess in secret_word:
                letters_guessed.append(guess)
                print('Good guess:', get_guessed_word(secret_word, letters_guessed))
                # check for victory
                if is_word_guessed(secret_word, letters_guessed):
                    secret_letters = set([char for char in secret_word])
                    score += guesses_left*len(secret_letters)
                    print(f"Congratulations, you won!\nYour total score for this game is: {score}")
                    victory = True
                    break
            else:
                letters_guessed.append(guess)
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
                if guess in ['a', 'e', 'i', 'o', 'u']:
                    # lose 2 guesses for incorrect vowels
                    guesses_left -= 2
                else:
                    # lose 1 guess for incorrect consonant
                    guesses_left -= 1
        print("------------")
        
        # loss when all guesses depleted
        if victory:
            pass
        else:
            print("Sorry, you lose! You're out of guesses.")
        
        # prompt player to play again
        play_again = 0
        while play_again not in ['Y', 'N', 'y', 'n']:
            print("Please type either Y or N")
            play_again = input("Play again? [Y/N] ")
        if play_again.upper() == 'Y':
            play = True
        elif play_again.upper() == 'N':
            play = False
        print("------------")

    
#hangman('apple')

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
