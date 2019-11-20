"""Another quick and dirty script to evaluate the models on UD data."""

import json
import _jsonnet
import os

SERIALIZATION_DIR = "back/ud/trainedmodels"
CONFIG_DIR = "back/configs"
DATA_PATH = "back/ud/data/processed"
TRAIN_CMD = (
    "allennlp train -s {directory} -f --include-package back {config}"
)
TASKS = ["pos-tagging", "translation", "classification"]


def train(language, task):
    """Train a model for `task` in `language`."""
    config_file_name = os.path.join(CONFIG_DIR, f"{task}.jsonnet")
    serialization_directory = os.path.join(SERIALIZATION_DIR, task, language)
    if task == "classification":
        ext = "jsonl"
    else:
        ext = "txt"
    train_data_path = os.path.join(DATA_PATH, task, language, f"train.{ext}")
    validation_data_path = os.path.join(DATA_PATH, task, language, f"valid.{ext}")
    # The -o override flag in allennlp train was finicky so I used a temporary file hack
    config = json.loads(_jsonnet.evaluate_file(config_file_name))
    config["train_data_path"] = train_data_path
    config["validation_data_path"] = validation_data_path
    with open("tmp.jsonnet", "w") as file:
        json.dump(config, file, indent=2)
    cmd = TRAIN_CMD.format(
        config="tmp.jsonnet", directory=serialization_directory
    )
    os.system(cmd)
    cmd = "rm tmp.jsonnet"
    os.system(cmd)

if __name__ == "__main__":
    tasks = os.listdir(DATA_PATH)
    for task in tasks:
        languages = os.listdir(os.path.join(DATA_PATH, task))
        for language in languages:
            print(f"Training {task} for {language}")
            train(language, task)

