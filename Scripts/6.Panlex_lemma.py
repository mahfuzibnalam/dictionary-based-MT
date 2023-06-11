import pickle
import stanza
import argparse

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

nlpsrc = stanza.Pipeline(lang=src, processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)
nlptgt = stanza.Pipeline(lang=tgt, processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)

UDposes = ["VERB", "ADJ", "NOUN"]
lemma = {}

with open(f"data/{pair}/unimorph/unimorph.{src3}.txt", "r") as r:
    for line in r:
        elemets = line.strip().split("\t")
        if len(elemets) == 3:
            if elemets[1] not in lemma and " " not in elemets[1]:
                lemma[elemets[1]] = elemets[0]

with open(f"data/{pair}/unimorph/unimorph.{tgt3}.txt", "r") as r:
    for line in r:
        elemets = line.strip().split("\t")
        if len(elemets) == 3:
            if elemets[1] not in lemma and " " not in elemets[1]:
                lemma[elemets[1]] = elemets[0]

translation_src = {}
translation_tgt = {}
with open(f'data/{pair}/panlex/{src3}_{tgt3}_lexicon.txt', 'r') as r:
    lines = r.read().splitlines()
    for line in lines:
        wordsrc = line.strip().split("\t")[0]
        wordtgt = line.strip().split("\t")[1]
        if " " in wordsrc or " " in wordtgt:
            continue
        found = False
        if wordsrc in lemma and wordsrc not in translation_src:
            found = True
            translation_src[wordsrc] = lemma[wordsrc]

        if not found:
            docsrc = nlpsrc(wordsrc)
            srcword = docsrc.sentences[0].words[0]
            if srcword.upos in UDposes and srcword.lemma and srcword.text not in translation_src:
                translation_src[srcword.text] = srcword.lemma

        found = False
        if wordtgt in lemma and wordtgt not in translation_tgt:
            found = True
            translation_tgt[wordtgt] = lemma[wordtgt]

        if not found:
            doctgt = nlptgt(wordtgt)
            tgtword = doctgt.sentences[0].words[0]
            if tgtword.upos in UDposes and tgtword.lemma and tgtword.text not in translation_tgt:
                translation_tgt[tgtword.text] = tgtword.lemma

f = open(f"data/{pair}/vocab/panlex.{src}.form-lemma.pkl","wb")
pickle.dump(translation_src, f)
f.close()

f = open(f"data/{pair}/vocab/panlex.{tgt}.form-lemma.pkl","wb")
pickle.dump(translation_tgt, f)
f.close()