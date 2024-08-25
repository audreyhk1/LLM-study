import deepl
from SECRET_KEYS.secret import DEEPL_KEY

def main():
    print(deepl_translate("Hallo, Welt!", "DE"))

def deepl_translate(text, from_lang_to_eng, auth_key: str = DEEPL_KEY):
    translator = deepl.Translator(auth_key)

    # all languages - https://developers.deepl.com/docs/api-reference/languages
    return translator.translate_text(text, source_lang=from_lang_to_eng, target_lang="EN-US")

if __name__ == "__main__":
    main()
    
