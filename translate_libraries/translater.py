# https://translate-python.readthedocs.io/en/latest/providers.html
from translate.translate import Translator

def main():
    text = "I love apples and oranges"
    print(py_translater("fr", text))
    

# https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes
def py_translater(language: str, text: str):
    translator = Translator(to_lang=language)
    return translator.translate(text)


if __name__ == "__main__":
    main()
