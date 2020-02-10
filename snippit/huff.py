from heapq import heappush, heappop, heapify
from collections import defaultdict


def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = "0" + pair[1]
        for pair in hi[1:]:
            pair[1] = "1" + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def genbitstream(txt, huff):
    "turn the huff into a dictionary"
    d = {}
    for i in huff:
        d[i[0]] = i[1]
    "generate a text bitstream"
    bs = ""
    for i in txt:
        bs += d[i]
    print(bs)
    print(len(bs) / 8)
    return bs


txt = open("boneless.txt").read()
print(txt)
symb2freq = defaultdict(int)
for ch in txt:
    symb2freq[ch] += 1
huff = encode(symb2freq)
print("Symbol\tWeight\tHuffman Code")
for p in huff:
    print("%s\t%s\t%s" % (p[0], symb2freq[p[0]], p[1]))

bs = genbitstream(txt, huff)
