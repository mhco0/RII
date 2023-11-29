import json
import re
from utils import Utils


def main():
    json_data = Utils.readJsonFile("scored.json")
    positive_matches = 0
    negative_matches = 0
    true_negative = 0
    true_positive = 0
    false_positive = 0
    false_negative = 0
    total = 0

    for entry in json_data:
        for review in entry["reviews"]:
            if review["match"]:
                positive_matches += 1
                if review["category"] == "positive":
                    true_positive += 1
                else:
                    true_negative += 1
            else:
                negative_matches += 1

            if not review["match"] and review["category"] == "positive":
                false_positive += 1

            if not review["match"] and review["category"] == "negative":
                false_negative += 1

            total += 1

    print(f"\tMatch\tNot Match\tTotal\tFP\tFN\tPrecision\tRecall\tF1\n")
    print(
        f"\t{positive_matches}\t{negative_matches}\t\t{total}\t{false_positive}\t{false_negative}\t{true_positive/ (true_positive + false_positive):.2f}\t\t{true_negative/(true_negative + false_positive):.2f}\t{ (2 * true_positive)/ (2* true_positive + false_positive + false_negative):.2f}\n"
    )


if __name__ == "__main__":
    main()
