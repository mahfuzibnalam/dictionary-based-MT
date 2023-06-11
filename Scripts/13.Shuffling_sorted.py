import os
import math
import torch
import argparse
import numpy as np
from transformers import GPT2Tokenizer, GPT2LMHeadModel

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="el")
parser.add_argument("--t", help="echo the string you use here", default="en")
parser.add_argument("--dataset", help="echo the string you use here", default="stanza.100K")
parser.add_argument("--index", help="echo the string you use here", default="0")
args = parser.parse_args()

src = args.s
tgt = args.t
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"
dataset = args.dataset
index = (int)(args.index)
beautysize = ["5K", "10K", "50K", "100K", "200K"]

def score(sentence, model, tokenizer):
    tokenize_input = tokenizer.encode(sentence)
    if len(tokenize_input) > 1024:
        return float('inf')
    else:
        tensor_input = torch.tensor([tokenize_input])
        loss = model(tensor_input, labels=tensor_input)[0]
        return np.exp(loss.detach().numpy())

def topindexes(srclines, tgtlines, dataset):
    with torch.no_grad():
        srcmodel = GPT2LMHeadModel.from_pretrained(f'/home/mahfuz/Research/MachineTranslation/OPUS/models/{pair}/{dataset}.{src}')
        srcmodel.eval()

    with torch.no_grad():
        tgtmodel = GPT2LMHeadModel.from_pretrained(f'/home/mahfuz/Research/MachineTranslation/OPUS/models/{pair}/{dataset}.{tgt}')
        tgtmodel.eval()

    srctokenizer = GPT2Tokenizer.from_pretrained(f'/home/mahfuz/Research/MachineTranslation/OPUS/models/{pair}/{dataset}.{src}')
    tgttokenizer = GPT2Tokenizer.from_pretrained(f'/home/mahfuz/Research/MachineTranslation/OPUS/models/{pair}/{dataset}.{tgt}')
    
    scores = {}
    for id, _ in enumerate(srclines):
        srcline = srclines[id]
        tgtline = tgtlines[id]
        srcline = srcline.strip().replace("<noisy> ", "")
        tgtline = tgtline.strip().replace("<noisy> ", "")
        if srcline.strip() != '' and tgtline.strip() != '':
            srcprep = score(srcline, srcmodel, srctokenizer)
            tgtprep = score(tgtline, tgtmodel, tgttokenizer)
            prep = srcprep + tgtprep
            scores[id] = prep

    scores = dict(sorted(scores.items(), key=lambda item: item[1]))
    return scores

if os.path.exists(f"data/{pair}/{dataset}"):
    os.chdir(f"data/{pair}/{dataset}")
    with open(f"new_train({beautysize[index]})_dedup.{src}", "r") as rs:
        with open(f"new_train({beautysize[index]})_dedup.{tgt}", "r") as rt:
            srclines = rs.readlines()
            tgtlines = rt.readlines()
            scores = topindexes(srclines, tgtlines, dataset)
            with open(f"sorted({beautysize[index]}).{src}", "w") as ws:
                with open(f"sorted({beautysize[index]}).{tgt}", "w") as wt:
                        for id in scores.keys():
                            ws.write(srclines[id])
                            wt.write(tgtlines[id])

