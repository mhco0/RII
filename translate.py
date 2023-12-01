import json
import unidecode
from filtered import bow, tokenize_field
from utils import Utils
from spellchecker import SpellChecker

import argostranslate.package
import argostranslate.translate

from_code = "pt"
to_code = "en"

# Download and install Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())


def try_correct_spelling(json_data):
    spell = SpellChecker(language="pt")
    print("Trying to correct....")
    i = 0
    for entry in json_data:
        for review in entry["reviews"]:
            words = spell.split_words(unidecode.unidecode(review["body"]))

            list_of_correct_words = []

            for word in words:
                correct_word = spell.correction(word)
                if correct_word:
                    list_of_correct_words.append(correct_word)
                else:
                    list_of_correct_words.append(word)

            review["probably_correct_body"] = list_of_correct_words

        i += 1
        print(f"run : {i / len(json_data)}%")

    return json_data


def translate_text(json_data):
    i = 0
    print("Trying to translate...")

    for entry in json_data:
        for review in entry["reviews"]:
            bag = bow(review["probably_correct_body"])

            list_of_translated_words = []

            for word in bag.keys():
                word = argostranslate.translate.translate(word, from_code, to_code)
                word_list = list(set(word.split()))
                list_of_translated_words.append(" ".join(word_list))

            if list_of_translated_words:
                review["body"] = " ".join(list_of_translated_words)
            else:
                review["body"] = review["probably_correct_body"]
            review["body"] = tokenize_field(review, "body", "english")

        i += 1
        print(f"run : {i / len(json_data)}%")

    return json_data


def main():
    # json_data = Utils.readJsonFile("filtered.json")
    # json_data = try_correct_spelling(json_data)
    # Utils.writeJsonFile("correct_spelling.json", json_data)
    json_data = Utils.readJsonFile("correct_spelling.json")
    json_data = translate_text(json_data)
    Utils.writeJsonFile("translated2.json", json_data)


if __name__ == "__main__":
    main()
