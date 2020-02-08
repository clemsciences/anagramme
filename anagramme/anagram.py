
import itertools
from collections import defaultdict
from nltk.collections import Counter
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
    """
    >>> compute_anagrams_dictionary(["bonjour"])

    :param words:
    :return:
    """
    anagrams = defaultdict(set)
    for word in words:
        key = ''.join(sorted(word))
        anagrams[key].add(word)
    return anagrams


def find_word_anagrams(word: str, anagram_dictionary: Dict[str, Set[str]]):
    """
    >>> d = compute_anagrams_dictionary(["bonjour"])
    >>> find_word_anagrams("bjnroou", d)

    :param word:
    :param anagram_dictionary:
    :return:
    """
    key = "".join(sorted(word))
    anagrams = anagram_dictionary[key]
    return [anagram for anagram in anagrams if word != anagram]


def is_valid_subanagram(hashed_sentence, word):
    count_hashed_sentence = Counter(hashed_sentence)
    count_word = Counter(hashed_sentence)
    return all([c in hashed_sentence and count_word[c] <= count_hashed_sentence[c] for c in set(word)])


def find_sentence_anagrams(sentence: str, anagram_dictionary: list, temp=None):
    """
    >>> d = ["Je", "suis", "Voldemort", "Tom", "Jedusor", "Harry", "Potter", "Hermione", "Granger", "Ron", "Weasley"]
    >>> find_sentence_anagrams("Tom Elvis Jedusor".lower(), [i.lower() for i in d])
    ['je', 'suis', 'voldemort']

    >>> d.extend(["ja", "sais"])
    >>> find_sentence_anagrams("Tom Elvis Jedasor".lower(), [i.lower() for i in d])
    ['je', 'sais', 'voldemort']

    :param sentence:
    :param anagram_dictionary:
    :param temp:
    :return: sorted result or None
    """
    if len(sentence) == 0:
        return sorted(temp)
    if temp is None:
        temp = set()
    key = "".join(sorted(sentence.replace(" ", "").lower()))
    for word in anagram_dictionary:
        if is_valid_subanagram(key, word.lower()):
            temp.add(word)
            anagram_dictionary.remove(word)
            sentence = "".join(Counter(key) - Counter(word))
            res = find_sentence_anagrams(sentence, anagram_dictionary, temp)
            if res is not None:
                return res
    return None
