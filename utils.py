import os
import re
import json


class Utils:
    @staticmethod
    def readFile(path) -> str:
        newPath = os.path.join(os.path.dirname(__file__), path)
        with open(newPath, "r", encoding="utf-8") as f:
            data = f.read()
        return data

    @staticmethod
    def regexSearch(pattern, page) -> str:
        try:
            result = re.search(pattern, page).group(1)
        except:
            result = ""
        return result

    @staticmethod
    def getFilenames(path) -> list:
        newPath = os.path.join(os.path.dirname(__file__), path)
        filenames = next(os.walk(newPath), (None, None, []))[2]
        return filenames

    @staticmethod
    def readJsonFile(path):
        jsonPath = os.path.join(os.path.dirname(__file__), path)
        with open(jsonPath, encoding="utf-8") as f:
            jsonData = json.load(f)
        return jsonData

    @staticmethod
    def writeJsonFile(path, obj):
        jsonPath = os.path.join(os.path.dirname(__file__), path)
        with open(jsonPath, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)
