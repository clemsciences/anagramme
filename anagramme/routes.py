"""

"""

from flask import jsonify, request

from . import anagramme

from anagramme.resource_manager import tokenize, AVAILABLE_LIBRARIES, load_latin_proper_nouns, load_latin_library
from anagramme.anagram import find_possible, compute_anagrams_dictionary, find_word_anagrams, find_sentence_anagrams


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


@anagramme.route("/tokenize", methods=["POST", "GET"])
def get_tokenize():
    text = request.get_json()["text"]
    print(text)
    tokenized_text = tokenize(text)
    return jsonify({"success": True, "result": " ".join(tokenized_text)})


@anagramme.route("/possible_words", methods=["POST"])
def get_possible_words():
    text = request.get_json()["text"]
    words = text.split(" ")
    possible_words = [find_possible(word) for word in words if word]
    return jsonify({"success": True, "result": possible_words})


@anagramme.route("/load_cltk_libraries", methods=["GET"])
def load_cltk_libraries():
    print("chargé")
    return jsonify({"success": True, "result": AVAILABLE_LIBRARIES})


@anagramme.route("/find_anagrams", methods=["POST"])
def find_anagrams_with_data():
    data = request.get_json()
    library_choice = data["cltk_choice"]
    user_input = data["user_input"]
    text = data["text"]
    scale = data["scale"]

    if text:
        tokenized_text = tokenize(text)
    else:
        return jsonify({"success": True, "result": []})
    loaded_data = []
    if user_input != "":
        tokenized_user_input = tokenize(user_input)
        loaded_data.extend(tokenized_user_input)

    if "Latin proper names" in library_choice:
        loaded_data.extend(load_latin_proper_nouns())
    if "Latin texts" in library_choice:
        loaded_data.extend(load_latin_library())

    print(len(loaded_data))

    result = []
    if scale == "word":
        anagram_dictionary = compute_anagrams_dictionary(loaded_data)

        for token in tokenized_text:
            anagrams = find_word_anagrams(token, anagram_dictionary)
            if len(anagrams) > 0:
                result.append({"text": token, "anagrams": " ".join(anagrams)})
    elif scale == "sentence":
        anagrams = find_sentence_anagrams({i.lower() for i in loaded_data}, " ".join(tokenized_text).lower())
        if len(anagrams) > 0:
            result.append({"text": " ".join(tokenized_text), "anagrams": " ".join(anagrams)})

    return jsonify({"success": True, "result": result})
