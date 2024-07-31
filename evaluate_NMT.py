# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 17:02:48 2023

@author: zilio
"""

import argparse
import evaluate

###########################################################
def arguments():
    parser = argparse.ArgumentParser(description="Evaluate translations using SacreBLEU")
    #parser.add_argument("-s", "--source", default="data/pt/test_source.txt", help="File containing the source sentences.")
    #parser.add_argument("-g", "--gold", default="data/pt/test_gold.txt", help="File containing one reference translation per line.")
    #parser.add_argument("-t", "--translation", default="test/pt/translation_small100_noft.txt", help="File containing one translation per line.")
    #parser.add_argument("-r", "--results", default="results/pt/", help="Output file for the test.")
    parser.add_argument("-s", "--source", default="data/sq/test_source.txt", help="File containing the source sentences.")
    parser.add_argument("-g", "--gold", default="data/sq/test_gold.txt", help="File containing one reference translation per line.")
    parser.add_argument("-t", "--translation", default="test/sq/translation_small100_lr3e-5_ft.txt", help="File containing one translation per line.")
    parser.add_argument("-r", "--results", default="results/sq/", help="Output file for the test.")
    return parser.parse_args()

def get_sentences(f):
    sentences = list()
    for line in f:
        line = line.strip()
        sentences.append(line)
    return sentences

##########################################################

args = arguments()
sacrebleu = evaluate.load("sacrebleu")

source_file = args.source
predictions_file = args.translation
reference_file = args.gold
results_folder = args.results
results_file = "results_" + args.translation.split("_", 1)[1]

with open(source_file, "r", encoding="utf-8") as src:
    source = get_sentences(src)

with open(predictions_file, "r", encoding="utf-8") as pred:
    predictions = get_sentences(pred)

with open(reference_file, "r", encoding="utf-8") as ref:
    references = [[x] for x in get_sentences(ref)]


results = sacrebleu.compute(predictions=predictions, references=references)
print(results)

with open(results_folder + results_file, "w", encoding="utf-8") as res:
    res.write("source\tgold\ttranslation\tBLEU score\n")
    for s, p, r in zip(source, predictions, references):
        # Added use_effective_order for sentence-by-sentence evaluation, 
        # so sentences smaller than 4 tokens are also evaluated
        line_results = sacrebleu.compute(predictions=[p], references=r, use_effective_order=True)
        res.write(f"{s}\t{r[0]}\t{p}\t{line_results['score']}\n")
    
    res.write(f"\n\nFinal score:\t{results}")