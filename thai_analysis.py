import json
import sys

try:
    from polyglot.text import Text
except Exception:
    Text = None

try:
    from pythainlp.transliterate import romanize
    from pythainlp.util import thai_word_tone_detector
    from pythainlp.tag import pos_tag
    from pythainlp.tokenize import word_tokenize
except Exception:
    romanize = None
    thai_word_tone_detector = None
    pos_tag = None
    word_tokenize = None

try:
    from googletrans import Translator
except Exception:
    Translator = None


def transliterate_text(th_text: str) -> str:
    """Transliterate Thai text to Latin."""
    if Text:
        try:
            t = Text(th_text, hint_language_code="th")
            return str(t.transliterate())
        except Exception:
            pass
    if romanize:
        try:
            return romanize(th_text)
        except Exception:
            pass
    return ""


def detect_tones(th_text: str):
    """Return tone information for Thai word if available."""
    if thai_word_tone_detector:
        try:
            return thai_word_tone_detector(th_text)
        except Exception:
            pass
    return None


def pos_tags(th_text: str):
    if pos_tag and word_tokenize:
        try:
            tokens = word_tokenize(th_text)
            return pos_tag(tokens, engine="perceptron")
        except Exception:
            pass
    return None


def translate(th_text: str, dest: str):
    if Translator:
        try:
            tr = Translator()
            tr.raise_Exception = False  # type: ignore
            result = tr.translate(th_text, src="th", dest=dest)
            return result.text
        except Exception:
            pass
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python thai_analysis.py <thai text>")
        return
    text = sys.argv[1]
    data = {
        "transliteration": transliterate_text(text),
        "tones": detect_tones(text),
        "pos": pos_tags(text),
        "translations": {
            "en": translate(text, "en"),
            "ru": translate(text, "ru"),
            "zh": translate(text, "zh-cn"),
        },
    }
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()