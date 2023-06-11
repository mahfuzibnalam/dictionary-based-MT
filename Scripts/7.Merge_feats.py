import os
import glob
import pickle
import argparse

parser = argparse.ArgumentParser(description="Noises pre-trained MT model.")
parser.add_argument("--s", type=str, required=False, help="The pre-trained model directory.", default="kmr")
parser.add_argument("--t", type=str, required=False, help="The pre-trained model directory.", default="en")
args = parser.parse_args()

src = args.s
tgt = args.t
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"

folder_name = f"panlex.{src}-{tgt}_form"

os.system(f"mkdir data/{pair}/panlex.{src}-{tgt}_form")

def get_feats_dictionaries():
    dict_src = {}
    dict_tgt = {}

    filenames = glob.glob(f"data/{pair}/{folder_name}.old/*.txt")
    for filename in filenames:
        if ".feats_" in filename:
            with open(filename, "r") as r:
                filename = filename.split("/")[-1]
                components = filename.split(".")
                type = components[0]
                name = components[1].split("_")[1]
                if type == src:
                    dict_src[name] = r.read().splitlines()
                else:
                    dict_tgt[name] = r.read().splitlines()
    
    return dict_src, dict_tgt

def get_vocab(filename):
    with open(filename, 'rb') as r:
        translation = pickle.load(r)
    return translation

def check_feat(feat):
    feats = feat.split(";")
    for un_feat in un_to_ud:
        un_feats = un_feat.split(";")
        found = True
        if len(feats) == len(un_feats):
            for element in un_feats:
                if element not in feats:
                    found = False
                    break
        else:
            found = False
        
        if found:
            return un_to_ud[un_feat]
    return None

mess_to_clean = {}
feats_dict_src, feats_dict_tgt = get_feats_dictionaries()
un_to_ud = get_vocab(f"data/{pair}/vocab/stanza.all.un-ud.pkl")

new_dict_src = {}
new_dict_tgt = {}

for feat in feats_dict_src:
    if "|" in feat:
        new_dict_src[feat] = feats_dict_src[feat]
    if ";" in feat:
        un_feat = ";".join(feat.split(";")[1:])
        ud_feat = check_feat(un_feat)
        if ud_feat:
            ud_feat = un_to_ud[feat.split(";")[0]]+ "|" + ud_feat
            if ud_feat not in new_dict_src:
                new_dict_src[ud_feat] = feats_dict_src[feat]
            else:
                new_dict_src[ud_feat].extend(feats_dict_src[feat])

for feat in new_dict_src:
    f = open(f"data/{pair}/{folder_name}/{src}.feats_{feat}.txt","w")
    for word in [*set(new_dict_src[feat])]:
        f.write(f"{word}\n")
    f.close()

for feat in feats_dict_tgt:
    if "|" in feat:
        new_dict_tgt[feat] = feats_dict_tgt[feat]
    if ";" in feat:
        un_feat = ";".join(feat.split(";")[1:])
        ud_feat = check_feat(un_feat)
        if ud_feat:
            ud_feat = un_to_ud[feat.split(";")[0]]+ "|" + ud_feat
            if ud_feat not in new_dict_tgt:
                new_dict_tgt[ud_feat] = feats_dict_tgt[feat]
            else:
                new_dict_tgt[ud_feat].extend(feats_dict_tgt[feat])

for feat in new_dict_tgt:
    f = open(f"data/{pair}/{folder_name}/{tgt}.feats_{feat}.txt","w")
    for word in [*set(new_dict_tgt[feat])]:
        f.write(f"{word}\n")
    f.close()
