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
        scores = {"body": 0.0, "title": 0.0}

        for score_key in scores.keys():
            for review in entry["reviews"]:
                total_score = {"pos_score": 0.0, "neg_score": 0.0, "obj_score": 0.0}
                for word in review[score_key]:
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

                review["score_" + score_key] = {
                    "pos": total_score["pos_score"],
                    "neg": total_score["neg_score"],
                    "obj": total_score["obj_score"],
                }

    return json_data


def main():
    json_preprocessed = Utils.readJsonFile("./preprocessed.json")
    print(json.dumps(apply_score(json_preprocessed), indent=4))


if __name__ == "__main__":
    main()
