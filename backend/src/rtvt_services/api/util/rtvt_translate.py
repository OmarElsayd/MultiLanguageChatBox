import os

from google.cloud import translate


def translate_text_(source_language_code: str, text: str, target_language_code: str) -> str:
    if source_language_code == target_language_code:
        return text

    client = translate.TranslationServiceClient()
    response = client.translate_text(
        parent=os.getenv('PROJECT_ID'),
        contents=[text],
        target_language_code=target_language_code,
        source_language_code=source_language_code
    )

    return response.translations[0]
