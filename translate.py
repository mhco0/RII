import json
import re
from utils import Utils
import numpy as np
import unidecode
import nltk
from nltk.tokenize import word_tokenize

nltk.download("stopwords")
from nltk.corpus import stopwords


def bow(json_data):
    word_dict = {}

    for entry in json_data:
        for review in entry["reviews"]:
            for word in review["body"]:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1

            for word in review["title"]:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1

    return word_dict


def simplifly_dict(translation_dictonary):
    t_dict = {}

    for word in translation_dictonary["words"]:
        unidecode_text = unidecode.unidecode(word["targetWord"])

        # Substitute point and go to lower case
        removed_dots = re.sub("[^A-Za-z]", " ", unidecode_text)
        removed_dots = removed_dots.lower()

        tokenized_text = word_tokenize(removed_dots, language="portuguese")

        word["targetWord"]= tokenized_text[0]

        t_dict[word["targetWord"]] = word["englishWord"]

    return t_dict


def translate(bow, translate_dict):
    translation = {}

    for word in bow:
        if word in translate_dict:
            translation[word] = translate_dict[word]
        else:
            translation[word] = word

    return translation


def main():
    json_preprocessed = Utils.readJsonFile("./preprocessed.json")
    translation_dictonary = Utils.readJsonFile("./pt.json")

    bag = bow(json_preprocessed)

    print(json.dumps(translate(bag, simplifly_dict(translation_dictonary)), indent=4))


if __name__ == "__main__":
    main()
