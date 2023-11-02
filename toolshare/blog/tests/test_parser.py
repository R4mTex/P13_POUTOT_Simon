from blog.scripts.parser import Parser, ocStopWords, customStopWords
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize


# Create your tests here.
def test_should_remove_upper_case():
    sut = Parser
    text = 'ABC'
    expected_value = 'abc'
    assert sut.removeUpperCase(text) == expected_value


def test_should_remove_ponctuation():
    sut = Parser
    text = 'a.b!c?'
    expected_value = 'abc'
    assert sut.removePonctuation(text) == expected_value


def test_should_remove_accent():
    sut = Parser
    text = 'áôè'
    expected_value = 'aoe'
    assert sut.removeAccent(text) == expected_value


def test_should_remove_stop_word():
    sut = Parser
    stop_words = set(ocStopWords + customStopWords)
    text = 'coucou estce connais ladresse'
    word_tokens = word_tokenize(text)
    expected_value = [word for word in word_tokens if not word.lower() in stop_words]

    assert sut.removeStopWord(text) == expected_value


def test_should_parse():
    sut = Parser
    text = "Salut GrandPy, est-ce que tu sais comment aller sur Paris ?"
    expected_value = ['paris']
    assert sut.scriptForParse(text) == expected_value
