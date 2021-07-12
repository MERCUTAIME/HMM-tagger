# HMM-tagger
You can run the POS tagger by typing the following at a command line:

$ python3 tagger.py -d <training file names> -t <test file name> -o <output file name>
where the parameters consist of:

a series of training files (pairings between words and POS tags),
a single input test file, and
a single output file (containing the words from the test file, paired with each word's POS tag).
