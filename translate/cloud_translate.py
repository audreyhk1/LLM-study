# Imports the Google Cloud Translation library
from google.cloud import translate
import os
from SECRET_KEYS.secret import CLOUD_PROJECT_ID
from SECRET_KEYS.secret import CLOUD_JSON_PATH 
# https://stackoverflow.com/questions/51554341/google-auth-exceptions-defaultcredentialserror
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CLOUD_JSON_PATH 

def main():
    text = "I love apples"
    translate_text(text=text)

# Initialize Translation client
def translate_text(text: str, project_id: str = CLOUD_PROJECT_ID) -> translate.TranslationServiceClient:
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
            "source_language_code": "en-US",
            "target_language_code": "fr",
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print(f"{translation.translated_text}")

    return response



if __name__ == "__main__":
    main()