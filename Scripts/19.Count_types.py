typ = "orig"

def Count(origlines):
    origtypes = []
    for line in origlines:
        words = line.split(" ")
        for word in words:
            if word not in origtypes:
                origtypes.append(word)
    
    print(len(origtypes))

with open(f"data/en-gd/exp-{typ}/gd-en.stanza.all.0K/train.en", "r") as r:
    srcoriglines = r.read().splitlines()
Count(srcoriglines)
with open(f"data/en-gd/exp-{typ}/gd-en.stanza.all.0K/train.gd", "r") as r:
    tgtoriglines = r.read().splitlines()
Count(tgtoriglines)
print("----------------------")
with open(f"data/en-gd/exp-{typ}/stanza.all/train(5K).en", "r") as r:
    srcchanglines = r.read().splitlines()
Count(srcchanglines)
with open(f"data/en-gd/exp-{typ}/stanza.all/train(5K).gd", "r") as r:
    tgtchanglines = r.read().splitlines()
Count(tgtchanglines)
print("----------------------")
with open(f"data/en-gd/exp-{typ}/stanza.all/train(5K)_bas.en", "r") as r:
    srcchangbaslines = r.read().splitlines()
Count(srcchangbaslines)
with open(f"data/en-gd/exp-{typ}/stanza.all/train(5K)_bas.gd", "r") as r:
    tgtchangbaslines = r.read().splitlines()
Count(tgtchangbaslines)