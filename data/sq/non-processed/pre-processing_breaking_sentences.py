import re

TEXT = "BuS-processed.txt"

f = open(TEXT, "r", encoding="utf-8")
text = f.readlines()
f.close()

o = open(TEXT.split(".")[0] + "-split_sentences.txt", "w", encoding="utf-8")
for line in text:
    line = line.strip()
    if line != "":
        split_line = line.split("\t")
        assert len(split_line) == 2, f"This line had multiple splitters: {split_line}"
        orig = list()
        norm = list()
        if ";" in split_line[0]:
            orig.extend(split_line[0].split(";"))
            norm.extend(split_line[1].split(";"))
            assert len(orig) == len(norm), f"Error! Punctuation was changed:\n{orig}\n{norm}\n"
            for y, z in zip(orig, norm):
                if y != orig[-1]:
                    o.write(y.strip() + " ;\t" + z.strip() + " ;\n")
                else:
                    o.write(y.strip() + "\t" + z.strip() + "\n")
        else:
            o.write(line + "\n")
o.close()