local common = import 'common.libsonnet';

{
  "dataset_reader": {
    "type": "sequence_tagging",
    "word_tag_delimiter": "/",
    "token_indexers": common["token_indexers"]
  },
  "train_data_path": "back/data/pos-tagging/train.txt",
  "model": {
    "type": "simple_tagger",
    "text_field_embedder": common["text_field_embedder"],
    "encoder": common["bidirectional_lstm_encoder"],
  },
  "iterator": common["iterator"],
  "trainer": common["trainer"]
}