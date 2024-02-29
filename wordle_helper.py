'''
Author: Joseph Boen 

Helps quickly filter wordle words 
Useful for people who can't remember all the 5-letter words
'''

import argparse

def load_words(fp: str) -> set:
    '''
    Loads list of all english words that contain only letters
    
    Params:
        fp: file path to wordle word list
    '''
    
    with open(fp) as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def check_words(all_words: set, gray: set, green: dict, yellow: dict) -> set:
    '''
    Filters list of words to see which match wordle conditions
    
    Params:
        all_words: words to check
        gray: letters to exclude
        green: letters to include with correct positions
        yellow: letters to include with incorrect positions
    
    Returns: 
        set of valid words
    '''

    valid_words = set()
    for word in all_words:

        letters = set(word)

        #checks if gray letters are NOT in current word
        gray_check = True
        if len(gray.intersection(letters)) != 0:
            gray_check = False

        #checks if yellow letters are in word, but NOT in current position
        yellow_check = True
        for pos, char in yellow.items():  
            if word[pos] == char or char not in letters:
                yellow_check = False

        #checks if green letters are in word AT current position
        green_check = True
        for pos, char in green.items():
            if word[pos] != char:
                green_check = False

        #checks that all conditions are met
        if gray_check and yellow_check and green_check:
            valid_words.add(word)
            
    return valid_words

def parse_board(board: list):
    '''
    Parses wordle board
    
    Note: Gray -> X, Yellow -> Y, Green -> G
    
    Example:
        first guess: "adieu" yields "gray, yellow, gray, gray, yellow"
        second guess: "bound" yields "gray, green, green, green, green"
        
        this can be inputted as in ["adieu", "XYXXY","bound", "XGGGG"]
    
    Param:
        board: list of tuples containing guesses and outputs
        
    Returns:
        conditions: dictionary of conditions
    
    '''
    
    assert len(board)%2 == 0, ("unequal number of guesses and outputs!")
    
    reshaped_board = [(board[i], board[i + 1]) for i in range(0, len(board), 2)]

    conditions = {"gray": set(), 
                  "green": {}, 
                  "yellow": {}}
    
    for guess, output in reshaped_board:
        assert len(guess) == len(output), ("guess and output are different lengths!")
        assert set(output).issubset(set("XYG")), ("outputs must be X,Y, or G!")

        for idx, (letter, color) in enumerate(zip(guess, output)):
            if color == "X":
                conditions["gray"].add(letter)

            if color == "Y":
                conditions["yellow"][idx] = letter

            if color == "G":
                conditions["green"][idx] = letter
                
    return conditions

def execute_wordle_help(word_fp, board):
    '''
    Reads board and filters words
    
    Params:
        word_fp: word file path
        board: board list
        
    Returns:
        filtered words
    '''
    
    all_words = load_words(word_fp)
    
    conditions = parse_board(board)
    
    valid_words = check_words(all_words, 
                              gray = conditions['gray'],          
                              green = conditions['green'],      
                              yellow = conditions['yellow'])
    
    print("{} valid words found!".format(len(valid_words)))
   
    for word in valid_words:
        print(word)
    
if __name__ == "__main__":

    help_message = (
    '''
    
    A wordle board is a sequence of guesses and outputs. 
    
    Example:
    
    first guess: "adieu" yields "gray, yellow, gray, gray, yellow"
    second guess: "bound" yields "gray, green, green, green, green"

    board = "adieu" "XYXXY" "bound" "XGGGG"
        
    Note: Gray -> X, Yellow -> Y, Green -> G 
    
    '''
    )
                   
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-board", help = help_message, type = str, nargs = "*")
    parser.add_argument("--words_file", help = "list of words", default = "wordle-La.txt", type = str)
    
    args = parser.parse_args()
        
    execute_wordle_help(args.words_file, args.board)



