import os
import argparse
from pathlib import Path
from tokenizers import ByteLevelBPETokenizer

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="hy")
parser.add_argument("--t", help="echo the string you use here", default="en")
args = parser.parse_args()

src = args.s
tgt = args.t
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"

os.system(f"mkdir data/{pair}/tokenizers")
for dataset in ["stanza.5K", "stanza.10K", "stanza.50K", "stanza.100K", "stanza.200K", "stanza.all"]:
    if os.path.exists(f"data/{pair}/{dataset}"):
        paths = [str(x) for x in Path(f"data/{pair}/{dataset}/").glob(f"**/old_train.{src}")]

        tokenizer = ByteLevelBPETokenizer()

        tokenizer.train(files=paths, vocab_size=5_000, min_frequency=2, special_tokens=[
            "<|endoftext|>",
        ])

        os.system(f"mkdir data/{pair}/tokenizers/{dataset}.{src}")
        tokenizer.save_model(f"data/{pair}/tokenizers/{dataset}.{src}", "")

        os.system(f"mv data/{pair}/tokenizers/{dataset}.{src}/-vocab.json data/{pair}/tokenizers/{dataset}.{src}/vocab.json")
        os.system(f"mv data/{pair}/tokenizers/{dataset}.{src}/-merges.txt data/{pair}/tokenizers/{dataset}.{src}/merges.txt")
        os.system(f"cp data/tokenizers/config.json data/{pair}/tokenizers/{dataset}.{src}/config.json")

        paths = [str(x) for x in Path(f"data/{pair}/{dataset}/").glob(f"**/old_train.{tgt}")]

        tokenizer = ByteLevelBPETokenizer()

        tokenizer.train(files=paths, vocab_size=5_000, min_frequency=2, special_tokens=[
            "<|endoftext|>",
        ])

        os.system(f"mkdir data/{pair}/tokenizers/{dataset}.{tgt}")
        tokenizer.save_model(f"data/{pair}/tokenizers/{dataset}.{tgt}", "")

        os.system(f"mv data/{pair}/tokenizers/{dataset}.{tgt}/-vocab.json data/{pair}/tokenizers/{dataset}.{tgt}/vocab.json")
        os.system(f"mv data/{pair}/tokenizers/{dataset}.{tgt}/-merges.txt data/{pair}/tokenizers/{dataset}.{tgt}/merges.txt")
        os.system(f"cp data/tokenizers/config.json data/{pair}/tokenizers/{dataset}.{tgt}/config.json")


        os.system(f"cp data/{pair}/{dataset}/old_train.{src} data/{pair}/{dataset}/old_train.{src}.txt")
        os.system(f"cp data/{pair}/{dataset}/old_valid.{src} data/{pair}/{dataset}/old_valid.{src}.txt")
        os.system(f"cp data/{pair}/{dataset}/old_train.{tgt} data/{pair}/{dataset}/old_train.{tgt}.txt")
        os.system(f"cp data/{pair}/{dataset}/old_valid.{tgt} data/{pair}/{dataset}/old_valid.{tgt}.txt")
        
        os.system(f"mkdir models/{pair}")
        os.system(f"bash 5.train_GPT2.sh data/{pair}/{dataset}/old_train.{src}.txt data/{pair}/{dataset}/old_valid.{src}.txt data/{pair}/tokenizers/{dataset}.{src} models/{pair}/{dataset}.{src}/")
        os.system(f"bash 5.train_GPT2.sh data/{pair}/{dataset}/old_train.{tgt}.txt data/{pair}/{dataset}/old_valid.{tgt}.txt data/{pair}/tokenizers/{dataset}.{tgt} models/{pair}/{dataset}.{tgt}/")