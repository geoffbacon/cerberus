local common = import 'common.libsonnet';

{
    "dataset_reader": {
        "type": "simple_language_modeling",
        "tokenizer": common["word_tokenizer"],
        "token_indexers": common["token_indexers"]
    },
    "train_data_path": "back/data/language-modeling/data.txt",
    "model": {
        "type": "language_model",
        "text_field_embedder": common["text_field_embedder"],
        "contextualizer": common["lstm_encoder"],
    },
    "iterator": common["iterator"],
    "trainer": common["trainer"]
}