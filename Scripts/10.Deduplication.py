import os
import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="el")
parser.add_argument("--t", help="echo the string you use here", default="en")
parser.add_argument("--dataset", help="echo the string you use here", default="")
parser.add_argument("--rep_num", help="echo the string you use here", default="")
args = parser.parse_args()

src = args.s
tgt = args.t
pair = f"{src}-{tgt}"
dataset = args.dataset
rep_num = args.rep_num

with open(f"data/{pair}/{dataset}/new_train({rep_num}).{src}", 'r') as r1:
    with open(f"data/{pair}/{dataset}/new_train({rep_num}).{tgt}", 'r') as r2:
        cnt = 0
        hex_digs = {}
        with open(f"data/{pair}/{dataset}/new_train({rep_num})_dedup.{src}", 'w') as w1:
            with open(f"data/{pair}/{dataset}/new_train({rep_num})_dedup.{tgt}", 'w') as w2:
                lines2 = r2.readlines()
                for id, text1 in enumerate(r1):
                    cnt += 1
                    if cnt % 100000 == 0:
                        print(cnt)
                    ntext1 = text1.strip().replace("<clean> ","")
                    ntext1 = ntext1.strip().replace("<noisy> ","")
                    hash_object1 = hashlib.md5(ntext1.encode())
                    hex_dig1 = hash_object1.hexdigest()
                    
                    text2 = lines2[id]
                    ntext2 = text2.strip().replace("<clean> ", "")
                    ntext2 = ntext2.strip().replace("<noisy> ", "")
                    hash_object2 = hashlib.md5(ntext2.encode())
                    hex_dig2 = hash_object2.hexdigest()
                    if hex_dig1 in hex_digs and hex_digs[hex_dig1] == hex_dig2:
                        continue
                    else:
                        hex_digs[hex_dig1] = hex_dig2
                        w1.write(f"{text1.strip()}\n")
                        w2.write(f"{text2.strip()}\n")



