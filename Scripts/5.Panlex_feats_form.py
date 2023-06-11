import os
import pickle
import stanza
import argparse
from numpy import append 

parser = argparse.ArgumentParser(description="Noises pre-trained MT model.")
parser.add_argument("--s", type=str, required=False, help="The pre-trained model directory.", default="kmr")
parser.add_argument("--t", type=str, required=False, help="The pre-trained model directory.", default="en")
parser.add_argument("--s3", type=str, required=False, help="The pre-trained model directory.", default="kmr")
parser.add_argument("--t3", type=str, required=False, help="The pre-trained model directory.", default="eng")
args = parser.parse_args()

src = args.s
tgt = args.t
src3 = args.s3
tgt3 = args.t3
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"
folder_name = f"panlex.{src}-{tgt}_form.old"

nlpsrc = stanza.Pipeline(lang=src, processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)
nlptgt = stanza.Pipeline(lang=tgt, processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)

UDposes = ["ADJ", "NOUN", "VERB"]
pos = {}
feats = {}

os.system(f"mkdir data/{pair}/{folder_name}")

with open(f"data/{pair}/unimorph/unimorph.{src3}.txt", "r") as r:
    for line in r:
        elemets = line.strip().split("\t")
        if len(elemets) == 3:
            if elemets[1] not in pos and " " not in elemets[1]:
                pos[elemets[1]] = elemets[2].split(";")[0]
                feats[elemets[1]] = elemets[2]

with open(f"data/{pair}/unimorph/unimorph.{tgt3}.txt", "r") as r:
    for line in r:
        elemets = line.strip().split("\t")
        if len(elemets) == 3:
            if elemets[1] not in pos and " " not in elemets[1]:
                pos[elemets[1]] = elemets[2].split(";")[0]
                feats[elemets[1]] = elemets[2]

translation = {}
with open(f'data/{pair}/panlex/{src3}_{tgt3}_lexicon.txt', 'r') as r:
    lines = r.read().splitlines()
    feats_dict_src = {}
    feats_dict_tgt = {}
    for line in lines:
        wordsrc = line.strip().split("\t")[0]
        wordtgt = line.strip().split("\t")[1]
        if " " in wordsrc or " " in wordtgt:
            continue
        found = False
        if wordsrc in pos and wordtgt in pos and pos[wordsrc] == pos[wordtgt]:
            if wordsrc not in translation:
                found = True
                translation[wordsrc] = wordtgt

                srcfeat = feats[wordsrc]
                if srcfeat not in feats_dict_src:
                    feats_dict_src[srcfeat] = [wordsrc]
                elif srcfeat in feats_dict_src:
                    feats_dict_src[srcfeat].append(wordsrc)
                
                tgtfeat = feats[wordtgt]
                if tgtfeat not in feats_dict_tgt:
                    feats_dict_tgt[tgtfeat] = [wordtgt]
                elif tgtfeat in feats_dict_tgt:
                    feats_dict_tgt[tgtfeat].append(wordtgt)

        if not found:
            docsrc = nlpsrc(wordsrc)
            doctgt = nlptgt(wordtgt)
            srcword = docsrc.sentences[0].words[0]
            tgtword = doctgt.sentences[0].words[0]

            if srcword.upos == tgtword.upos and srcword.upos in UDposes:
                if tgtword.text and srcword.text and srcword.text not in translation:
                    translation[srcword.text] = tgtword.text

                    if srcword.feats:
                        srcfeat = srcword.upos + "|" + srcword.feats
                        if  srcfeat not in feats_dict_src:
                            feats_dict_src[srcfeat] = [srcword.text]
                        elif srcfeat in feats_dict_src:
                            feats_dict_src[srcfeat].append(srcword.text)

                    if tgtword.feats:
                        tgtfeat = tgtword.upos + "|" + tgtword.feats
                        if  tgtfeat not in feats_dict_tgt:
                            feats_dict_tgt[tgtfeat] = [tgtword.text]
                        elif tgtfeat in feats_dict_tgt:
                            feats_dict_tgt[tgtfeat].append(tgtword.text)
                
    for feat in feats_dict_src:
        f = open(f"data/{pair}/{folder_name}/{src}.feats_{feat}.txt","w")
        for word in [*set(feats_dict_src[feat])]:
            f.write(f"{word}\n")
        f.close()
    for feat in feats_dict_tgt:
        f = open(f"data/{pair}/{folder_name}/{tgt}.feats_{feat}.txt","w")
        for word in [*set(feats_dict_tgt[feat])]:
            f.write(f"{word}\n")
        f.close()

f = open(f"data/{pair}/vocab/panlex.form.{src}-{tgt}.pkl","wb")
pickle.dump(translation, f)
f.close()