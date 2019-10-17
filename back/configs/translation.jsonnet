local common = import 'common.libsonnet';

{
    "dataset_reader": {
        "type": "seq2seq",
        "source_tokenizer": common["word_tokenizer"],
        "target_tokenizer": common["word_tokenizer"],
        "source_token_indexers": common["token_indexers"],
        "target_token_indexers": common["token_indexers"],
        "source_add_start_token": true
    },
    "train_data_path": "back/data/translation/data.txt",
    "model": {
        "type": "simple_seq2seq",
        "source_embedder": common["text_field_embedder"],
        "encoder": common["lstm_encoder"],
        "max_decoding_steps": 100
        # target_namespace
    },
    "iterator": common["iterator"],
    "trainer": common["trainer"]
}