
'''
Author: Joseph Boen

Desc: Command Line Interface spelling bee solver
'''


import argparse
from tqdm import tqdm


def load_words(fp: str = 'words_alpha.txt') -> set:
    '''
    Loads list of all english words that contain only letters
    '''
    
    with open(fp) as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def filter_words(all_words: set,  all_letters: set, required_letter: str) -> list:
    '''
    Filters words that satisfy set spelling bee rules
    '''

    valid_words = []
    for word in tqdm(all_words, total = len(all_words)):
        if set(word) <= all_letters and required_letter in word and len(word) > 3:
            valid_words.append(word)
        
    print("{} valid words found!".format(len(valid_words)))
        
    valid_words = sorted(valid_words, key = lambda x: len(x))[::-1]

    return valid_words

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-req", help = "required letter", type = str)
    parser.add_argument("-opt", help = "optional letters", type = str)
    parser.add_argument("--words_file", help = "list of words", default = "words_alpha.txt", type = str)
    
    args = parser.parse_args()

    all_words = load_words(args.words_file)

    all_letters = set(list(args.opt) + [args.req])
    valid_words = filter_words(all_words, all_letters, args.req)

    for word in valid_words:
        print(word)

    
