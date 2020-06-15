from gromark import *


with open('10000.txt') as f:
    WORDS = [l.strip() for l in f.readlines()]


def find_gromark_key(pattern, words=WORDS):
    possible_key = []

    for word in words:
        word = key_remove_dups(word)
        if len(word) != len(pattern):
            continue

        numerical_key = [sorted(word).index(w)+1 for w in word]
        if numerical_key == pattern:
            possible_key.append(word)

    return possible_key
