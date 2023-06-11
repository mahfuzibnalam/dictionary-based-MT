import os
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="el")
parser.add_argument("--t", help="echo the string you use here", default="en")
parser.add_argument("--dataset", help="echo the string you use here", default="stanza.100K")
args = parser.parse_args()

src = args.s
tgt = args.t
pair = f"{src}-{tgt}"
dataset = args.dataset

actualsize = [5000, 10000, 50000, 100000, 200000]
beautysize = ["5K", "10K", "50K", "100K", "200K"]

if not os.path.exists(f"data/{pair}/{dataset}/new_train({1})_dedup.{src}"):
    os.system(f"python 9.OPUS_modification.py --dataset {dataset} --rep_num {1}")
    os.system(f"python 10.Deduplication.py --dataset {dataset} --rep_num {1}")
with open(f"data/{pair}/{dataset}/new_train({1})_dedup.{src}", "r") as r:
    initlength = math.ceil(len(r.readlines()) * 0.75)

ind = 0
i = math.ceil(actualsize[ind] / initlength)
while 1:
    if not os.path.exists(f"data/{pair}/{dataset}/new_train({i})_dedup.{src}"):
        os.system(f"python 9.OPUS_modification.py --dataset {dataset} --rep_num {i}")
        os.system(f"python 10.Deduplication.py --dataset {dataset} --rep_num {i}")
    with open(f"data/{pair}/{dataset}/new_train({i})_dedup.{src}", "r") as r:
        length = len(r.readlines())
    if length > actualsize[ind]:
        os.system(f"cp data/{pair}/{dataset}/new_train\({i}\)_dedup.{src} data/{pair}/{dataset}/new_train\({beautysize[ind]}\)_dedup.{src}")
        os.system(f"cp data/{pair}/{dataset}/new_train\({i}\)_dedup.{tgt} data/{pair}/{dataset}/new_train\({beautysize[ind]}\)_dedup.{tgt}")
        ind += 1
    if ind == 6:
        break
    initlength = math.ceil((length / i) * 0.75)
    i = math.ceil(actualsize[ind] / initlength)


