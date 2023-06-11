import argparse
import unimorph_inflect
from unimorph_inflect import inflect

parser = argparse.ArgumentParser()
parser.add_argument("--s3", help="echo the string you use here", default="ell")
parser.add_argument("--typ", help="echo the string you use here", default="")
parser.add_argument("--strt", help="echo the string you use here", default="")
args = parser.parse_args()

src3 = args.s3
strt = (int)(args.strt)
pair = "el-en"

with open(f"data/{pair}/panlex.{pair}_form.populated/lemma-ud.{args.typ}.new_list", "r") as r:
    with open(f"data/{pair}/panlex.{pair}_form.populated/word.{args.typ}.{strt}.list", "w") as w:
        lines = r.read().splitlines()
        for line in lines[strt:strt+5000]:
            lemma = line.split('\t')[0]
            un_feat = line.split('\t')[2]
            un_feat = un_feat.replace("IND","")
            un_feat = un_feat.replace("ACT","")
            un_feat = un_feat.replace("FIN","")
            un_feat = un_feat.replace(";;",";")
            result = inflect(lemma, un_feat, language=src3)
            w.write(f"{result[0]}\n")