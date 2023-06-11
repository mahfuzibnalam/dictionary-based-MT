import os
import stanza
import pickle
import argparse

parser = argparse.ArgumentParser(description="Noises pre-trained MT model.")
parser.add_argument("--s", type=str, required=False, help="The pre-trained model directory.", default="")
parser.add_argument("--t", type=str, required=False, help="The pre-trained model directory.", default="")
args = parser.parse_args()

src = args.s
tgt = args.t
pair = f"{src}-{tgt}"

#nlpsrc = stanza.Pipeline(lang=src, processors='tokenize,mwt,pos', tokenize_pretokenized=True)
#nlptgt = stanza.Pipeline(lang=tgt, processors='tokenize,mwt,pos', tokenize_pretokenized=True)
nlpsrc = stanza.Pipeline(lang=src, processors='tokenize,pos', tokenize_pretokenized=True)
nlptgt = stanza.Pipeline(lang=tgt, processors='tokenize,pos', tokenize_pretokenized=True)

ud_to_un = {}
ud_to_un["VERB"] = "V"
ud_to_un["NOUN"] = "N"
ud_to_un["ADJ"] = "ADJ"

un_to_ud = {}
un_to_ud["V"] = "VERB"
un_to_ud["N"] = "NOUN"
un_to_ud["ADJ"] = "ADJ"

pinffeats = []
feats = []
with open(f"data/{pair}/stanza.all/old_train.{src}", "r") as r:
    lines = r.readlines()
    for line in lines:
        doc = nlpsrc(line.strip())
        for sentence in doc.sentences:
            for token in sentence.words:
                if token.feats not in feats:
                    feats.append(token.feats)
                if token.feats and (token.upos == "VERB" or token.upos == "NOUN" or token.upos == "ADJ") and src == "en":
                    pinffeat = token.upos + "|" + token.feats
                    if pinffeat not in pinffeats:
                        pinffeats.append(pinffeat)

with open(f"data/{pair}/stanza.all/UNI_{src}.txt", "w") as w:
    for feat in feats:
        w.write(f"# text = hello\n")
        w.write(f"1\t_\t_\t_\t_\t{feat}\t0\troot\t0:root\t_\n\n")

feats = []
with open(f"data/{pair}/stanza.all/old_train.{tgt}", "r") as r:
    lines = r.readlines()
    for line in lines:
        doc = nlptgt(line.strip())
        for sentence in doc.sentences:
            for token in sentence.words:
                if token.feats not in feats:
                    feats.append(token.feats)
                if token.feats and (token.upos == "VERB" or token.upos == "NOUN" or token.upos == "ADJ") and tgt == "en":
                    pinffeat = token.upos + "|" + token.feats
                    if pinffeat not in pinffeats:
                        pinffeats.append(pinffeat)

with open(f"data/{pair}/stanza.all/UNI_{tgt}.txt", "w") as w:
    for feat in feats:
        w.write(f"# text = hello\n")
        w.write(f"1\t_\t_\t_\t_\t{feat}\t0\troot\t0:root\t_\n\n")

UD_PINF = {}
with open(f"data/UD-PINF.txt", "r") as r:
    lines = r.readlines()
    for line in lines:
        UD_PINF[line.split("_")[0]] = line.split("_")[1]

with open(f"data/{pair}/stanza.all/UD-PINF.txt", "w") as w:
    pinffeats.sort()
    for pinffeat in pinffeats:
        if pinffeat in UD_PINF:
            PINF = UD_PINF[pinffeat]
            w.write(f"{pinffeat}_{PINF}")
        else:
        	w.write(f"{pinffeat}_\n")

os.system(f"cp data/{pair}/stanza.all/UNI_{src}.txt data/{pair}/stanza.all/UD_{src}.txt")
os.chdir("ud-compatibility/UD_UM/")
os.system(f"python marry.py convert --ud ../../data/{pair}/stanza.all/UNI_{src}.txt")
os.chdir("../../")

os.system(f"cp data/{pair}/stanza.all/UNI_{tgt}.txt data/{pair}/stanza.all/UD_{tgt}.txt")
os.chdir("ud-compatibility/UD_UM/")
os.system(f"python marry.py convert --ud ../../data/{pair}/stanza.all/UNI_{tgt}.txt")
os.chdir("../../")

with open(f"data/{pair}/stanza.all/UD_{src}.txt", "r") as udr:
    udlines = udr.readlines()
    with open(f"data/{pair}/stanza.all/UNI_{src}.txt", "r") as unr:
        unlines = unr.readlines()
        for id, unline in enumerate(unlines):
            udline = udlines[id]
            if id % 3 == 1:
                udfeat = udline.strip().split("\t")[5]
                unfeat = unline.strip().split("\t")[5]
                if udfeat not in ud_to_un:
                    ud_to_un[udfeat] = unfeat
                if unfeat not in un_to_ud:
                    un_to_ud[unfeat] = udfeat

with open(f"data/{pair}/stanza.all/UD_{tgt}.txt", "r") as udr:
    udlines = udr.readlines()
    with open(f"data/{pair}/stanza.all/UNI_{tgt}.txt", "r") as unr:
        unlines = unr.readlines()
        for id, unline in enumerate(unlines):
            udline = udlines[id]
            if id % 3 == 1:
                udfeat = udline.strip().split("\t")[5]
                unfeat = unline.strip().split("\t")[5]
                if udfeat not in ud_to_un:
                    ud_to_un[udfeat] = unfeat
                if unfeat not in un_to_ud:
                    un_to_ud[unfeat] = udfeat
os.system(f"mkdir data/{pair}/vocab")

f = open(f"data/{pair}/vocab/stanza.all.ud-un.pkl","wb")
pickle.dump(ud_to_un, f)
f.close()

f = open(f"data/{pair}/vocab/stanza.all.un-ud.pkl","wb")
pickle.dump(un_to_ud, f)
f.close()