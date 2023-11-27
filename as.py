import numpy as np
import json
import re
import unidecode
from utils import Utils
from deep_translator import PonsTranslator
import nltk

from nltk.stem import WordNetLemmatizer

nltk.download("averaged_perceptron_tagger")
nltk.download("sentiwordnet")
nltk.download("wordnet")
from nltk.corpus import sentiwordnet as swn

nltk.download("punkt")
from nltk.tokenize import word_tokenize

nltk.download("stopwords")
from nltk.corpus import stopwords


def filter_data(json_data):
    new_data = []

    for entry in json_data:
        graph = entry["@graph"]
        for info in graph:
            if info["@type"] != "Product":
                continue

            if "review" not in info:
                continue

            new_json = {
                "name": info["name"],
                "description": info["description"],
                "url": info["url"],
                "sku": info["sku"],
                "aggregate": info["aggregateRating"]["ratingValue"],
                "reviews": [],
            }

            for review in info["review"]:
                if review["@type"] != "Review":
                    continue

                new_json["reviews"].append(
                    {
                        "rating": review["reviewRating"]["ratingValue"],
                        "date": review["datePublished"],
                        "author": review["author"]["id"],
                        "body": review["reviewBody"],
                        "title": review["name"],
                    }
                )

            new_data.append(new_json)

    return new_data


def tokenize_field(json_data, field):
    unidecode_text = unidecode.unidecode(json_data[field])

    # Substitute point and go to lower case
    removed_dots = re.sub("[^A-Za-z]", " ", unidecode_text)
    removed_dots = removed_dots.lower()

    tokenized_text = word_tokenize(removed_dots, language="portuguese")

    for word in tokenized_text:
        if word in stopwords.words("portuguese"):
            tokenized_text.remove(word)

    return tokenized_text


def pre_process(json_data):
    for entry in json_data:
        for review in entry["reviews"]:
            review["body"] = tokenize_field(review, "body")
            review["title"] = tokenize_field(review, "title")

    return json_data


def load_db():
    return Utils.readJsonFile("bookccw\\amazon.json")



def apply_score(json_data):
    for entry in json_data:
        scores = {"body": 0.0, "title": 0.0}

        for score_key in scores.keys():
            pos_score = 0.0
            neg_score = 0.0
            obj_score = 0.0

            for review in entry["reviews"]:
                for word in review[score_key]:
                    lemmatizer = WordNetLemmatizer()
                    lemma = lemmatizer.lemmatize(word, pos="n")
                    if not lemma:
                        continue

                    synsets = swn.synsets(word, pos=wn_tag)
                    synset = synsets[0]
                    swn_synset = swn.senti_synset(synset.name())

                    pos_score += swn_synset.pos_score()
                    neg_score += swn_synset.neg_score()
                    obj_score += swn_synset.obj_score()

                review["score_" + score_key] = {
                    "pos": pos_score,
                    "neg": neg_score,
                    "obj": obj_score,
                }

    return json_data


def main():
    json_data = load_db()
    json_data = filter_data(json_data)
    json_data = pre_process(json_data)
    print(json.dumps(apply_score(json_data), indent=4))


if __name__ == "__main__":
    main()
