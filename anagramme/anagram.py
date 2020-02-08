
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
    defaultdict(<class 'set'>, {'bjnooru': {'bonjour'}})

    >>> compute_anagrams_dictionary(["bonjour ca va", "coucou", "oui", "non", "oui non"])
    defaultdict(<class 'set'>, {'aabcjnooruv': {'bonjour ca va'}, 'ccoouu': {'coucou'}, 'iou': {'oui'}, 'nno': {'non'}, 'innoou': {'oui non'}})

    :param words:
    :return:
    """
    anagrams = defaultdict(set)
    for word in words:
        key = clean_and_sort_string(word)
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
    """
    >>> is_valid_subanagram(Counter("jesuisvoldemort"), Counter("voldemort"))
    True

    >>> is_valid_subanagram(Counter("jesuisvoldemort"), Counter("tromodlov"))
    False

    :param hashed_sentence:
    :param word:
    :return:
    """
    count_hashed_sentence = Counter(hashed_sentence)
    count_word = Counter(word)
    for c in set(word):
        if c not in hashed_sentence or count_word[c] > count_hashed_sentence[c]:
            return False
    return True


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
            res.update(find_sentence_anagrams2(sentence, anagram_dictionary, temp, res))
    return res


# region
# https://stackoverflow.com/questions/34220147/efficient-way-to-find-anagrams-of-sentences-from-dictionary/34224914
def clean_and_sort_string(sentence: str):
    """
    >>> clean_and_sort_string("bonjour oui non")
    'bijnnnooooruu'
    """
    return ''.join(sorted(sentence)).strip()


def count_letters(string: str):
    """
    >>> count_letters("bonjour oui non")
    Counter({'o': 4, 'n': 3, 'u': 2, ' ': 2, 'b': 1, 'j': 1, 'r': 1, 'i': 1})
    """
    return Counter(string.replace(" ", ""))


def count_string(string):
    """
    >>> count_string("bonjour oui non")
    13
    """
    return len("".join(count_letters(string).elements()))


def generate(database, length, letters, curstring="", curdata=None):
    """
    >>> anagram_to_find = "njrboou"
    >>> generate({"bonjour", "oui", "non"}, count_string(anagram_to_find), count_letters(anagram_to_find))
    {'bonjour'}

    >>> anagram_to_find = "Tom Elvis Jedusor".lower()
    >>> result = generate({"Harry", "Hermione", "Ron", "je", "suis", "voldomert", "voldemort"}, count_string(anagram_to_find), count_letters(anagram_to_find))
    >>> sorted([ " ".join(sorted(i.split(" "))) for i in result])
    ['je suis voldemort', 'je suis voldomert']

    """
    if curdata is None:
        curdata = set()
    if len(curstring.replace(" ", "")) > length:
        return set()
    if len(curstring.replace(" ", "")) == length:
        return curdata.union({curstring})
    t = count_letters(curstring)
    for i in ascii_lowercase:
        if t[i] > letters[i]:
            return set()
    for i in database:
        t = count_letters(curstring + i)
        if is_valid_subanagram(letters, t) and sum(t.values()) <= length:
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
    {'bonjour'}

    >>> d = ["Je", "suis", "sius", "Voldemort", "Veldomort", "Tom", "Jedusor", "Harry", "Hermione", "Ron"]
    >>> result = find_sentence_anagrams({i.lower() for i in d}, "Tom Elvis Jedusor".lower())

    >>> sorted([" ".join(sorted(i.split(" "))) for i in result])
    ['je sius veldomort', 'je sius voldemort', 'je suis veldomort', 'je suis voldemort']

    :param database: list of tokens
    :param sentence: sentence that you want to find anagrams from
    :return: list of sentences which are anagrams of the given sentence
    """
    cletters = count_string(sentence)
    letters = count_letters(sentence)
    strings = compute_anagrams_dictionary(generate(database, cletters, letters))
    data = []
    sorted_string = clean_and_sort_string(sentence)
    if sorted_string in strings.keys():
        data = strings[sorted_string]
    return data
# endregion
