import math
import glob
import pickle
import stanza
import random
import argparse
from pyinflect import getInflection

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="gd")
parser.add_argument("--t", help="echo the string you use here", default="en")
parser.add_argument("--s3", help="echo the string you use here", default="gla")
parser.add_argument("--t3", help="echo the string you use here", default="eng")
parser.add_argument("--dataset", help="echo the string you use here", default="stanza.all")
parser.add_argument("--rep_num", help="echo the string you use here", default="3") # one = 5000
args = parser.parse_args()

src = args.s
tgt = args.t
src3 = args.s3
tgt3 = args.t3
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"
dataset = args.dataset
rep_num = (int)(args.rep_num)

nlpsrc = stanza.Pipeline(lang=src, processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)
nlptgt = stanza.Pipeline(lang=tgt, processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)

def get_feats_dictionaries():
    dict_src = {}
    dict_tgt = {}

    filenames = glob.glob(f"data/{pair}/panlex.{src}-{tgt}_form/*.txt")
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

def get_dict(filename):
    a_to_b = {}
    with open(filename, 'r') as r:
        lines = r.read().splitlines()
        for line in lines:
            a = line.strip().split("_")[0]
            b = line.strip().split("_")[-1]
            a_to_b[a] = b
    return a_to_b

def get_ids_to_modify(alignline):
    srctotgt = {}
    duplicates = []
    if alignline == "":
        return srctotgt
    for alignments in alignline.split(" "):
        left = (int)(alignments.split("-")[0])
        right = (int)(alignments.split("-")[1])
        if left in srctotgt:
            duplicates.append(left)
        srctotgt[left] = right
    duplicates = [*set(duplicates)]
    for duplicate in duplicates:
        srctotgt.pop(duplicate, None)
    return srctotgt

def create_old_word_dictionaries(srcsent, tgtsent):
    docsrc = nlpsrc(srcsent)
    oldsrcwords = {}
    num = 0
    for sentence in docsrc.sentences:
        for word in sentence.words:
            oldsrcwords[num] = word
            num += 1
    
    doctgt = nlptgt(tgtsent)
    oldtgtwords = {}
    num = 0
    for sentence in doctgt.sentences:
        for word in sentence.words:
            oldtgtwords[num] = word
            num += 1
    return oldsrcwords, oldtgtwords

def get_ids_to_finalize(srctotgt, oldsrcwords, oldtgtwords):
    keys = list(srctotgt.keys())
    for srckey in keys:
        tgtkey = srctotgt[srckey]
        if oldsrcwords[srckey].upos == oldtgtwords[tgtkey].upos and (oldsrcwords[srckey].upos == "NOUN" or oldsrcwords[srckey].upos == "ADJ" or oldsrcwords[srckey].upos == "VERB"):
            continue
        else:
            srctotgt.pop(srckey, None)
    return srctotgt

def create_baseline(bassrctokens, bastgttokens, srckey, tgtkey, srcfeat):
    feat_keys = list(feats_dict_src.keys())
    srcpos = srcfeat.split("|")[0]
    feat_keys = [featkey for featkey in feat_keys if srcpos in featkey]
    # for i in range(0, 50): # remove
    while 1:
        feat_key = random.choice(feat_keys)
        if len(feats_dict_src[feat_key]) != 0:
            srcwordbas = random.choice(feats_dict_src[feat_key])
            # srcwordbas = random.choice(feats_dict_src[feat_key][0: math.ceil(len(feats_dict_src[feat_key])/2)]) # half
            if srcwordbas in translation_form:
                tgtwordbas = translation_form[srcwordbas]
                bassrctokens[srckey] = f"{srcwordbas}"
                bastgttokens[tgtkey] = f"{tgtwordbas}"
                # feats_dict_src[feat_key].remove(srcwordbas) # remove
                break
    return bassrctokens, bastgttokens

