# Problem Set 4A
# Name: Octavio Vega
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    n = len(sequence)
    
    # base case: unit length sequences have only one permutation
    if n == 1:
        return [sequence] # only one possible permutation of a single element
    
    # recursive step: get all unique permutations of length n-1 sequence and shift first character around
    else:
        # create a list from the set so as to avoid storing duplicate permutations
        return [*set([s[:i] + sequence[0] + s[i:] for i in range(n) for s in get_permutations(sequence[1:])])]
        
if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    # case 1: 'abc'
    example_input_1 = 'abc'
    expected_output_1 = ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    actual_output_1 = get_permutations(example_input_1)
    if sorted(expected_output_1) == sorted(actual_output_1): # use sorted() since order is arbitrary
        print("Test case 1 PASSED")
    else:
        print(f"Test case 1 FAILED: expected {expected_output_1} but received {actual_output_1}")
    
    # case 2: 'odd'
    example_input_2 = 'odd'
    expected_output_2 = ['odd', 'dod', 'ddo']
    actual_output_2 = get_permutations(example_input_2)
    if sorted(expected_output_2) == sorted(actual_output_2):
        print("Test case 2 PASSED")
    else:
        print(f"Test case 2 FAILED: expected {expected_output_2} but received {actual_output_2}")
        
    # case 3: 'xy'
    example_input_3 = 'xy'
    expected_output_3 = ['xy', 'yx']
    actual_output_3 = get_permutations(example_input_3)
    if sorted(expected_output_3) == sorted(actual_output_3):
        print("Test Case 3 PASSED")
    else:
        print(f"Test Case 3 FAILED: expected {expected_output_3} but received {actual_output_3}")
    

