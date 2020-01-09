from flask import jsonify, request

from . import main

from app.resource_manager import tokenize
from app.anagram import find_possible


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
