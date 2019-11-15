"""Quick and dirty script to prepare UD data for my different tasks."""

import glob
import os
import re
from xml.etree import ElementTree

from conllu import parse

THRESHOLD = 50_000


def languages_under_threshold(threshold):
    """Return the names of languages with UD corpora totalling under `threshold` tokens."""
    file_names = glob.glob("back/ud/**/stats.xml", recursive=True)
    result = {}
    for file_name in file_names:
        directory = os.path.split(os.path.split(file_name)[0])[1]
        language = re.match(r"UD_(\w+)-\w+", directory).groups(1)[0]
        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        num_tokens = int(root.find("./size/total/tokens").text)
        if language not in result:
            result[language] = num_tokens
        else:
            result[language] += num_tokens
    return sorted([lg for lg, num in result.items() if num <= threshold])


languages = languages_under_threshold(THRESHOLD)
print(languages)

lg = languages[0]
dir_names = [dir_name for dir_name in os.listdir("back/ud") if lg in dir_name]
file_names = []
for dir_name in dir_names:
    pattern = f"back/ud/{dir_name}/*.conllu"
    file_names.extend(glob.glob(pattern))
for file_name in file_names:
    data = parse(file_name)
