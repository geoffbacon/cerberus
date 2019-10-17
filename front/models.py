"""Utilities for working with the backend models."""

import json
import os
import re
import shutil
import time

from allennlp.predictors import Predictor

SERIALIZATION_DIR = "back/trainedmodels"
CONFIG_DIR = "back/configs"
TRAIN_CMD = "allennlp train {config} -s {directory} -f --include-package back &"
TASKS = ["POS tagging", "Translation", "Classification", "Language modeling"]
PREDICTOR_NAMES = {
    "pos-tagging": "sentence-tagger",
    "translation": "seq2seq",
    "classification": "text_classifier",
}


def is_trained(slug):
    """Return True if we already have a trained model for the task `slug`."""
    model_file_name = os.path.join(SERIALIZATION_DIR, slug, "model.tar.gz")
    return os.path.exists(model_file_name)


def train(slug, sidebar_train_message, training_message):
    """Train a model for `slug`."""
    config_file_name = os.path.join(CONFIG_DIR, f"{slug}.jsonnet")
    serialization_directory = os.path.join(SERIALIZATION_DIR, slug)
    refresh_directory(
        serialization_directory
    )  # because we use `is_trained` to know when the training is finished
    cmd = TRAIN_CMD.format(config=config_file_name, directory=serialization_directory)
    os.system(cmd)
    while not is_trained(slug):  # will loop indefinitely if error in the previous line
        time_remaining = get_time_remaining(slug) or "Unknown"
        message = f"{training_message}\n\nTime remaining: {time_remaining}"
        sidebar_train_message.info(message)
        time.sleep(1)


def refresh_directory(path):
    """Create new directory at `path`."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)


def get_time_remaining(slug):
    """Return the estimated training time remaining for the task `slug`."""
    log_file_name = os.path.join(SERIALIZATION_DIR, slug, "stdout.log")
    pattern = re.compile(r"Estimated training time remaining: (.*)$", re.MULTILINE)
    try:
        with open(log_file_name) as file:
            logs = file.read()
        matches = pattern.findall(logs)
        if matches:
            return matches[-1]
    except FileNotFoundError:
        pass


def get_metrics(slug):
    """Return useful metrics about the training process for the task `slug`."""
    assert is_trained(slug), "We haven't trained a model to get metrics from yet"
    metrics_file_name = os.path.join(SERIALIZATION_DIR, slug, "metrics.json")
    with open(metrics_file_name, "rb") as file:
        metrics = json.load(file)
    duration = metrics["training_duration"]
    duration = duration.split(".")[0]  # remove milliseconds
    # for the time being, just get accuracy
    score = metrics.get("training_accuracy", "Undefined")
    if isinstance(score, float):
        score = f"{round(score * 100, 1)}%"
    return {"Duration": duration, "Accuracy": score}


def load_model(slug):
    """Return an AllenNLP Predictor for the trained model for `slug`."""
    assert is_trained(slug), "We haven't trained a model to load yet"
    model_file_name = os.path.join(SERIALIZATION_DIR, slug, "model.tar.gz")
    name = PREDICTOR_NAMES[slug]
    return Predictor.from_path(model_file_name, predictor_name=name)


def predict(slug, text):
    """Run trained model for `slug` over user's input `text`."""
    predictor = load_model(slug)
    return predictor.predict(text)
