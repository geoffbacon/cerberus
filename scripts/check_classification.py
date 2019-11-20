"""Check how many classes there are in the classification task of each language."""
import os
import jsonlines

DATA_PATH = "back/ud/data/processed/classification"

for lg in os.listdir(DATA_PATH):
    filename = os.path.join(DATA_PATH, lg, "train.jsonl")
    labels = []
    with jsonlines.open(filename) as reader:
        for line in reader:
            label = line["label"]
            labels.append(label)
    labels = set(labels)
    print(lg, len(labels), labels)