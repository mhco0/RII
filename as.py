import json
import re
from utils import Utils
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

nltk.download("averaged_perceptron_tagger")
nltk.download("sentiwordnet")
nltk.download("wordnet")
from nltk.corpus import sentiwordnet as swn


def apply_score(json_data):
    for entry in json_data:
        for review in entry["reviews"]:
            total_score = {"pos_score": 0.0, "neg_score": 0.0, "obj_score": 0.0}
            for word in review["body"]:
                lemmatizer = WordNetLemmatizer()
                lemma = lemmatizer.lemmatize(word, pos="n")
                if not lemma:
                    continue

                synsets = list(swn.senti_synsets(word))

                pos_score = 0.0
                neg_score = 0.0
                obj_score = 0.0
                score_sum = 0.0

                for i in range(len(synsets)):
                    pos_score += synsets[i].pos_score() / (i + 1)
                    neg_score += synsets[i].neg_score() / (i + 1)
                    obj_score += synsets[i].obj_score() / (i + 1)
                    score_sum += 1.0 / (i + 1)

                if np.isclose(score_sum, 0.0):
                    continue

                total_score["pos_score"] += pos_score / score_sum
                total_score["neg_score"] += neg_score / score_sum
                total_score["obj_score"] += obj_score / score_sum

            review["sent"] = {
                "pos": total_score["pos_score"],
                "neg": total_score["neg_score"],
                "obj": total_score["obj_score"],
            }

            if review["sent"]["pos"] < review["sent"]["neg"]:
                review["sent_category"] = "negative"
            else:
                review["sent_category"] = "positive"

            star_score = review["rating"]
            review["match"] = 0

            if star_score < 3:
                review["category"] = "negative"
            else:
                review["category"] = "positive"

            if review["category"] == review["sent_category"]:
                review["match"] = 1

    return json_data


def main():
    json_translated = Utils.readJsonFile("./translated.json")
    Utils.writeJsonFile("scored.json", apply_score(json_translated))


if __name__ == "__main__":
    main()
