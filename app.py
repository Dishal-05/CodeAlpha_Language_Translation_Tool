# ============================================================
# app.py - Flask Backend for Language Translator
# ============================================================
# CodeAlpha AI Internship Project: Language Translation Tool
#
# Highlights:
#   1. Powered by Microsoft Bing Neural Translation engine (via translators library).
#   2. Zero API keys required (100% free and ready to demo).
#   3. Immune to Google's HTTP 429 rate-limiting blocks.
#   4. Multi-engine automatic fallback (Bing -> Alibaba -> Yandex).
#   5. Clean JSON REST API endpoint for the web front-end.
# ============================================================

import os

# Prevent region lookups during offline/cold startup
os.environ["translators_default_region"] = "EN"

from flask import Flask, render_template, request, jsonify
import translators as ts

# Initialize Flask application
app = Flask(__name__)

# ── Supported Languages ──────────────────────────────────────
# Standard ISO / BCP-47 language codes accepted by Microsoft Translator
LANGUAGES = {
    "Auto Detect":            "auto",
    "Afrikaans":              "af",
    "Albanian":               "sq",
    "Amharic":                "am",
    "Arabic":                 "ar",
    "Armenian":               "hy",
    "Azerbaijani":            "az",
    "Bengali":                "bn",
    "Bosnian":                "bs",
    "Bulgarian":              "bg",
    "Catalan":                "ca",
    "Chinese (Simplified)":   "zh-Hans",
    "Chinese (Traditional)":  "zh-Hant",
    "Croatian":               "hr",
    "Czech":                  "cs",
    "Danish":                 "da",
    "Dutch":                  "nl",
    "English":                "en",
    "Estonian":               "et",
    "Filipino":               "fil",
    "Finnish":                "fi",
    "French":                 "fr",
    "Georgian":               "ka",
    "German":                 "de",
    "Greek":                  "el",
    "Gujarati":               "gu",
    "Haitian Creole":         "ht",
    "Hebrew":                 "he",
    "Hindi":                  "hi",
    "Hungarian":              "hu",
    "Icelandic":              "is",
    "Indonesian":             "id",
    "Irish":                  "ga",
    "Italian":                "it",
    "Japanese":               "ja",
    "Kannada":                "kn",
    "Kazakh":                 "kk",
    "Korean":                 "ko",
    "Latvian":                "lv",
    "Lithuanian":             "lt",
    "Macedonian":             "mk",
    "Malay":                  "ms",
    "Malayalam":              "ml",
    "Maltese":                "mt",
    "Maori":                  "mi",
    "Marathi":                "mr",
    "Mongolian":              "mn-Cyrl",
    "Nepali":                 "ne",
    "Norwegian":              "nb",
    "Persian":                "fa",
    "Polish":                 "pl",
    "Portuguese":             "pt",
    "Punjabi":                "pa",
    "Romanian":               "ro",
    "Russian":                "ru",
    "Serbian":                "sr-Cyrl",
    "Slovak":                 "sk",
    "Slovenian":              "sl",
    "Somali":                 "so",
    "Spanish":                "es",
    "Swahili":                "sw",
    "Swedish":                "sv",
    "Tamil":                  "ta",
    "Telugu":                 "te",
    "Thai":                   "th",
    "Turkish":                "tr",
    "Ukrainian":              "uk",
    "Urdu":                   "ur",
    "Uzbek":                  "uz",
    "Vietnamese":             "vi",
    "Welsh":                  "cy",
    "Yiddish":                "yi",
    "Zulu":                   "zu",
}


def perform_translation(text: str, source: str, target: str):
    """
    Translates text using Microsoft Bing as primary engine,
    with automatic fallbacks to Alibaba and Yandex if needed.
    """
    engines = [
        ("bing", "Microsoft Bing"),
        ("alibaba", "Alibaba"),
        ("yandex", "Yandex"),
    ]

    last_error = None
    for engine_key, engine_name in engines:
        try:
            translated = ts.translate_text(
                query_text=text,
                translator=engine_key,
                from_language=source,
                to_language=target,
            )
            if translated and str(translated).strip():
                return str(translated).strip(), engine_name
        except Exception as e:
            last_error = e
            continue

    raise Exception(f"All translation engines were busy or unavailable. Details: {last_error}")


# ── Routes ────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serves the main application page."""
    return render_template("index.html", languages=LANGUAGES)


@app.route("/translate", methods=["POST"])
def translate():
    """
    API endpoint: receives JSON { text, source_lang, target_lang }
    and returns { translated_text, service } or { error }.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request format. Expected JSON."}), 400

    text = data.get("text", "").strip()
    source_lang = data.get("source_lang", "auto")
    target_lang = data.get("target_lang", "fr")

    # Input validation
    if not text:
        return jsonify({"error": "Please enter some text to translate."}), 400

    if not target_lang or target_lang == "auto":
        return jsonify({"error": "Please select a specific target language."}), 400

    if source_lang == target_lang and source_lang != "auto":
        return jsonify({"error": "Source and target languages cannot be identical."}), 400

    try:
        translated_text, service = perform_translation(text, source_lang, target_lang)
        return jsonify({
            "translated_text": translated_text,
            "service": service,
        })
    except Exception as e:
        return jsonify({"error": f"Translation error: {str(e)}"}), 500


# ── Entry point ────────────────────────────────────────────────
if __name__ == "__main__":
    # Host on 127.0.0.1:5000 for local development and demonstration
    app.run(debug=True, host="127.0.0.1", port=5000)
