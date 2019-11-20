"""Quick and dirty script to extract results from UD evaluation."""
import os
import glob
import json

import pandas as pd

SERIALIZATION_DIR = "back/ud/trainedmodels"
TASKS = ["pos-tagging", "translation", "classification"]

results = []
for task in TASKS:
    path = os.path.join(SERIALIZATION_DIR, task)
    for language in sorted(os.listdir(path)):
        metrics_filename = os.path.join(path, language, "metrics.json")
        with open(metrics_filename) as file:
            metrics = json.load(file)
        if task == "translation":
            score = metrics["validation_BLEU"]
        else:
            score = metrics["validation_accuracy"]
        score = round(score*100, 1)
        config_filename = os.path.join(path, language, "config.json")
        with open(config_filename) as file:
            config = json.load(file)
        train_data_path = config["train_data_path"]
        with open(train_data_path) as file:
            train_data = file.read()
        num_training_examples = len(train_data.split("\n"))
        print(language, task, score, num_training_examples)
        print()
        num_training_examples = len(train_data.split("\n"))
        results.append({"language": language, "task": task, "score": score, "num": num_training_examples})
results = pd.DataFrame(results)
results.to_csv("scripts/results.csv", index=False)