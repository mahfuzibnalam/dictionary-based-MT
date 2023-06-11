import os
import argparse
import sentencepiece as spm


parser = argparse.ArgumentParser()
parser.add_argument("--src", help="echo the string you use here", default="")
parser.add_argument("--tgt", help="echo the string you use here", default="")
parser.add_argument("--input_dir", help="echo the string you use here", default="")
args = parser.parse_args()

src=args.src
tgt=args.tgt
input_dir=args.input_dir

bpe_dir=f"bpe.DeltaLM.{input_dir}"
spmmodel="/home/mahfuz/Research/MachineTranslation/DeltaLM/models/multi/spm/spm.model"

os.system(f"mkdir -p {bpe_dir}")
os.system(f"mv {input_dir}/*valid.{src} {input_dir}/valid.{src}")
os.system(f"mv {input_dir}/*valid.{tgt} {input_dir}/valid.{tgt}")
os.system(f"mv {input_dir}/*train.{src} {input_dir}/train.{src}")
os.system(f"mv {input_dir}/*train.{tgt} {input_dir}/train.{tgt}")
os.system(f"mv {input_dir}/*test.{src} {input_dir}/test.{src}")
os.system(f"mv {input_dir}/*test.{tgt} {input_dir}/test.{tgt}")

sp = spm.SentencePieceProcessor(model_file=spmmodel)

for typ in ["train", "test", "valid"]:
    with open(f"{input_dir}/{typ}.{src}", 'r') as r:
        with open(f'{bpe_dir}/{typ}.{src}', 'w') as w:
            lines = r.readlines()
            for line in lines:
                line = line.strip()
                segments = sp.encode(line, out_type=str)
                segment = " ".join(segments[0:511])
                w.write(f"{segment}\n")

    with open(f"{input_dir}/{typ}.{tgt}", 'r') as r:
        with open(f'{bpe_dir}/{typ}.{tgt}', 'w') as w:
            lines = r.readlines()
            for line in lines:
                line = line.strip()
                segments = sp.encode(line, out_type=str)
                segment = " ".join(segments[0:511])
                w.write(f"{segment}\n")