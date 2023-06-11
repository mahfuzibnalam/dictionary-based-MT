import os
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="kmr")
parser.add_argument("--t", help="echo the string you use here", default="en")
args = parser.parse_args()

src = args.s
tgt = args.t
pair = f"{src}-{tgt}"

actualsize = [5000, 10000, 50000, 100000, 200000]
beautysize = ["5K", "10K", "50K", "100K", "200K"]

with open(f"data/{pair}/alignment/{pair}.stanza.all/train.alignment", "r") as ralignment:
    with open(f"data/{pair}/alignment/{pair}.stanza.all/train.aligned", "r") as raligned:
        with open(f"data/{pair}/stanza.all/old_train.{src}", "r") as rs:
            with open(f"data/{pair}/stanza.all/old_train.{tgt}", "r") as rt:
                srclines = rs.readlines()
                tgtlines = rt.readlines()
                alignments = ralignment.readlines()
                aligneds = raligned.readlines()
                for index, size in enumerate(actualsize):
                    random.seed(42)
                    randomindexes = random.sample(range(len(srclines)), size)
                    os.system(f"mkdir data/{pair}/stanza.{beautysize[index]}")
                    os.system(f"mkdir data/{pair}/alignment/{pair}.stanza.{beautysize[index]}")
                    with open(f"data/{pair}/stanza.{beautysize[index]}/old_train.{src}", "w") as ws:
                        with open(f"data/{pair}/stanza.{beautysize[index]}/old_train.{tgt}", "w") as wt:
                            with open(f"data/{pair}/alignment/{pair}.stanza.{beautysize[index]}/train.alignment", "w") as walignment:
                                with open(f"data/{pair}/alignment/{pair}.stanza.{beautysize[index]}/train.aligned", "w") as waligned:
                                    for randomindex in randomindexes:
                                        ws.write(srclines[randomindex])
                                        wt.write(tgtlines[randomindex])
                                        walignment.write(alignments[randomindex])
                                        waligned.write(aligneds[randomindex])
                    
                    os.system(f"cp data/{pair}/stanza.all/old_test.{src} data/{pair}/stanza.{beautysize[index]}/old_test.{src}")
                    os.system(f"cp data/{pair}/stanza.all/old_test.{tgt} data/{pair}/stanza.{beautysize[index]}/old_test.{tgt}")
                    os.system(f"cp data/{pair}/stanza.all/old_valid.{src} data/{pair}/stanza.{beautysize[index]}/old_valid.{src}")
                    os.system(f"cp data/{pair}/stanza.all/old_valid.{tgt} data/{pair}/stanza.{beautysize[index]}/old_valid.{tgt}")

