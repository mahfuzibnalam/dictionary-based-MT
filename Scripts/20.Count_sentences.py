typ = "orig"

def diff(list1, list2):
    c = set(list1).union(set(list2))
    d = set(list1).intersection(set(list2))
    return list(c - d)

def Count(changlines):
    changsents = 0
    ids = []
    for id1, line1 in enumerate(changlines):
        if id1 not in ids:
            ids.append(id1)
            words1 = line1.split(" ")
            for id2 in range(id1 + 1 , len(changlines)):
                words2 = changlines[id2].split(" ") 
                di = diff(words1, words2)
                if len(di) <= 4:
                    ids.append(id2)
            changsents += 1

    print(changsents)
    
with open(f"data/en-gd/exp-{typ}/stanza.all/new_train(5K).gd", "r") as r:
    srcchanglines = r.read().splitlines()
Count(srcchanglines)

print("----------------------")

with open(f"data/en-gd/exp-{typ}/stanza.all/new_train(5K)_bas.gd", "r") as r:
    srcchangbaslines = r.read().splitlines()
Count(srcchangbaslines)