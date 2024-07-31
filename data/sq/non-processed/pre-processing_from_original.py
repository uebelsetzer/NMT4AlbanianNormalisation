TEXT = "BuS.INPUT.itrpt.20p.OLD+STANDARD.parallel.p0-p–008-p002.utf8.txt"

f = open(TEXT, "r", encoding="utf-8")
text = f.readlines()
f.close()

o = open(TEXT.split(".")[0] + "-processed.txt", "w", encoding="utf-8")
o.write("sq\tals\n")
for line in text:
    line = line.strip()
    if line != "":
        line = line.split("#")
        clean = list()
        for l in line:
            l = l.strip().replace("\t", " ")
            clean.append(l)
        assert len(clean) == 2, f"This line had multiple splitters: {line}"
        o.write(clean[0] + "\t" + clean[1] + "\n")
o.close()