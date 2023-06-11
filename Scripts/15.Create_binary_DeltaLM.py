import glob
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="gla_Latn")
parser.add_argument("--t", help="echo the string you use here", default="eng_Latn")
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
    os.system(f"python ../../1.spm_data_DeltaLM.py --src {src} --tgt {tgt} --input_dir {filename}")
    os.system(f"bash ../../2.binary_data_DeltaLM.sh {src} {tgt} bpe.DeltaLM.{filename}")

filenames = glob.glob(f"{tgt}-{src}.stanza.*")
for filename in filenames:
    filename = filename.split("/")[-1]
    os.system(f"python ../../1.spm_data_DeltaLM.py --src {tgt} --tgt {src} --input_dir {filename}")
    os.system(f"bash ../../2.binary_data_DeltaLM.sh {tgt} {src} bpe.DeltaLM.{filename}")
