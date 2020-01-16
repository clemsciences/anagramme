import codecs
import os
from typing import Set, List

from cltk.corpus.utils.importer import CorpusImporter

from cltk.tokenize.latin.word import WordTokenizer
ci = CorpusImporter("latin")
wt = WordTokenizer()

tokenize = wt.tokenize

print([c for c in ci.all_corpora])

AVAILABLE_LIBRARIES = {
    "latin_proper_names_cltk": "Latin proper names",
    "latin_text_latin_library": "Latin texts"
}


def load_latin_proper_nouns() -> List[str]:
    corpus_path = os.path.join(os.environ.get("HOME"), "cltk_data", "latin", "lexicon", "latin_proper_names_cltk")
    if not os.path.exists(corpus_path):
        ci.import_corpus("latin_proper_names_cltk")
    with codecs.open(os.path.join(corpus_path, "proper_names"), "r") as f:
        nouns = f.read().split(os.linesep)
    return nouns


def tokenize_raw_text(text: str) -> List[str]:
    text = text.replace("\n", " ")
    return tokenize(text)


def filter_text(word: str) -> bool:
    if word:
        return True
    return False


def clean_word(word: str) -> str:
    return word


def load_latin_library() -> Set[str]:
    words = set()
    corpus_path = os.path.join(os.path.expanduser("~"), "cltk_data", "latin", "text", "latin_text_latin_library")
    if not os.path.exists(corpus_path):
        ci.import_corpus("latin_text_latin_library")
    for filename in os.listdir(corpus_path):
        if filename[0] == ".":
            continue
        if os.path.isfile(os.path.join(corpus_path, filename)):
            with codecs.open(os.path.join(corpus_path, filename), "r", encoding="utf-8") as f:
                text = [clean_word(word) for word in tokenize_raw_text(f.read()) if filter_text(word)]
                words.update(set(text))
        else:
            for filename_2 in os.listdir(os.path.join(corpus_path, filename)):
                if filename_2[0] != ".":
                    continue
                if os.path.isfile(os.path.join(corpus_path, filename, filename_2)):
                    with codecs.open(os.path.join(corpus_path, filename), "r", encoding="utf-8") as f:
                        text = tokenize_raw_text(f.read())
                        words.update(set(text))
    return words


def make_lexicon() -> bool:
    words = load_latin_library()
    with codecs.open("latin_words.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(words))
    return True


if __name__ == "__main__":
    make_lexicon()
