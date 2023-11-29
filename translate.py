import json
from preprocessing import bow, tokenize_field
from utils import Utils

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


def get_english_reviews(json_data):
    i = 0

    for entry in json_data:
        for review in entry["reviews"]:
            bag = bow(review["body"])

            list_of_keys = list(bag.keys())

            for word in bag:
                word = argostranslate.translate.translate(word, from_code, to_code)
                list_of_keys.append(word)

            review["body"] = " ".join(list_of_keys)
            review["body"] = tokenize_field(review, "body", "english")

        i += 1
        print(f"run : {i / len(json_data)}%")

    return json_data


def main():
    json_data = Utils.readJsonFile("preprocessed.json")
    Utils.writeJsonFile("translated.json", get_english_reviews(json_data))


if __name__ == "__main__":
    main()
