import os
import glob
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="echo the string you use here", default="el")
parser.add_argument("--t", help="echo the string you use here", default="en")
args = parser.parse_args()

src = args.s
tgt = args.t
if src < tgt:
    pair = f"{src}-{tgt}"
else:
    pair = f"{tgt}-{src}"

os.system(f"mkdir data/{pair}/panlex.{src}-{tgt}_form.populated")

def get_feats_dictionaries():
    dict_src = {}
    dict_tgt = {}

    filenames = glob.glob(f"data/{pair}/panlex.{src}-{tgt}_form.unpopulated/*.txt")
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

def populate_noun():
    genderlemmas = {}
    genderlemmas["Fem"] = []
    genderlemmas["Masc"] = []
    genderlemmas["Neut"] = []
    for feat in feats_dict_src:
        pos = feat.split("|")[0]
        tags = "|".join(feat.split("|")[1:])
        if pos == "NOUN" and "Gender=" in tags:
            gender = tags.split("Gender=")[1].split("|")[0]
            for word in feats_dict_src[feat]:
                if word in src_lemma:
                    lemma = src_lemma[word]
                    genderlemmas[gender].append(lemma)

    nouncases = ["Case=Acc", "Case=Dat", "Case=Gen", "Case=Nom", "Case=Voc"]
    nounnumbers = ["Number=Sing", "Number=Plur"]
    with open(f"data/{pair}/panlex.{src}-{tgt}_form.populated/lemma-ud.noun.list", "w") as w:
        for lemmas in genderlemmas:
            feat = f"NOUN|Case=Nom|Gender={lemmas}|Number=Sing"
            pos = feat.split("|")[0]
            tags = "|".join(feat.split("|")[1:])
            for nouncase in nouncases:
                for nounnumber in nounnumbers:
                    new_tags = tags.replace("Case=Nom", nouncase)
                    new_tags = new_tags.replace("Number=Sing", nounnumber)
                    if new_tags in ud_to_un_stanza:
                        new_feat = f"{pos}|{new_tags}"
                        un_tags = ud_to_un_stanza[new_tags]
                        un_pos = ud_to_un_stanza[pos]
                        un_feat = f"{un_pos};{un_tags}"
                        for lemma in genderlemmas[lemmas]:
                            w.write(f"{lemma}\t{new_feat}\t{un_feat}\n")

def populate_adj():
    genderlemmas = {}
    genderlemmas["Fem"] = []
    genderlemmas["Masc"] = []
    genderlemmas["Neut"] = []
    for feat in feats_dict_src:
        pos = feat.split("|")[0]
        tags = "|".join(feat.split("|")[1:])
        if pos == "ADJ" and "Gender=" in tags:
            gender = tags.split("Gender=")[1].split("|")[0]
            for word in feats_dict_src[feat]:
                if word in src_lemma:
                    lemma = src_lemma[word]
                    genderlemmas[gender].append(lemma)

    adjcases = ["Case=Acc", "Case=Gen", "Case=Nom"]
    adjnumbers = ["Number=Sing", "Number=Plur"]
    # adjgenders = ["Gender=Fem", "Gender=Masc", "Gender=Neut"]
    with open(f"data/{pair}/panlex.{src}-{tgt}_form.populated/lemma-ud.adj.list", "w") as w:
        for lemmas in genderlemmas:
            feat = f"ADJ|Case=Nom|Gender={lemmas}|Number=Sing"
            pos = feat.split("|")[0]
            tags = "|".join(feat.split("|")[1:])
            for adjcase in adjcases:
                for adjnumber in adjnumbers:
                    # for adjgender in adjgenders:
                    new_tags = tags.replace("Case=Nom", adjcase)
                    new_tags = new_tags.replace("Number=Sing", adjnumber)
                    # new_tags = new_tags.replace(f"Gender={lemmas}", adjgender)
                    if new_tags in ud_to_un_stanza:
                        new_feat = f"{pos}|{new_tags}"
                        un_tags = ud_to_un_stanza[new_tags]
                        un_pos = ud_to_un_stanza[pos]
                        un_feat = f"{un_pos};{un_tags}"
                        for lemma in genderlemmas[lemmas]:
                            w.write(f"{lemma}\t{new_feat}\t{un_feat}\n")

