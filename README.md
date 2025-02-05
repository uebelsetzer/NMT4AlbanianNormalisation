# Using neural machine translation for normalising historical documents

This repository contains scripts, datasets and results related to the paper:

> Zilio, L. and Kabashi, B. (2024) Using neural machine translation for normalising historical documents. In _Lexicography
and Semantics. Proceedings of the XXI EURALEX International Congress_. Institute for the Croatian Language. (https://euralex.org/wp-content/themes/euralex/proceedings/Euralex%202024/EURALEX2024_Pr_p827-839_Zilio-Kabashi.pdf.pdf)


## Basic requirements for running the scripts in this repository

A basic requirement is to have **Python 3** installed in your system. It is also recommended to create a new virtual environment for running the scripts in this repository.


### On Linux:

A simple way to do create a new environment would be to open a command line (or terminal) within the folder with this repository and type:

```
python -m venv nmt4dh
source nmt4dh/bin/activate
```

### On Windows:

A simple way to do create a new environment would be to open a PowerShell window (make sure you run it as administrator) within the folder with this repository and type:

```
pip install virtualenv
python -m virtualenv nmt4dh
.\nmt4dh\Scripts\activate
```


This should create and activate a new environment called **nmt4hd** (this name can be modified), and make sure it will not mess with anything else in the root Python environment.

With the activated virtual environment a few required packages need to be installed. The full list is in the "requirements.txt" file. All packages can be installed at once from within this repository folder by simply typing:

```
pip install -r requirements.txt
```

After the installation is done, new models can be fine-tuned using the commands in the following section.


## Fine-tuning neural machine translation (NMT) models

Due to the size of the fine-tuned models, we could not host them in this repository, but all scripts are provided to reproduce the work conducted on teh paper.

There are three scripts for fine-tuning NMT models, whose names start with "finetuningNMT-". These files can be run as they are, without selecting any option, by simply typing:
```
python finetuningNMT-m2m.py
```

or
```
python finetuningNMT-mbart50.py
```

or
```
python finetuningNMT-nllb_200.py
```

or these scripts can be customised (for using other available models, or a different training set) by adding some options. If they are not customised, they will run with the default options used for one of the experiments described in the paper. The available options are the following (which are equal for all models):

- -m = path to the model 
- -d = path to dataset folder 
- -dn = name of the dev file 
- -tn = name of the train file
- -src = language code (sq for Albanian, or pt for Portuguese)

The m2m script was also used for fine-tuning the small100 model.


Example (which is in the default use of the script):
```
python finetuningNMT-m2m.py -m "facebook/m2m100_418M" -d "data/" -dn "dev.tsv" -tn "train.tsv" -src "sq"
```

For fine-tuning NMT models, we strongly recommend using a good GPU (for the experiments described in the paper, we used an Nvidia RTX 4090 24GB). The fine-tuning process could potentially be run on CPU, but it would be extremely slow.


## Normalising the test set with baseline/fine-tuned models

After a model is fine-tuned, the best model will be saved to a folder that will look like this:

"m2m100_418M-finetuned-sq_orig-to-sq_mod/"

Inside this folder, there will be a few more folders that look like this:

"checkpoint-297/"

At the end of the fine-tuning step, the system will save the best model evaluated during the training and it will inform which checkpoint it was, so make sure to take note of that number as it will be in the name of the folder that should be loaded during the normalisation step.

Again there are three scripts for normalising texts (all starting with "translate-"). They all can be used with their default parameters, as in the fine-tuning step, but at least the folder of the fine-tuned model must be informed, for instance:

```
python translate-m2m.py -m "m2m100_418M-finetuned-sq_orig-to-sq_mod/checkpoint-297/"
```

It is also possible to load an already existing model, for instance: "facebook/m2m100_418M", which will then translate/normalise the source text using the non-fine-tuned model.

Further parameters/options that can be changed (for all models):

- -s = path to the source text (i.e. in our case the test set)
- -o = path for the output file (i.e. the file with normalised output)
- -tmx = indicate to the script that a TMX file should be generated at the end. Valid options are True or False (default=True).
- -e = indicate to the script that an evaluation file should be generated at the end (this file is used in the next step for evaluating the results). Valid options are True or False (default=True).
- -l = language code that should be used. Valid options are "sq" for Albanian, and "pt" for Portuguese.


## Evaluating the results

There is only one script for evaluating all models (including the rule-based model, despite the name of the script): `evaluate_NMT.py`

This script uses a source text, an automatically normalised output and a gold standard (a normalisation made by humans) as input, and produces a TSV file with an overall BLEU score for the whole set and an individual BLEU score for each sentence. This TSV file can also be used for error analysis, as it contains all three stages of the sentences (original, automatically normalised, and normalised by human).

If used as is, it will take as input an already existing normalisation produced with the OPUS fine-tuned model for the medical domain, as presented in the paper:

```
python evaluate_NMT.py
```

The options for this script are:

- -s = path to the source text with historical spelling. This is used only for generating the output with the three stages of the text. It is not used for computing BLEU scores
- -t = path to the automatically normalised text
- -g = path to the gold standard file
- -r = name of the results file that is going to be generated