def create_sentences(srctotgt, oldsrcwords, oldtgtwords, ws, wt, srctokens, tgttokens, bs, bt):
    for i in range(rep_num):
        keys = list(srctotgt.keys())
        random.shuffle(keys)
        newsrctokens = srctokens.copy()
        newtgttokens = tgttokens.copy()
        bassrctokens = srctokens.copy()
        bastgttokens = tgttokens.copy()

        for srckey in keys[0: min(len(keys), 2)]:
            tgtkey = srctotgt[srckey]
            if oldsrcwords[srckey].feats and oldtgtwords[tgtkey].feats:
                srcfeat = oldsrcwords[srckey].upos + "|" + oldsrcwords[srckey].feats
                oldtgtfeat = oldtgtwords[tgtkey].upos + "|" + oldtgtwords[tgtkey].feats
                if oldtgtfeat in ud_to_pinf:
                    tgtfeat = ud_to_pinf[oldtgtfeat]
                if srcfeat in feats_dict_src and tgtfeat:
                    num = 0
                    # for i in range(0, 50): # remove
                    while 1:
                        if len(feats_dict_src[srcfeat]) != 0:
                            srcwordform = random.choice(feats_dict_src[srcfeat])
                            # srcwordform = random.choice(feats_dict_src[srcfeat][0: math.ceil(len(feats_dict_src[srcfeat])/2)]) # half
                            if num == 5:
                                break
                            num += 1
                            if srcwordform in src_lemma:
                                srcwordlemma = src_lemma[srcwordform]
                                if srcwordlemma in translation_lemma:
                                    tgtwordlemma = translation_lemma[srcwordlemma]
                                    tgtwordform = getInflection(tgtwordlemma, tag=tgtfeat)
                                    if tgtwordform:
                                        newsrctokens[srckey] = f"{srcwordform}"
                                        newtgttokens[tgtkey] = f"{tgtwordform[0]}"
                                        # feats_dict_src[srcfeat].remove(srcwordform) # remove
                                        bassrctokens, bastgttokens = create_baseline(bassrctokens, bastgttokens, srckey, tgtkey, srcfeat)
                                        break

        newsrcsent = " ".join(newsrctokens)
        newtgtsent = " ".join(newtgttokens)
        newsrcsent.replace("\n", "")
        newtgtsent.replace("\n", "")
        ws.write(f"<noisy> {newsrcsent}\n")
        wt.write(f"<noisy> {newtgtsent}\n")
        bassrcsent = " ".join(bassrctokens)
        bastgtsent = " ".join(bastgttokens)
        bassrcsent.replace("\n", "")
        bastgtsent.replace("\n", "")
        bs.write(f"<noisy> {bassrcsent}\n")
        bt.write(f"<noisy> {bastgtsent}\n")

random.seed(42)
feats_dict_src, feats_dict_tgt = get_feats_dictionaries()
translation_lemma = get_vocab(f"data/{pair}/vocab/panlex.lemma.{src}-{tgt}.pkl")
translation_form = get_vocab(f"data/{pair}/vocab/panlex.form.{src}-{tgt}.pkl")
src_lemma = get_vocab(f"data/{pair}/vocab/panlex.{src}.form-lemma.pkl")
ud_to_pinf = get_dict(f"data/{pair}/stanza.all/UD-PINF.txt")


for typ in ["valid", "test", "train"]:
    with open(f"data/{pair}/{dataset}/tagged_{typ}.{tgt}", "w") as wt:
        with open(f"data/{pair}/{dataset}/old_{typ}.{tgt}", "r") as rt:
            for id, line in enumerate(rt):
                wt.write(f"<clean> {line}")
    with open(f"data/{pair}/{dataset}/tagged_{typ}.{src}", "w") as wt:
        with open(f"data/{pair}/{dataset}/old_{typ}.{src}", "r") as rt:
            for id, line in enumerate(rt):
                wt.write(f"<clean> {line}")


with open(f"data/{pair}/{dataset}/new_train({rep_num}).{src}", "w") as ws:
    with open(f"data/{pair}/{dataset}/new_train({rep_num}).{tgt}", "w") as wt:
        with open(f"data/{pair}/{dataset}/new_train({rep_num})_bas.{src}", "w") as bs:
            with open(f"data/{pair}/{dataset}/new_train({rep_num})_bas.{tgt}", "w") as bt:

                with open(f"data/{pair}/alignment/{src}-{tgt}.{dataset}/train.alignment", "r") as rs:
                    sentlines = rs.read().splitlines()
                    with open(f"data/{pair}/alignment/{src}-{tgt}.{dataset}/train.aligned", "r") as ra:
                        alignlines = ra.read().splitlines()

                        for id, alignline in enumerate(alignlines):
                            srctotgt = get_ids_to_modify(alignline)

                            srcsent = sentlines[id].strip().split("|||")[0].strip()
                            tgtsent = sentlines[id].strip().split("|||")[1].strip()

                            oldsrcwords, oldtgtwords = create_old_word_dictionaries(srcsent, tgtsent)
                            srctotgt = get_ids_to_finalize(srctotgt, oldsrcwords, oldtgtwords)
                            
                            srctokens = srcsent.split(" ")
                            tgttokens = tgtsent.split(" ")

                            if len(srctotgt) >= 1 and len(srctokens) >= 7 and len(tgttokens) >= 7: # quality < 7
                                print(id)
                                create_sentences(srctotgt, oldsrcwords, oldtgtwords, ws, wt, srctokens, tgttokens, bs, bt)
                                
