import argostranslate.package
import argostranslate.translate

def translate_text(text: str, from_lang: str, to_lang: str) -> str:
    try:
        translated = argostranslate.translate.translate(text, from_lang, to_lang)
        return translated
    except Exception as e:
        return f"Translation error: {str(e)}"

def setup_translation(from_lang: str = "en", to_lang: str = "bn"):
    argostranslate.package.update_package_index()
    available = argostranslate.package.get_available_packages()
    package = next(
        filter(lambda x: x.from_code == from_lang and x.to_code == to_lang, available),
        None
    )
    if package:
        argostranslate.package.install_from_path(package.download())