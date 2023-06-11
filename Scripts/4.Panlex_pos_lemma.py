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
folder_name = f"panlex.{src}-{tgt}_lemma"

nlpsrc = stanza.Pipeline(lang=src, processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)
nlptgt = stanza.Pipeline(lang=tgt, processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)

with open(f'data/{pair}/vocab/stanza.all.un-ud.pkl', 'rb') as r:
    un_to_ud = pickle.load(r)

UDposes = ["VERB", "ADJ", "NOUN"]
pos = {}
lemma = {}

os.system(f"mkdir data/{pair}/{folder_name}")

with open(f"data/{pair}/unimorph/unimorph.{src3}.txt", "r") as r:
    for line in r:
        elemets = line.strip().split("\t")
        if len(elemets) == 3:
            if elemets[1] not in pos and " " not in elemets[1]:
                pos[elemets[1]] = elemets[2].split(";")[0]
                lemma[elemets[1]] = elemets[0]

with open(f"data/{pair}/unimorph/unimorph.{tgt3}.txt", "r") as r:
    for line in r:
        elemets = line.strip().split("\t")
        if len(elemets) == 3:
            if elemets[1] not in pos and " " not in elemets[1]:
                pos[elemets[1]] = elemets[2].split(";")[0]
                lemma[elemets[1]] = elemets[0]

translation = {}
translation_lemma = {}
with open(f'data/{pair}/panlex/{src3}_{tgt3}_lexicon.txt', 'r') as r:
    lines = r.read().splitlines()
    upos_dict_src = {}
    upos_dict_tgt = {}
    for line in lines:
        wordsrc = line.strip().split("\t")[0]
        wordtgt = line.strip().split("\t")[1]
        if " " in wordsrc or " " in wordtgt:
            continue
        found = False
        if wordsrc in pos and wordtgt in pos and pos[wordsrc] == pos[wordtgt]:
            if wordsrc not in translation:
                translation[wordsrc] = wordtgt
            if lemma[wordsrc] not in translation_lemma:
                found = True
                translation_lemma[lemma[wordsrc]] = lemma[wordtgt]

                if un_to_ud[pos[wordsrc]] not in upos_dict_src:
                    upos_dict_src[un_to_ud[pos[wordsrc]]] = [lemma[wordsrc]]
                elif un_to_ud[pos[wordsrc]] in upos_dict_src:
                    upos_dict_src[un_to_ud[pos[wordsrc]]].append(lemma[wordsrc])
                if un_to_ud[pos[wordtgt]] not in upos_dict_tgt:
                    upos_dict_tgt[un_to_ud[pos[wordtgt]]] = [lemma[wordtgt]]
                elif un_to_ud[pos[wordtgt]] in upos_dict_tgt:
                    upos_dict_tgt[un_to_ud[pos[wordtgt]]].append(lemma[wordtgt])

        if not found:
            docsrc = nlpsrc(wordsrc)
            doctgt = nlptgt(wordtgt)
            srcword = docsrc.sentences[0].words[0]
            tgtword = doctgt.sentences[0].words[0]

            if srcword.upos == tgtword.upos and srcword.upos in UDposes:
                if wordsrc not in translation:
                    translation[wordsrc] = wordtgt
                if tgtword.lemma and srcword.lemma and srcword.lemma not in translation_lemma:
                    translation_lemma[srcword.lemma] = tgtword.lemma

                    if srcword.upos not in upos_dict_src and srcword.upos:
                        upos_dict_src[srcword.upos] = [srcword.lemma]
                    elif srcword.upos in upos_dict_src and srcword.upos:
                        upos_dict_src[srcword.upos].append(srcword.lemma)
                    if tgtword.upos not in upos_dict_tgt and tgtword.upos:
                        upos_dict_tgt[tgtword.upos] = [tgtword.lemma]
                    elif tgtword.upos in upos_dict_tgt and tgtword.upos:
                        upos_dict_tgt[tgtword.upos].append(tgtword.lemma)
    for feat in upos_dict_src:
        f = open(f"data/{pair}/{folder_name}/{src}.upos_{feat}.txt","w")
        for word in [*set(upos_dict_src[feat])]:
            f.write(f"{word}\n")
        f.close()
    for feat in upos_dict_tgt:
        f = open(f"data/{pair}/{folder_name}/{tgt}.upos_{feat}.txt","w")
        for word in [*set(upos_dict_tgt[feat])]:
            f.write(f"{word}\n")
        f.close()

f = open(f"data/{pair}/vocab/panlex.lemma.{src}-{tgt}.pkl","wb")
pickle.dump(translation_lemma, f)
f.close()

f = open(f"data/{pair}/vocab/panlex.{src}-{tgt}.pkl","wb")
pickle.dump(translation, f)
f.close()