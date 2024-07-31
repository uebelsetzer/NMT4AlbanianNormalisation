# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 14:52:31 2023

@author: zilio
"""

import argparse
import datetime
import re
from transformers import M2M100ForConditionalGeneration, AutoTokenizer

###########################################################
def arguments():
    parser = argparse.ArgumentParser(description="Translate using mBart model")
    #parser.add_argument("-m", "--model", default="models/m2m100_418M-finetuned-por-to-pob", help="Folder containing a translation model.")
    parser.add_argument("-m", "--model", default="m2m100_418M-finetuned-sq_orig-to-sq_mod", help="Folder containing a translation model.")
    #parser.add_argument("-s", "--source", default="data/pt/test_source.txt", help="File containing one sentence per line.")
    parser.add_argument("-s", "--source", default="data/sq/test_source.txt", help="File containing one sentence per line.")
    parser.add_argument("-t", "--translation", default="translation_m2m100_ft", help="File containing one translation per line.")
    #parser.add_argument("-o", "--output-folder", default="test/pt/", help="Folder where the translated file should be saved.")
    parser.add_argument("-o", "--output-folder", default="test/sq/", help="Folder where the translated file should be saved.")
    parser.add_argument("-tmx", "--to-tmx", default=True, help="Binary value indicating whether a TMX file should be generated.")
    parser.add_argument("-e", "--to-eval", default=True, help="Binary value indicating whether an evaluation file should be generated.")
    #parser.add_argument("-l", "--lang", default="pt", help="Language code that should be used in the tokenizer. For instance, 'pt-PT' for Portuguese and 'en-US' for US English.")
    parser.add_argument("-l", "--lang", default="sq", help="Language code that should be used in the tokenizer. For instance, 'pt' for Portuguese and 'en' for English.")
    return parser.parse_args()


def get_source(src):
    source_sentences = list()
    for line in src:
        line = line.strip()
        if line != "":
            source_sentences.append(line)
    return source_sentences
        

def break_if_too_long(sentence):
    s = list()
    
    # Checks what type of punctuation should be used for splitting
    if ":" in sentence or ";" in sentence:
        punctuation = re.compile(r"(;|:)") # Splits at "less invasive" punctuation
    else:
        punctuation = re.compile(r"(,)") # Splits wherever is possible
    split_sentence = re.split(punctuation, sentence)
    
    while split_sentence:
        if len(split_sentence) > 1:
            # Will use any size of split that has a ":" at the end or any split that is already above 700 characters long
            if split_sentence[0][-1] != ":" and len(split_sentence[0] + split_sentence[1]) < 700:
                split = split_sentence[0] + split_sentence[1]
                del split_sentence[0]
                split_sentence[0] = split
            else:
                s.append(split_sentence[0])
                del split_sentence[0]
        else:
            s.append(split_sentence[0])
            del split_sentence[0]
    print(s)
    return s
    

def translate(src_list, model_path, lang):
    
    print("Loading model and tokenizer...")
    model = M2M100ForConditionalGeneration.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    tokenizer.src_lang = lang
    print("Loaded!")
    
    print("Starting translation process...")
    translations = list()
    t_counter = 0
    n_source = len(src_list)
    for src_text in src_list:
        t_counter += 1
        print(f"Translating sentence {t_counter} of {n_source}...")
        #print(f"Translating:\t<<{src_text}>>")
        is_too_long = False
        if len(src_text) > 700:
            print("The text is too long:", len(src_text))
            src_text = break_if_too_long(src_text)
            is_too_long = True
        if is_too_long:
            target = str()
            for st in src_text:
                lower = False
                if st[0].islower():
                    lower = True
                s = tokenizer(st, return_tensors="pt", padding=True)
                translated_text = model.generate(**s, forced_bos_token_id=tokenizer.lang_code_to_id[lang])
                #translated_text = model.generate(**s, forced_bos_token_id=tokenizer.lang_code_to_id[lang])
                t = [tokenizer.decode(tt, skip_special_tokens=True) for tt in translated_text][0]
                if lower:
                    t[0] = t[0].lower()
                target = target + " " + t 
            translations.append(target.strip())
        else:
            s = tokenizer(src_text, return_tensors="pt", padding=True)
            translated_text = model.generate(**s, forced_bos_token_id=tokenizer.lang_code_to_id[lang])
            #translated_text = model.generate(**s, forced_bos_token_id=tokenizer.lang_code_to_id[lang])
            target = [tokenizer.decode(tt, skip_special_tokens=True) for tt in translated_text]
            translations.append(target[0])
        print("Target:", target)
    
    return translations


def generate_tmx(src_list, translations, filename, lang, target_lang):
    assert len(src_list) == len(translations), f"The source and target have different sizes: {len(src_list)} vs. {len(translations)}\nPlease make sure they have the same amount of sentences."
    with open(filename, "w", encoding="utf-8") as tmx_file:
        tmx_file.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE tmx SYSTEM "tmx14.dtd">
<tmx version="1.4">
  <header creationtool="Python Script" o-tmf="OmegaT TMX" adminlang="EN-US" datatype="plaintext" creationtoolversion="6.0.0_0_1bf1729c" segtype="sentence" srclang="{lang}"/>
  <body>
""")
        for src, tgt in zip(src_list, translations):
            now = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
            print(f"SOURCE: {src}\nTARGET: {tgt}\n{now}\n\n")
            tmx_file.write(f"""    <tu>
      <tuv xml:lang="{lang}">
        <seg>{src}</seg>
      </tuv>
      <tuv xml:lang="{target_lang}" creationid="AI" creationdate="{now}">
        <seg>{tgt}</seg>
      </tuv>
    </tu>\n""")
    
        tmx_file.write("""  </body>\n</tmx>""")

def generate_eval(translations, filename):
    with open(filename, "w", encoding="utf-8") as eval_file:
        for target in translations:
            eval_file.write(target + "\n")
    
###########################################################

args = arguments()
model_path = args.model
source_file = args.source
output_file = args.translation
outdir = args.output_folder
to_tmx = args.to_tmx
to_eval = args.to_eval
lang = args.lang

if lang == "pt":
    target_lang = "pt-BR"
elif lang == "sq":
    target_lang = "sq-mod"


with open(source_file, "r", encoding="utf-8") as src:
    src_text = get_source(src)

translations = translate(src_text, model_path, lang)

if to_tmx:
    tmx_file = outdir + output_file + ".tmx"
    generate_tmx(src_text, translations, tmx_file, lang, target_lang)
else:
    for t in translations:
        print(t)

if to_eval:
    eval_file = outdir + output_file + ".txt"
    generate_eval(translations, eval_file)

print("Finished!")