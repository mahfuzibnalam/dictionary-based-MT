import os
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="kk")
parser.add_argument("--t", help="echo the string you use here", default="en")
parser.add_argument("--s3", help="echo the string you use here", default="kaz")
parser.add_argument("--t3", help="echo the string you use here", default="eng")
parser.add_argument("--dataset", help="echo the string you use here", default="stanza.all")
args = parser.parse_args()

src = args.s
tgt = args.t
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"
dataset = args.dataset

actualsize = [5000, 10000, 50000, 100000, 200000]
beautysize = ["5K", "10K", "50K", "100K", "200K"]

if not os.path.exists(f"data/{pair}/{dataset}/new_train({1})_dedup.{src}"):
    os.system(f"python 9.OPUS_modification_baseline.py --s {args.s} --t {args.t} --s3 {args.s3} --t3 {args.t3} --dataset {dataset} --rep_num 1")
    os.system(f"python 10.Deduplication_baseline.py --s {args.s} --t {args.t} --dataset {dataset} --rep_num 1")
with open(f"data/{pair}/{dataset}/new_train({1})_dedup.{src}", "r") as r:
    initlength = math.ceil(len(r.readlines()) * 0.75)

ind = 0
i = math.ceil(actualsize[ind] / initlength)
while 1:
    if not os.path.exists(f"data/{pair}/{dataset}/new_train({i})_dedup.{src}"):
        os.system(f"python 9.OPUS_modification_baseline.py --s {args.s} --t {args.t} --s3 {args.s3} --t3 {args.t3} --dataset {dataset} --rep_num {i}")
        os.system(f"python 10.Deduplication_baseline.py --s {args.s} --t {args.t} --dataset {dataset} --rep_num {i}")
    with open(f"data/{pair}/{dataset}/new_train({i})_dedup.{src}", "r") as r:
        length = len(r.readlines())
    if length > actualsize[ind]:
        os.system(f"cp data/{pair}/{dataset}/new_train\({i}\)_dedup.{src} data/{pair}/{dataset}/new_train\({beautysize[ind]}\)_dedup.{src}")
        os.system(f"cp data/{pair}/{dataset}/new_train\({i}\)_dedup.{tgt} data/{pair}/{dataset}/new_train\({beautysize[ind]}\)_dedup.{tgt}")
        os.system(f"cp data/{pair}/{dataset}/new_train\({i}\)_dedup_bas.{src} data/{pair}/{dataset}/new_train\({beautysize[ind]}\)_dedup_bas.{src}")
        os.system(f"cp data/{pair}/{dataset}/new_train\({i}\)_dedup_bas.{tgt} data/{pair}/{dataset}/new_train\({beautysize[ind]}\)_dedup_bas.{tgt}")
        ind += 1
    if ind == 5:
        break
    initlength = math.ceil((length / i) * 0.75)
    i = math.ceil(actualsize[ind] / initlength)


