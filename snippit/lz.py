txt = open("boneless.txt").read()
d = {}
# single
for i in txt:
    if i not in d:
        d[i] = 1
    else:
        d[i] += 1

print(d)


def scan(txt, size):
    d = {}
    for i in range(len(txt)):
        val = txt[i : i + size]
        if val not in d:
            d[val] = 1
        else:
            d[val] += 1
    print("length: ", len(d), " for ", size, " ratio ", float(len(d) / size))
    return d
