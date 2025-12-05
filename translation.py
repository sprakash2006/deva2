# Updated translation.py with logging and improved fallback safety
from googletrans import Translator
import logging

translator = Translator()
logger = logging.getLogger(__name__)

def translate_to_english(text, source_lang):
    if not text:
        return ""
    if source_lang.lower() in ["en", "english"]:
        return text
    try:
        translated = translator.translate(text, src=source_lang, dest="en").text
        logger.info(f"Translated to English from {source_lang}")
        return translated
    except Exception as e:
        logger.warning(f"Translation to English failed: {e}")
        return text  # Fallback

def translate_from_english(text, target_lang):
    if not text:
        return ""
    if target_lang.lower() in ["en", "english"]:
        return text
    try:
        translated = translator.translate(text, src="en", dest=target_lang).text
        logger.info(f"Translated from English to {target_lang}")
        return translated
    except Exception as e:
        logger.warning(f"Translation from English failed: {e}")
        return text  # Fallback