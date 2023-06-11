import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="el")
parser.add_argument("--t", help="echo the string you use here", default="en")
parser.add_argument("--s3", help="echo the string you use here", default="ell")
parser.add_argument("--t3", help="echo the string you use here", default="eng")
args = parser.parse_args()

src = args.s
tgt = args.t
src3 = args.s3
tgt3 = args.t3

pair = f"{src}-{tgt}"

def get_feats_dictionaries():
    dict_src = {}
    dict_tgt = {}

    filenames = glob.glob(f"data/{pair}/panlex.{pair}_form.unpopulated/*.txt")
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

def populate_noun():
    with open(f"data/{pair}/panlex.{pair}_form.populated/lemma-ud.noun.new_list", "r") as r:
        lemma_ud = r.read().splitlines()
        words = []
        for i in range(0, 167699, 5000):
            filename = f"data/{pair}/panlex.{pair}_form.populated/word.noun.{i}.list"
            with open(filename, "r") as r:
                words.extend(r.read().splitlines())
    new_feats_dict_src = {}
    for id in range(len(words)):
        new_feat = lemma_ud[id].split("\t")[1]
        word = words[id]
        if  new_feat not in new_feats_dict_src:
            new_feats_dict_src[new_feat] = [word]
        elif new_feat in new_feats_dict_src:
            new_feats_dict_src[new_feat].append(word)

    for feat in new_feats_dict_src:
        if "NOUN" in feat :
            f = open(f"data/{pair}/panlex.{pair}_form.populated/{src}.feats_{feat}.txt","w")
            for word in [*set(new_feats_dict_src[feat])]:
                f.write(f"{word}\n")
            f.close()

def populate_adj():
    with open(f"data/{pair}/panlex.{pair}_form.populated/lemma-ud.adj.new_list", "r") as r:
        lemma_ud = r.read().splitlines()
        words = []
        for i in range(0, 27672, 5000):
            filename = f"data/{pair}/panlex.{pair}_form.populated/word.adj.{i}.list"
            with open(filename, "r") as r:
                words.extend(r.read().splitlines())
    new_feats_dict_src = {}
    for id in range(len(words)):
        new_feat = lemma_ud[id].split("\t")[1]
        word = words[id]
        if  new_feat not in new_feats_dict_src:
            new_feats_dict_src[new_feat] = [word]
        elif new_feat in new_feats_dict_src:
            new_feats_dict_src[new_feat].append(word)

    for feat in new_feats_dict_src:
        if "ADJ" in feat :
            f = open(f"data/{pair}/panlex.{pair}_form.populated/{src}.feats_{feat}.txt","w")
            for word in [*set(new_feats_dict_src[feat])]:
                f.write(f"{word}\n")
            f.close()


def populate_verb():
    with open(f"data/{pair}/panlex.{pair}_form.populated/lemma-ud.verb.new_list", "r") as r:
        lemma_ud = r.read().splitlines()
        words = []
        for i in range(0, 116928, 5000):
            filename = f"data/{pair}/panlex.{pair}_form.populated/word.verb.{i}.list"
            with open(filename, "r") as r:
                words.extend(r.read().splitlines())
    new_feats_dict_src = {}
    for id in range(len(words)):
        new_feat = lemma_ud[id].split("\t")[1]
        word = words[id]
        if  new_feat not in new_feats_dict_src:
            new_feats_dict_src[new_feat] = [word]
        elif new_feat in new_feats_dict_src:
            new_feats_dict_src[new_feat].append(word)

    for feat in new_feats_dict_src:
        if "VERB" in feat :
            f = open(f"data/{pair}/panlex.{pair}_form.populated/{src}.feats_{feat}.txt","w")
            for word in [*set(new_feats_dict_src[feat])]:
                f.write(f"{word}\n")
            f.close()


feats_dict_src, feats_dict_tgt = get_feats_dictionaries()
populate_noun()
populate_adj()
populate_verb()