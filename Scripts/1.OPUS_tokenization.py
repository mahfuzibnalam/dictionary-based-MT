import os
import stanza
import argparse
from numpy import append

parser = argparse.ArgumentParser(description="Noises pre-trained MT model.")
parser.add_argument("--s", type=str, required=False, help="The pre-trained model directory.", default="en")
parser.add_argument("--t", type=str, required=False, help="The pre-trained model directory.", default="kmr")
args = parser.parse_args()

src = args.s
tgt = args.t
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"

nlpsrc = stanza.Pipeline(lang=src, processors='tokenize')
nlptgt = stanza.Pipeline(lang=tgt, processors='tokenize')

os.system(f"mkdir data/{pair}/stanza.all")

for type in ["dev", "test", "train"]:
    with open(f"data/{pair}/opus.{pair}-{type}.{src}" ,"r") as rs:
        with open(f"data/{pair}/opus.{pair}-{type}.{tgt}" ,"r") as rt:
            if type == "dev":
                type = "valid"
            with open(f"data/{pair}/stanza.all/old_{type}.{src}" ,"w") as w:
                for line in rs:
                    doc = nlpsrc(line)
                    tokens = []
                    for i, sentence in enumerate(doc.sentences):
                        for token in sentence.tokens:
                            tokens.append(token.text)
                        sent = " ".join(tokens)
                    w.write(f"{sent}\n")

            with open(f"data/{pair}/stanza.all/old_{type}.{tgt}" ,"w") as w:
                for line in rt:
                    doc = nlptgt(line)
                    tokens = []
                    for i, sentence in enumerate(doc.sentences):
                        for token in sentence.tokens:
                            tokens.append(token.text)
                        sent = " ".join(tokens)
                    w.write(f"{sent}\n")
