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
args = parser.parse_args()

src = args.s
tgt = args.t
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"
dataset = args.dataset
actualsize = [5000, 5000, 40000, 50000, 100000]
beautysize = ["5K", "10K", "50K", "100K", "200K"]
if os.path.exists(f"data/{pair}/{dataset}"):
    os.chdir(f"data/{pair}/{dataset}")
    srces = []
    tgts = []
    srcesbas = []
    tgtsbas = []
    for index in range(0,5):
        size = actualsize[index]
        with open(f"sorted({beautysize[index]}).{src}", "r") as rs:
            with open(f"sorted({beautysize[index]}).{tgt}", "r") as rt:
                srclines = rs.readlines()
                tgtlines = rt.readlines()
                for id in range(len(srces), len(srces) + size):
                    srces.append(srclines[id])
                    tgts.append(tgtlines[id])
                with open(f"new_train({beautysize[index]}).{src}", "w") as ws:
                    with open(f"new_train({beautysize[index]}).{tgt}", "w") as wt:
                        for id in range(len(srces)):
                            ws.write(srces[id])
                            wt.write(tgts[id])
        os.system(f"cat new_train\({beautysize[index]}\).{src} tagged_train.{src} > new_train\({beautysize[index]}\)_unshuf.{src}")
        os.system(f"cat new_train\({beautysize[index]}\).{tgt} tagged_train.{tgt} > new_train\({beautysize[index]}\)_unshuf.{tgt}")
        with open(f"new_train({beautysize[index]})_unshuf.{tgt}", "r") as rt:
            with open(f"new_train({beautysize[index]})_unshuf.{src}", "r") as rs:
                with open(f"new_train({beautysize[index]})_unshuf.both", "w") as w:
                    linest = rt.read().splitlines()
                    liness = rs.read().splitlines()
                    for id, srcline in enumerate(liness):
                        tgtline = linest[id]
                        w.write(f"{tgtline}|||{srcline}\n")
        os.system(f"shuf new_train\({beautysize[index]}\)_unshuf.both > new_train\({beautysize[index]}\)_shuf.both")

        with open(f"new_train({beautysize[index]})_shuf.both", "r") as r:
            with open(f"train({beautysize[index]}).{tgt}", "w") as wt:
                with open(f"train({beautysize[index]}).{src}", "w") as ws:
                    lines = r.read().splitlines()
                    for line in lines:
                        tgtline = line.split("|||")[0]
                        srcline = line.split("|||")[1]
                        ws.write(f"{srcline}\n")
                        wt.write(f"{tgtline}\n")