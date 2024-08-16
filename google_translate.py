# Imports the Google Cloud Translation library
from google.cloud import translate

def main():
    text = "I love apples"
    project_id = "august-jigsaw-432021-r7"
    
    translate_text(text=text, project_id=project_id)

# Initialize Translation client
def translate_text(text: str = "YOUR_TEXT_TO_TRANSLATE", project_id: str = "YOUR_PROJECT_ID") -> translate.TranslationServiceClient:
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
        print(f"Translated text: {translation.translated_text}")

    return response
