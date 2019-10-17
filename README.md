# Cerberus

### What is Cerberus?

Cerberus is an app that reduces the annotation burden of linguists. It does this by making it easy for linguists to apply state-of-the-art natural language processing models to their data. Given some initial data, these models learn to perform linguistic annotation tasks themselves. They can then automatically perform those tasks on a much larger dataset, reducing the manual labour of a linguist. The models are not perfect and are designed to help bootstrap a linguistic project.

Cerberus currently supports the following tasks:

- **POS tagging**: Assigning a syntactic category to each word.
- **Translation**: Automatically translating from one language to another.
- **Classification**: Assigning a user-defined label to a word, sentence or paragraph.

Coming soon:

- **Spelling correction**: Correcting misspelt words.
- **Morphological analysis**: Assigning morphosyntactic features to each word.
- **Language modeling**: Generating grammatical sentences.

Cerberus is built on top of [AllenNLP](https://allennlp.org/) and [Streamlit](https://streamlit.io/).