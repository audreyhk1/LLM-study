# Imports the Google Cloud Translation library
from google.cloud import translate
import os
from SECRET_KEYS.secret import CLOUD_PROJECT_ID
from SECRET_KEYS.secret import CLOUD_JSON_PATH 
# https://stackoverflow.com/questions/51554341/google-auth-exceptions-defaultcredentialserror
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CLOUD_JSON_PATH 

def main():
    text = "J'adore les pommes et les oranges"
    # https://cloud.google.com/translate/docs/languages
    translate_cloud(language="fr", text=text)

# Initialize Translation client
def translate_cloud(language: str, text: str, project_id: str = CLOUD_PROJECT_ID, target_lang: str = "en-US") -> translate.TranslationServiceClient:
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": language,
            "target_language_code": target_lang,
        }
    )
    for translation in response.translations:
        return translation.translated_text




if __name__ == "__main__":
    main()