# Common configuration settings across tasks
# Note that this is not a valid config file by itself, it simply holds reused settings.
# The following global variables exist because either they need to appear in multiple 
# locations with the same value, or they're often modified so it's handy to have them up.
local TOKEN_EMBEDDING_DIM = 50;
local CHAR_EMBEDDING_DIM = 8;
local USE_GPU = false;
local NUM_EPOCHS = 3;

{
    "iterator": {
        "type": "basic",
        "batch_size": 32
    },
    "trainer": {
        "optimizer": {
            "type": "adam"
            },
        "num_epochs": NUM_EPOCHS,
        "patience": std.max(std.floor(NUM_EPOCHS / 10), 1),
        "cuda_device": if USE_GPU then 0 else -1,
        "shuffle": true,
        "num_serialized_models_to_keep": 1
    },
    "text_field_embedder": {
        "type": "basic",
        "token_embedders": {
            "tokens": {
                "type": "embedding",
                "embedding_dim": TOKEN_EMBEDDING_DIM,
                "trainable": true
            },
            "token_characters": {
                "type": "character_encoding",
                "embedding": {
                    "embedding_dim": CHAR_EMBEDDING_DIM,
                    "trainable": true
                },
                "encoder": $["character_lstm_encoder"],
                "dropout": 0.1
            }
        }
    },
    "token_indexers": {
        "tokens": {
            "type": "single_id",
            "lowercase_tokens": true
        },
        "token_characters": {
            "type": "characters",
            "min_padding_length": 1
        },
    },
    "input_size": TOKEN_EMBEDDING_DIM + $["character_lstm_encoder"]["hidden_size"],
    "word_tokenizer": {
        "type": "word",
        "word_splitter": {
            "type": "just_spaces"
        },
        "word_filter": {
            "type": "pass_through"
        },
        "word_stemmer": {
            "type": "pass_through"
        }
    },
    "character_tokenizer": {
        "type": "character"
    },
    "character_lstm_encoder": {
        "type": "lstm",
        "input_size": CHAR_EMBEDDING_DIM,
        "hidden_size": CHAR_EMBEDDING_DIM,
        "num_layers": 1,
        "bidirectional": false
    },
    "lstm_encoder": {
        "type": "lstm",
        "input_size": $["input_size"],
        "hidden_size": 100,
        "num_layers": 1,
        "bidirectional": false
    },
    "bidirectional_lstm_encoder": {
        "type": "lstm",
        "input_size": $["input_size"],
        "hidden_size": 100,
        "num_layers": 2,
        "dropout": 0.5,
        "bidirectional": true
    }
}