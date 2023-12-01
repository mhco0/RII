import json
import re
from utils import Utils
import pandas as pd
import matplotlib.pyplot as plt


def main():
    json_data = Utils.readJsonFile("scored.json")

    true_negative = 0
    true_positive = 0
    false_positive = 0
    false_negative = 0
    total_positive = 0
    total_negative = 0

    for entry in json_data:
        for review in entry["reviews"]:
            if review["match"]:
                if review["sent_category"] == "positive":
                    true_positive += 1
                else:
                    true_negative += 1

            if not review["match"] and review["sent_category"] == "positive":
                false_positive += 1

            if not review["match"] and review["sent_category"] == "negative":
                false_negative += 1

            if review["category"] == "positive":
                total_positive += 1
            else:
                total_negative += 1

    array = [
        [
            true_positive,
            false_positive,
            false_negative / (true_positive + false_negative),
            total_positive,
            true_positive + false_positive,
        ],
        [
            false_negative,
            true_negative,
            false_positive / (false_positive + true_negative),
            total_negative,
            false_negative + true_negative,
        ],
    ]

    data_frame = pd.DataFrame(
        array,
        ["positive", "negative"],
        [
            "Senti Positive",
            "Senti Negative",
            "Error by class",
            "Total Real",
            "Total Senti",
        ],
    )

    print(data_frame)
    print(
        f"Error total = {(false_negative + false_positive) / (true_positive + true_negative + false_negative + false_positive):2f}\nAccuracy = {(true_positive + true_negative)/ (true_positive + true_negative + false_negative + false_positive):2f}"
    )


if __name__ == "__main__":
    main()
