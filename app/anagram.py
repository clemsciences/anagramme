
import itertools
from collections import defaultdict
from typing import List, Dict, Set

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def find_possible(word: str):
    """
    From https://github.com/patrickleweryharris/anagram-solver/blob/master/anagram_solver/anagram_solver.py
    Return all possible combinations of letters in word
    @type word: [str]
    @rtype: [str]
    """
    possible_words = []

    for i in range(0, len(word) + 1):
        for subset in itertools.permutations(word, i):
            possible = ''
            for letter in subset:
                possible += letter
            if len(possible) == len(word):
                # itertools.permutations returns smaller lists
                possible_words.append(possible)

    return possible_words


def compute_anagrams_dictionary(words: List[str]) -> Dict[str, Set[str]]:
    anagrams = defaultdict(set)
    for word in words:
        key = ''.join(sorted(word))
        anagrams[key].add(word)
    return anagrams


def find_anagrams(word: str, anagram_dictionary: Dict[str, Set[str]]):
    key = "".join(sorted(word))
    anagrams = anagram_dictionary[key]
    return [anagram for anagram in anagrams if word != anagram]