def populate_verb():
    lemmas = []
    for feat in feats_dict_src:
        pos = feat.split("|")[0]
        tags = "|".join(feat.split("|")[1:])
        if pos == "VERB":
            for word in feats_dict_src[feat]:
                if word in src_lemma:
                    lemma = src_lemma[word]
                    lemmas.append(lemma)

    verbpersons = ["Person=1", "Person=2", "Person=3"]
    verbnumbers = ["Number=Sing", "Number=Plur"]
    verbtenses = ["Tense=Pres", "Tense=Past"]
    verbaspects = ["Aspect=Imp", "Aspect=Perf"]
    verbvoices = ["Voice=Act", "Voice=Pass"]
    with open(f"data/{pair}/panlex.{src}-{tgt}_form.populated/lemma-ud.verb.list", "w") as w:
        feat = f"VERB|Aspect=Imp|Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin|Voice=Act"
        pos = feat.split("|")[0]
        tags = "|".join(feat.split("|")[1:])
        for verbperson in verbpersons:
            for verbnumber in verbnumbers:
                for verbtense in verbtenses:
                    for verbaspect in verbaspects:
                        for verbvoice in verbvoices:
                            new_tags = tags.replace("Person=1", verbperson)
                            new_tags = new_tags.replace("Number=Sing", verbnumber)
                            new_tags = new_tags.replace("Tense=Pres", verbtense)
                            new_tags = new_tags.replace("Aspect=Imp", verbaspect)
                            new_tags = new_tags.replace("Voice=Act", verbvoice)
                            if new_tags in ud_to_un_stanza:
                                new_feat = f"{pos}|{new_tags}"
                                un_tags = ud_to_un_stanza[new_tags]
                                un_pos = ud_to_un_stanza[pos]
                                un_feat = f"{un_pos};{un_tags}"
                                for lemma in lemmas:
                                    w.write(f"{lemma}\t{new_feat}\t{un_feat}\n")

def clean(typ):
    with open(f"data/{pair}/panlex.{src}-{tgt}_form.populated/lemma-ud.{typ}.list", "r") as r:
        with open(f"data/{pair}/panlex.{src}-{tgt}_form.populated/lemma-ud.{typ}.new_list", "w") as w:
            for line in r.readlines():
                lemma = line.split("\t")[0]
                new_feat = line.split("\t")[1]
                un_feat = line.split("\t")[2]
                if (lemma[-2] =="ο" and lemma[-1] == "ς") or (lemma[-2] =="η" and lemma[-1] == "ς") or (lemma[-2] =="α" and lemma[-1] == "ς"):
                    new_feat = new_feat.replace("Fem","Masc")
                    new_feat = new_feat.replace("Neut","Masc")
                    un_feat = un_feat.replace("FEM","MASC")
                    un_feat = un_feat.replace("NEUT","MASC")
                if (lemma[-1] == "α") or (lemma[-1] == "η") or (lemma[-2]=="ώ" and lemma[-1] == "ν") or (len(lemma) > 2 and lemma[-3] == "ε" and lemma[-2]== "ι" and lemma[-1] == "ς"):
                    new_feat = new_feat.replace("Masc","Fem")
                    new_feat = new_feat.replace("Neut","Fem")
                    un_feat = un_feat.replace("MASC","FEM")
                    un_feat = un_feat.replace("NEUT","FEM")
                if (lemma[-1] == "ι") or (lemma[-1] == "ο") or (len(lemma) > 2 and lemma[-3] == "ο" and lemma[-2]== "υ" and lemma[-1] == "ς"):
                    new_feat = new_feat.replace("Masc","Neut")
                    new_feat = new_feat.replace("Fem","Neut")
                    un_feat = un_feat.replace("MASC","NEUT")
                    un_feat = un_feat.replace("FEM","NEUT")
                w.write(f"{lemma}\t{new_feat}\t{un_feat}")

feats_dict_src, feats_dict_tgt = get_feats_dictionaries()
src_lemma = get_vocab(f"data/{pair}/vocab/panlex.{src}.form-lemma.pkl")
ud_to_un_stanza = get_vocab(f"data/{pair}/vocab/stanza.all.ud-un.pkl")
# populate_noun()
# populate_adj()
# populate_verb()
# clean("noun")
# clean("adj")