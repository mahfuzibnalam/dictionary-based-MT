import os
import argparse

parser = argparse.ArgumentParser(description="Noises pre-trained MT model.")
parser.add_argument("--s", type=str, required=False, help="The pre-trained model directory.", default="gd")
parser.add_argument("--t", type=str, required=False, help="The pre-trained model directory.", default="en")
args = parser.parse_args()

src = args.s
tgt = args.t
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"

os.system(f"mkdir data/{pair}/alignment")
os.system(f"mkdir data/{pair}/alignment/{src}-{tgt}.stanza.all")

for type in ["train"]:
    with open(f"data/{pair}/alignment/{src}-{tgt}.stanza.all/{type}.alignment", "w") as w:
        with open(f"data/{pair}/stanza.all/old_{type}.{src}" ,"r") as rs:
            linessrc = rs.readlines()
            with open(f"data/{pair}/stanza.all/old_{type}.{tgt}" ,"r") as rt:
                linestgt = rt.readlines()
                for id, linesrc in enumerate(linessrc):
                    sent = f"{linesrc.strip()}    ||| {linestgt[id].strip()}"
                    w.write(f"{sent}\n")

    # os.system(f"CUDA_VISIBLE_DEVICES=0 awesome-align --output_file=data/{pair}/alignment/{src}-{tgt}.stanza.all/{type}.aligned --model_name_or_path=bert-base-multilingual-cased --data_file=data/{pair}/alignment/{src}-{tgt}.stanza.all/{type}.alignment --extraction 'softmax' --batch_size 2")
    os.chdir("/home/mahfuz/research3.7/fast_align/build")
    os.system(f"./fast_align -i /home/mahfuz/Research/MachineTranslation/OPUS/data/{pair}/alignment/{src}-{tgt}.stanza.all/{type}.alignment -d -o -v > /home/mahfuz/Research/MachineTranslation/OPUS/data/{pair}/alignment/{src}-{tgt}.stanza.all/{type}.aligned")