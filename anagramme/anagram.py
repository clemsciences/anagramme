
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


def find_anagrams(word: str, anagram_dictionary: Dict[str, Set[str]]):
    """
    >>> d = compute_anagrams_dictionary(["bonjour"])
    >>> find_anagrams("bjnroou", d)

    :param word:
    :param anagram_dictionary:
    :return:
    """
    key = "".join(sorted(word))
    anagrams = anagram_dictionary[key]
    return [anagram for anagram in anagrams if word != anagram]


# region
def sortstring(sentence):
    """
    >>> sortstring("bonjour oui non")
    '  bijnnnooooruu'
    """
    return ''.join(sorted(sentence))


def simplify(sentences):
    """
    >>> simplify(["bonjour oui non", "bonsoir oui"])
    defaultdict(<class 'list'>, {'bijnnnooooruu': ['bonjour oui non'], 'biinooorsu': ['bonsoir oui']})

    """
    possible_strings = defaultdict(list)
    for string in sentences:
        possible_strings[sortstring(string).strip()].append(string)
    return possible_strings


def countletters(string):
    """
    >>> countletters("bonjour oui non")
    {'a': 0, 'b': 1, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 1, 'j': 1, 'k': 0, 'l': 0, 'm': 0, 'n': 3, 'o': 4, 'p': 0, 'q': 0, 'r': 1, 's': 0, 't': 0, 'u': 2, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
    """

    result = {}
    for i in "abcdefghijklmnopqrstuvwxyz":
        result[i] = string.count(i)
    return result


def countstring(string):
    """
    >>> countstring("bonjour oui non")
    13
    """

    a = countletters(string)
    return sum(a.values())


def analyse(database, sentence):
    """
    >>> analyse(["bonjour", "oui", "non"], "bonjour oui non")

    """
    cletters = countstring(sentence)
    strings = simplify(generate(database, cletters, "abcdefghijklmnopqrstuvwxyz"))
    data = list()
    sorted_string = sortstring(sentence).strip()
    if sorted_string in strings.keys():
        data = strings[sorted_string]
    return len(strings.values()), data


def generate(database, length, letters, curstring="", curdata=None):
    """

    # >>> generate(["bonjour oui non", 13, "abcdefghijklmnopqrstuvwxyz"])

    """
    if curdata is None:
        curdata = set()
    if len(curstring.replace(" ", "")) > length:
        return set()
    if len(curstring.replace(" ", "")) == length:
        return curdata.union({curstring})
    t = countletters(curstring)
    for i in "abcdefghijklmnopqrstuvwxyz":
        if t[i] > letters[i]:
            return set()
    for i in database:
        t = countletters(curstring+i)
        test = 0
        for j in "abcdefghijklmnopqrstuvwxyz":
            if t[j] > letters[j]:
                test = 1
        if test:
            continue
        if sum(t.values()) <= length:
            curdata = curdata.union(generate(database.difference({i}), length, letters, curstring + " " + i, curdata))
            database = database.difference({i})
    return curdata
# endregion
