import glob
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="el")
parser.add_argument("--t", help="echo the string you use here", default="en")
args = parser.parse_args()

src = args.s
tgt = args.t
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"
os.chdir(f"data/{pair}")

filenames = glob.glob(f"{src}-{tgt}.stanza.*")
for filename in filenames:
    filename = filename.split("/")[-1]
    os.system(f"bash ../../1.spm_data.sh {src} {tgt} {filename}")
    os.system(f"bash ../../2.binary_data.sh {src} {tgt} bpe.{filename}")

filenames = glob.glob(f"{tgt}-{src}.stanza.*")
for filename in filenames:
    filename = filename.split("/")[-1]
    os.system(f"bash ../../1.spm_data.sh {tgt} {src} {filename}")
    os.system(f"bash ../../2.binary_data.sh {tgt} {src} bpe.{filename}")
    