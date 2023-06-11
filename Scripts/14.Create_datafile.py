import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="el")
parser.add_argument("--t", help="echo the string you use here", default="en")
args = parser.parse_args()

src = args.s
tgt = args.t
pair = f"{src}-{tgt}"

for dataset in ["stanza.5K", "stanza.10K", "stanza.50K", "stanza.100K", "stanza.200K"]:
    if os.path.exists(f"data/{pair}/{dataset}"):
        os.system(f"mkdir data/{pair}/{src}-{tgt}.{dataset}.0K")
        os.system(f"cp data/{pair}/{dataset}/old_test.{tgt} data/{pair}/{src}-{tgt}.{dataset}.0K/test.{tgt}")
        os.system(f"cp data/{pair}/{dataset}/old_test.{src} data/{pair}/{src}-{tgt}.{dataset}.0K/test.{src}")
        os.system(f"cp data/{pair}/{dataset}/old_train.{tgt} data/{pair}/{src}-{tgt}.{dataset}.0K/train.{tgt}")
        os.system(f"cp data/{pair}/{dataset}/old_train.{src} data/{pair}/{src}-{tgt}.{dataset}.0K/train.{src}")
        os.system(f"cp data/{pair}/{dataset}/old_valid.{tgt} data/{pair}/{src}-{tgt}.{dataset}.0K/valid.{tgt}")
        os.system(f"cp data/{pair}/{dataset}/old_valid.{src} data/{pair}/{src}-{tgt}.{dataset}.0K/valid.{src}")

        os.system(f"mkdir data/{pair}/{tgt}-{src}.{dataset}.0K")
        os.system(f"cp data/{pair}/{dataset}/old_test.{tgt} data/{pair}/{tgt}-{src}.{dataset}.0K/test.{tgt}")
        os.system(f"cp data/{pair}/{dataset}/old_test.{src} data/{pair}/{tgt}-{src}.{dataset}.0K/test.{src}")
        os.system(f"cp data/{pair}/{dataset}/old_train.{tgt} data/{pair}/{tgt}-{src}.{dataset}.0K/train.{tgt}")
        os.system(f"cp data/{pair}/{dataset}/old_train.{src} data/{pair}/{tgt}-{src}.{dataset}.0K/train.{src}")
        os.system(f"cp data/{pair}/{dataset}/old_valid.{tgt} data/{pair}/{tgt}-{src}.{dataset}.0K/valid.{tgt}")
        os.system(f"cp data/{pair}/{dataset}/old_valid.{src} data/{pair}/{tgt}-{src}.{dataset}.0K/valid.{src}")
        actualsize = [5000, 10000, 50000, 100000, 200000]
        beautysize = ["5K", "10K", "50K", "100K", "200K"]

        for size in beautysize:
            os.system(f"mkdir data/{pair}/{src}-{tgt}.{dataset}.{size}")
            os.system(f"mkdir data/{pair}/{tgt}-{src}.{dataset}.{size}")
            for typ in ["train", "test", "valid"]:
                if typ == "train":
                    with open(f"data/{pair}/{dataset}/train({size}).{src}", "r") as rs:
                        with open(f"data/{pair}/{dataset}/train({size}).{tgt}", "r") as rt:
                            srclines = rs.readlines()
                            tgtlines = rt.readlines()
                            
                            with open(f"data/{pair}/{src}-{tgt}.{dataset}.{size}/train.{src}", "w") as wsts:
                                with open(f"data/{pair}/{src}-{tgt}.{dataset}.{size}/train.{tgt}", "w") as wstt:
                                    with open(f"data/{pair}/{tgt}-{src}.{dataset}.{size}/train.{src}", "w") as wtss:
                                        with open(f"data/{pair}/{tgt}-{src}.{dataset}.{size}/train.{tgt}", "w") as wtst:
                                            for index, _ in enumerate(tgtlines):
                                                srcline = srclines[index]
                                                tgtline = tgtlines[index]
                                                wsts.write(srcline)
                                                wtst.write(tgtline)
                                                srcline = srcline.replace("<clean> ","")
                                                srcline = srcline.replace("<noisy> ","")
                                                tgtline = tgtline.replace("<clean> ","")
                                                tgtline = tgtline.replace("<noisy> ","")
                                                wstt.write(tgtline)
                                                wtss.write(srcline)
                else:
                    with open(f"data/{pair}/{dataset}/tagged_{typ}.{src}", "r") as rs:
                        with open(f"data/{pair}/{dataset}/tagged_{typ}.{tgt}", "r") as rt:
                            srclines = rs.readlines()
                            tgtlines = rt.readlines()
                            
                            with open(f"data/{pair}/{src}-{tgt}.{dataset}.{size}/{typ}.{src}", "w") as wsts:
                                with open(f"data/{pair}/{src}-{tgt}.{dataset}.{size}/{typ}.{tgt}", "w") as wstt:
                                    with open(f"data/{pair}/{tgt}-{src}.{dataset}.{size}/{typ}.{src}", "w") as wtss:
                                        with open(f"data/{pair}/{tgt}-{src}.{dataset}.{size}/{typ}.{tgt}", "w") as wtst:
                                            for index, _ in enumerate(tgtlines):
                                                srcline = srclines[index]
                                                tgtline = tgtlines[index]
                                                wsts.write(srcline)
                                                wtst.write(tgtline)
                                                srcline = srcline.replace("<clean> ","")
                                                srcline = srcline.replace("<noisy> ","")
                                                tgtline = tgtline.replace("<clean> ","")
                                                tgtline = tgtline.replace("<noisy> ","")
                                                wstt.write(tgtline)
                                                wtss.write(srcline)
