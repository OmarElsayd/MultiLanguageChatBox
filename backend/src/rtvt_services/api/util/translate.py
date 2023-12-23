import langid
from translate import Translator

from rtvt_services.dependency.exception_handler import TranslationException
from rtvt_services.util.constant import SUPPORTED_LANGS, MAX_LENGTH_PER_STR


def translate_text(text: str, target_language: str):
    if len(text) > MAX_LENGTH_PER_STR:
        raise TranslationException(
            "Text length exceeded the str len limit"
        )
    target_language = supported_lang(target_language)

    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)

    return translation


# Potentially the front end will be responsible for detecting the lang
# Hold on this or now
def detect_language(text: str):
    lang, confidence = langid.classify(text)
    return lang, confidence


def supported_lang(target_language: str):
    if target_language not in SUPPORTED_LANGS:
        raise TranslationException(
            f"{target_language} language is not supported"
        )
    return target_language
