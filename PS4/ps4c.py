# Problem Set 4C
# Name: Octavio Vega
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words('words.txt')
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        # initialize a dict to store the map
        map_dict = {}
        
        # consonants stay the same
        for i in range(21):
            map_dict[CONSONANTS_LOWER[i]] = CONSONANTS_LOWER[i]
            map_dict[CONSONANTS_UPPER[i]] = CONSONANTS_UPPER[i]
            
        # record the mapping for vowels
        for i in range(5):
            map_dict[VOWELS_LOWER[i]] = vowels_permutation[i]
            map_dict[VOWELS_UPPER[i]] = vowels_permutation[i].upper()
        
        return map_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        # get the input message
        input_message = self.get_message_text()
        
        # initialize empty message to write new message
        new_message = ''
        
        # iterate over input message and translate
        for char in input_message:
            new_message += transpose_dict.get(char, char)
        
        return new_message
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        # get the list of possible permutations of vowels
        vowel_permutations = get_permutations(VOWELS_LOWER) #5! = 120 options
        
        # initialize a dict to store the number of valid words per permutation
        valid_word_counts = {}
    
        # iterate over possible permutations and count valid words in translated message
        for perm in vowel_permutations:
            valid_word_counts[perm] = 0 
            
            # build a transpose dictionary for the perm and translate
            transpose_dict = self.build_transpose_dict(perm)
            new_message = self.apply_transpose(transpose_dict)
            
            # split into words and count
            new_words = new_message.split()
            for word in new_words:
                if is_word(self.get_valid_words(), word):
                    valid_word_counts[perm] += 1
            
        # find the permutation that results in the most English words
        counts = list(valid_word_counts.values())
        
        # if no good permutations, return original message
        if max(counts) == 0:
            best_message = self.get_message_text()
        else:
            best_perm = vowel_permutations[counts.index(max(counts))]
            best_message = self.apply_transpose(self.build_transpose_dict(best_perm))
        
        return best_message
    

if __name__ == '__main__':
     
    #Test Case 1 (SubMessage)
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    expected_encryption = "Hallu Wurld!"
    actual_encryption = message.apply_transpose(enc_dict)
    if expected_encryption == actual_encryption:
        print("SubMessage Test Case 1 Passed")
    else:
        print("SubMessage Test Case 1 Failed")
        print(f"Expected {expected_encryption} but got {actual_encryption}")
        
    #Test Case 2 (SubMessage)
    message = SubMessage("I am a student in 6.0001.")
    permutation = "uoiea"
    enc_dict = message.build_transpose_dict(permutation)
    expected_encryption = "I um u stadont in 6.0001."
    actual_encryption = message.apply_transpose(enc_dict)
    if expected_encryption == actual_encryption:
        print("SubMessage Test Case 2 Passed")
    else:
        print("SubMessage Test Case 2 Failed")
        print(f"Expected {expected_encryption} but got {actual_encryption}")
      
    #Test Case 1 (EncryptedSubMessage)
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    expected_decryption = "Hello World!"
    actual_decryption = enc_message.decrypt_message()
    if expected_decryption == actual_decryption:
        print("EncryptedSubMessage Test Case 1 Passed")
    else:
        print("EncryptedSubMessage Test Case 1 FAILED")
        print(f"Expected {expected_decryption} but got {actual_decryption}")        
        
    #Test Case 2 (EncryptedSubMessage)
    message = SubMessage("I am a student in 6.0001.")
    permutation = "uoiea"
    enc_dict = message.build_transpose_dict(permutation)
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    expected_decryption = "I am a student in 6.0001."
    actual_decryption = enc_message.decrypt_message()
    if expected_decryption == actual_decryption:
        print("EncryptedSubMessage Test Case 2 Passed")
    else:
        print("EncryptedSubMessage Test Case 2 FAILED")
        print(f"Expected {expected_decryption} but got {actual_decryption}") 