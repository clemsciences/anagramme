
import itertools
from collections import defaultdict
from nltk.collections import Counter
from typing import List, Dict, Set

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


ascii_lowercase = "abcdefghijklmnopqrstuvwxyz"


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


def find_sentence_anagrams1(sentence: str, anagram_dictionary: list, temp=None):
    """
    >>> d = ["Je", "suis", "Voldemort", "Veldomort", "Tom", "Jedusor", "Harry", "Potter", "Hermione", "Granger", "Ron"]
    >>> find_sentence_anagrams1("Tom Elvis Jedusor".lower(), [i.lower() for i in d])
    ['je', 'suis', 'voldemort']

    >>> d.extend(["ja", "sais"])
    >>> find_sentence_anagrams1("Tom Elvis Jedasor".lower(), [i.lower() for i in d])
    ['je', 'sais', 'voldemort']

    :param sentence: we want to find anagrams of this sentence
    :param anagram_dictionary:
    :param temp:
    :return: the first result found or None
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
            res = find_sentence_anagrams1(sentence, anagram_dictionary, temp)
            if res is not None:
                return res
    return None


def find_sentence_anagrams2(sentence: str, anagram_dictionary: list, temp=None, res=None):
    """
    >>> d = ["Je", "suis", "Voldemort", "Veldomort", "Tom", "Jedusor", "Harry", "Potter", "Hermione", "Granger", "Ron"]
    >>> a = find_sentence_anagrams2("Tom Elvis Jedusor".lower(), [i.lower() for i in d])
    >>> a
    ['je', 'suis', 'voldemort']

    >>> d.extend(["ja", "sais"])
    >>> find_sentence_anagrams2("Tom Elvis Jedasor".lower(), [i.lower() for i in d])
    ['je', 'sais', 'voldemort']

    :param sentence: we want to find anagrams of this sentence
    :param anagram_dictionary:
    :param temp:
    :param res:
    :return: sorted result or None
    """
    # print(res)
    # print(temp
    # print(sentence)

    if temp is None:
        temp = ""
    if res is None:
        res = set()
    if len(sentence) == 0:
        # print(type(temp))
        return {temp}
    key = "".join(sorted(sentence.replace(" ", "").lower()))
    for word in anagram_dictionary:
        if is_valid_subanagram(key, word.lower()):
            if temp:
                temp = temp + " " + word
            else:
                temp = word
            anagram_dictionary.remove(word)
            sentence = "".join(Counter(key) - Counter(word))
            # res.add(temp)
            res.update(find_sentence_anagrams2(sentence, anagram_dictionary, temp, res))
    return res


def sort_string(sentence: str):
    """
    >>> sort_string("bonjour oui non")
    'bijnnnooooruu'
    """
    return ''.join(sorted(sentence)).strip()


def simplify(sentences: List[str]):
    """
    >>> simplify(["bonjour oui non", "bonsoir oui"])
    defaultdict(<class 'list'>, {'bijnnnooooruu': ['bonjour oui non'], 'biinooorsu': ['bonsoir oui']})

    """
    possible_strings = defaultdict(list)
    for string in sentences:
        possible_strings[sort_string(string)].append(string)
    return possible_strings


def countletters(string: str):
    """
    >>> countletters("bonjour oui non")
    {'a': 0, 'b': 1, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 1, 'j': 1, 'k': 0, 'l': 0, 'm': 0, 'n': 3, 'o': 4, 'p': 0, 'q': 0, 'r': 1, 's': 0, 't': 0, 'u': 2, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
    """

    result = {}
    for i in ascii_lowercase:
        result[i] = string.count(i)
    return result


def countstring(string):
    """
    >>> countstring("bonjour oui non")
    13
    """

    a = countletters(string)
    return sum(a.values())


def generate(database, length, letters, curstring="", curdata=None):
    """
    >>> anagram_to_find = "njrboou"
    >>> generate({"bonjour", "oui", "non"}, countstring(anagram_to_find), countletters(anagram_to_find))
    {'bonjour'}
    """
    if curdata is None:
        curdata = set()
    if len(curstring.replace(" ", "")) > length:
        return set()
    if len(curstring.replace(" ", "")) == length:
        return curdata.union({curstring})
    t = countletters(curstring)
    for i in ascii_lowercase:
        if t[i] > letters[i]:
            return set()
    for i in database:
        t = countletters(curstring+i)
        test = 0
        for j in ascii_lowercase:
            if t[j] > letters[j]:
                test = 1
        if test:
            continue
        if sum(t.values()) <= length:
            if curstring:
                curdata = curdata.union(generate(database.difference({i}),
                                                 length, letters, curstring + " " + i, curdata))
            else:
                curdata = curdata.union(generate(database.difference({i}), length, letters, i, curdata))
            database = database.difference({i})
    return curdata


def find_sentence_anagrams(database: set, sentence: str):
    """
    >>> find_sentence_anagrams({"bonjour", "oui", "non"}, "jourbon")
    (1, ['bonjour'])

    >>> d = ["Je", "suis", "sius", "Voldemort", "Veldomort", "Tom", "Jedusor", "Harry", "Potter", "Hermione", "Granger", "Ron"]
    >>> find_sentence_anagrams({i.lower() for i in d}, "Tom Elvis Jedusor".lower())

    :param database:
    :param sentence:
    :return:
    """
    cletters = countstring(sentence)
    letters = countletters(sentence)
    strings = simplify(generate(database, cletters, letters))
    data = list()
    sorted_string = sort_string(sentence).strip()
    if sorted_string in strings.keys():
        data = strings[sorted_string]
    return len(strings.values()), data
