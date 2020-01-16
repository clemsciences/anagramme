from flask import jsonify, request

from . import main

from app.resource_manager import tokenize, AVAILABLE_LIBRARIES, load_latin_proper_nouns, load_latin_library
from app.anagram import find_possible, compute_anagrams_dictionary, find_anagrams


@main.route("/tokenize", methods=["POST", "GET"])
def get_tokenize():
    text = request.get_json()["text"]
    print(text)
    tokenized_text = tokenize(text)
    return jsonify({"success": True, "result": " ".join(tokenized_text)})


@main.route("/possible_words", methods=["POST"])
def get_possible_words():
    text = request.get_json()["text"]
    words = text.split(" ")
    possible_words = [find_possible(word) for word in words if word]
    return jsonify({"success": True, "result": possible_words})


@main.route("/load_cltk_libraries", methods=["GET"])
def load_cltk_libraries():
    print("chargé")
    return jsonify({"success": True, "result": AVAILABLE_LIBRARIES})


@main.route("/find_anagrams", methods=["GET"])
def find_anagrams_with_data():
    data = request.get_json()
    library_choice = data["cltk_choice"]
    user_input = data["user_input"]
    text = data["text"]

    if text:
        tokenized_text = tokenize(text)
    else:
        return jsonify({"success": True, "result": []})
    loaded_data = []
    if user_input != "":
        tokenized_user_input = tokenize(user_input)
        loaded_data.extend(tokenized_user_input)

    if library_choice == "":
        loaded_data.extend(load_latin_proper_nouns())
    elif library_choice == "":
        loaded_data.extend(load_latin_library())

    anagram_dctionary = compute_anagrams_dictionary(loaded_data)
    result = []
    for token in tokenized_text:
        result.append(find_anagrams(token, anagram_dctionary))
    return jsonify({"success": True, "result": result})
