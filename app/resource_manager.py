from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.latin.corpora import LATIN_CORPORA

from cltk.tokenize.latin.word import WordTokenizer
ci = CorpusImporter("latin")

# ci.import_corpus()
wt = WordTokenizer()

tokenize = wt.tokenize
