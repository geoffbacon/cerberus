"""Streamlit front end of Cerberus."""

import re
from itertools import cycle

import streamlit as st
from slugify import slugify
from spacy.displacy.render import EntityRenderer

from models import TASKS, get_metrics, is_trained, load_labels, predict, train

TASKS = ["Home"] + TASKS[:]
TRAINED_MODEL_MESSAGE = "You've got a trained model"
NO_TRAINED_MODEL_MESSAGE = "You haven't trained a model yet"
TRAINING_MESSAGE = "Training..."


def main():
    """This function is called after every user interaction."""
    task = st.sidebar.selectbox("Task", TASKS, 0)
    if task == "Home":
        home()
    else:
        run(task)


def home():
    """Display the home screen."""
    with open("front/home.md") as file:
        text = file.read()
    st.markdown(text, unsafe_allow_html=True)


def run(task):
    """Run the train/predict flow for `task`."""
    st.markdown(f'<h1 align="center">{task}</h1>', unsafe_allow_html=True)
    train_button = st.sidebar.button("Train")
    sidebar_train_message = st.sidebar.empty()
    main_train_message = st.empty()
    slug = slugify(task)
    trained = is_trained(slug)
    if trained:
        sidebar_train_message.success(TRAINED_MODEL_MESSAGE)
    else:
        sidebar_train_message.warning(NO_TRAINED_MODEL_MESSAGE)
        main_train_message.warning(NO_TRAINED_MODEL_MESSAGE)
    if train_button:
        sidebar_train_message.info(TRAINING_MESSAGE)
        main_train_message.info(TRAINING_MESSAGE)
        train(slug, sidebar_train_message, TRAINING_MESSAGE)
        sidebar_train_message.success(TRAINED_MODEL_MESSAGE)
        main_train_message.empty()
        trained = is_trained(slug)
    if trained:
        show_metrics = st.sidebar.checkbox("Show metrics")
        if show_metrics:
            metrics = get_metrics(slug)
            for key, value in metrics.items():
                st.sidebar.text(f"{key}: {value}")
        user_input = st.text_area("Input")
        st.text("Output")
        if user_input:
            output = predict(slug, user_input)
            display_function = DISPLAY_FUNCTIONS[slug]
            display_function(output)


def display_translation(output):
    """Render the `output` of a translation model on the screen."""
    tokens = output["predicted_tokens"]
    st.markdown(" ".join(tokens))


def display_with_displacy(text, labels, tags=None):
    """Render `text` with `labels` highlighted through spaCy's excellent displaCy."""
    if not tags:
        tags = labels
    COLORS = list(EntityRenderer().colors.values())
    colors = {label: color for label, color in zip(labels, cycle(COLORS))}
    options = {"ents": labels, "colors": colors}
    renderer = EntityRenderer(options=options)
    pattern = re.compile(r"[^ ]+")
    matches = pattern.finditer(text)
    spans = [
        {"label": tag, "start": m.start(), "end": m.end()}
        for tag, m in zip(tags, matches)
    ]
    html = renderer.render_ents(text, spans, title=None)
    # without the following line the tags are all squished up and the
    # first tag is all by itself. Unsure though why this fixes it.
    html = re.sub(r"\s+", " ", html)
    st.markdown(html, unsafe_allow_html=True)


def display_classification(output):
    """Render the `output` of a classification model on the screen.
    
    This makes use of the excellent visualization tools in spaCy's dispaCy.
    """
    probabilities = output["probs"]
    probabilities = [f"{round(p * 100, 1)}%" for p in probabilities]
    text = " ".join(probabilities)
    labels = [label.upper() for label in load_labels("classification")]
    display_with_displacy(text, labels)


def display_pos(output):
    """Render the `output` of a POS tagging model on the screen.
    
    This makes use of the excellent visualization tools in spaCy's dispaCy.
    """
    tokens = output["words"]
    text = " ".join(tokens)
    tags = [tag.upper() for tag in output["tags"]]
    labels = [label.upper() for label in load_labels("pos-tagging")]
    display_with_displacy(text, labels, tags)


DISPLAY_FUNCTIONS = {
    "pos-tagging": display_pos,
    "translation": display_translation,
    "classification": display_classification,
}


if __name__ == "__main__":
    main()
