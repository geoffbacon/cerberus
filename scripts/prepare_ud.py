"""Quick and dirty script to prepare UD data for my different tasks."""

import glob
import os
import random
import re
from xml.etree import ElementTree
from string import punctuation

import jsonlines
import pyconll
from tqdm import tqdm

RAW_UD_DIR = "back/ud/data/raw"
PROCESSED_UD_DIR = "back/ud/data/processed"


def languages_under_threshold(threshold):
    """Return the names of languages with UD corpora totalling at most `threshold` tokens."""
    pattern = os.path.join(RAW_UD_DIR, "**/stats.xml")
    filenames = glob.glob(pattern, recursive=True)
    counts = {}
    for filename in filenames:
        dirname = os.path.split(os.path.split(filename)[0])[1]
        language = re.match(r"UD_(\w+)-\w+", dirname).groups(1)[0]
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        num_tokens = int(root.find("./size/total/tokens").text)
        if language not in counts:
            counts[language] = num_tokens
        else:
            counts[language] += num_tokens
    return sorted([lg for lg, num in counts.items() if num <= threshold])


def conllify(language):
    """Return the CONLL data structures for the corpora in `language`."""
    filenames = []
    corpus_directories = [
        dirname for dirname in os.listdir(RAW_UD_DIR) if language in dirname
    ]
    for dirname in corpus_directories:
        pattern = os.path.join(RAW_UD_DIR, dirname, "*.conllu")
        filenames.extend(glob.glob(pattern))
    return [pyconll.load_from_file(filename) for filename in filenames]


def parse_for_classification(sentence):
    """Return a classification example from `sentence`."""
    for token in sentence:
        if token.deprel == "nsubj":
            try:
                label = next(iter(token.feats["Number"]))
                text = sentence.text
                return {"text": text, "label": label}
            except (StopIteration, KeyError):
                return {}
    return {}


def parse_for_lm(sentence):
    """Return a language modeling example from `sentence`."""
    return sentence.text


def parse_for_pos_tagging(sentence):
    """Return a POS tagging example from `sentence`."""
    try:
        return " ".join([token.form + "/" + token.upos for token in sentence])
    except TypeError:  # if a POS tag is missing
        return ""


def parse_for_translation(sentence):
    try:
        translation = sentence.meta_value("text_en").lower()
        translation = "".join([ch for ch in translation if ch not in punctuation])
        text = sentence.text
        text = "".join([ch for ch in text if ch not in punctuation])
        return text + "\t" + translation
    except KeyError:
        return ""


PARSE_FUNCTIONS = {
    "classification": parse_for_classification,
    "language-modeling": parse_for_lm,
    "pos-tagging": parse_for_pos_tagging,
    "translation": parse_for_translation,
}


def write(lines, filename, task):
    if task == "classification":
        with jsonlines.open(filename, mode="w") as writer:
            writer.write_all(lines)
    else:
        with open(filename, "w") as file:
            file.write("\n".join(lines))


def create_data(language, task, split=0.2):
    conlls = conllify(language)
    parse_fn = PARSE_FUNCTIONS[task]
    examples = []
    for conll in conlls:
        for sentence in conll:
            example = parse_fn(sentence)
            if example:
                examples.append(example)
    random.shuffle(examples)
    n = int(len(examples) * split)
    train, valid = examples[n:], examples[:n]
    if 500 <= len(train) <= 3000:
        path = os.path.join(PROCESSED_UD_DIR, task, language)
        os.makedirs(path, exist_ok=True)
        if task == "classification":
            ext = "jsonl"
        else:
            ext = "txt"
        train_filename = os.path.join(path, f"train.{ext}")
        valid_filename = os.path.join(path, f"valid.{ext}")
        write(train, train_filename, task)
        write(valid, valid_filename, task)
        print(
            f"{len(train)} training and {len(valid)} validation {task} examples for {language}"
        )


if __name__ == "__main__":
    languages = languages_under_threshold(50_000)
    for language in tqdm(languages):
        for task in PARSE_FUNCTIONS:
            create_data(language, task)
