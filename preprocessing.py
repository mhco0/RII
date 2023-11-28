import numpy as np
import json
import re
import unidecode
from utils import Utils
import nltk

nltk.download("punkt")
from nltk.tokenize import word_tokenize

nltk.download("stopwords")
from nltk.corpus import stopwords

from nltk.stem.porter import *


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
    stemmer = PorterStemmer()

    for entry in json_data:
        for review in entry["reviews"]:
            review["body"] = tokenize_field(review, "body")
            for word in review["body"]:
                word = stemmer.stem(word)
            review["title"] = tokenize_field(review, "title")
            for word in review["title"]:
                word = stemmer.stem(word)

    return json_data


def load_db():
    return Utils.readJsonFile("bookccw\\amazon.json")


def save_db(path, json):
    Utils.writeJsonFile(path, json)


def main():
    json_data = load_db()
    json_data = filter_data(json_data)
    json_data = pre_process(json_data)
    save_db("./preprocessed.json", json_data)


if __name__ == "__main__":
    main()
