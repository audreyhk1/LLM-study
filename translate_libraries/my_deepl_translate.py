import deepl
from SECRET_KEYS.secret import DEEPL_KEY

def main():
    print(deepl_translate("Hallo, Welt!", "DE"))

def deepl_translate(text, from_lang_to_eng, auth_key: str = DEEPL_KEY, source_language: str = "EN"):
    translator = deepl.Translator(auth_key)

    # all languages - https://developers.deepl.com/docs/api-reference/languages
    result = translator.translate_text(text, source_lang=source_language, target_lang=from_lang_to_eng)
    return result.text

if __name__ == "__main__":
    main()
    
