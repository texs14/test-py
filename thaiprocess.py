import sys
from pythainlp.transliterate import romanize
from pythainlp.util import tone_detector
from pythainlp.tokenize import word_tokenize
from pythainlp.tag import pos_tag

try:
    from googletrans import Translator
    _translator = Translator()
except Exception:
    _translator = None

def transliterate_word(word: str) -> str:
    return romanize(word)

def syllable_tone(syllable: str) -> str:
    return tone_detector(syllable)

def word_tones(word: str):
    tokens = word_tokenize(word, engine="newmm")
    return [(tok, tone_detector(tok)) for tok in tokens]

def part_of_speech(text: str):
    tokens = word_tokenize(text, engine="newmm")
    return pos_tag(tokens, corpus="orchid_ud")

def translate_word(word: str, dest: str) -> str:
    if _translator is None:
        raise RuntimeError("translator unavailable")
    return _translator.translate(word, src="th", dest=dest).text

if __name__ == "__main__":
    if not sys.argv[1:]:
        print("Usage: python thaiprocess.py <thai_word>")
        sys.exit(1)
    word = sys.argv[1]
    print("Romanization:", transliterate_word(word))
    print("Syllable tones:", word_tones(word))
    print("POS tags:", part_of_speech(word))
    if _translator:
        for lang in ["en", "ru", "zh-cn"]:
            try:
                print(f"{lang}:", translate_word(word, lang))
            except Exception as e:
                print(f"{lang} translation failed:", e)
    else:
        print("Translation is unavailable (googletrans not installed or network issue)")
