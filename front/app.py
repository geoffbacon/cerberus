"""Streamlit front end of Cerberus."""

import streamlit as st
from slugify import slugify

from models import TASKS, get_metrics, is_trained, predict, train

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
    st.text(" ".join(tokens))


def display_classification(output):
    """Render the `output` of a translation model on the screen."""
    probabilities = output["probs"]
    p = round(max(probabilities) * 100, 1)
    label = output["label"]
    st.text(label)
    st.text(f"Probability: {p}%")


def display_pos(output):
    """Render the `output` of a POS tagging model on the screen."""
    tokens = output["words"]
    tags = output["tags"]
    for token, tag in zip(tokens, tags):
        st.text(f"{token}: {tag}")


DISPLAY_FUNCTIONS = {
    "pos-tagging": display_pos,
    "translation": display_translation,
    "classification": display_classification,
}


if __name__ == "__main__":
    main()
