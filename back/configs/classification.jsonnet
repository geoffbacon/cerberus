local common = import 'common.libsonnet';

{
    "dataset_reader": {
        "type": "text_classification_json",
        "tokenizer": common["word_tokenizer"],
        "token_indexers": common["token_indexers"]
    },
    "train_data_path": "back/data/classification/data.jsonl",
    "model": {
        "type": "basic_classifier",
        "text_field_embedder": common["text_field_embedder"],
        "seq2vec_encoder": common["bidirectional_lstm_encoder"]
    },
    "iterator": common["iterator"],
    "trainer": common["trainer"]
}