# pt-lex
Pronunciation Lexicon for European Portuguese

**pt-lex** is a pronunciation dictionary for European Portuguese. It was inspired by [CMUdict](https://github.com/cmusphinx/cmudict) and it is suitable for uses in speech technology.

Following the disclaimer of [CMUdict](https://github.com/cmusphinx/cmudict), I do not guarantee the accuracy of this dictionary, nor its suitability for any specific purpose. In fact, I expect a number of errors, omissions and inconsistencies to remain in the dictionary. 

Future updates may occur, but they are not guaranteed. These would be in the form of correcting existing entries or adding new ones, as well as a more accurate Grapheme-to-Phoneme (G2P) model. I welcome input from users. Please create issues or pull request, or simply email me directly.

Use of this dictionary for any research or commercial purposes is completely unrestricted.  If you make use of or redistribute this material we request that you acknowledge its origin in your descriptions. If you do so, please also let me know, as I would be happy to hear others are making use of these resources.
If you add or correct words in your version of this dictionary, please send these additions and corrections to me so this lexicon can also be improved.


## Contents

The directory **phoneset** contain a description of the phoneset used for this project.
`phoneset.html` is the html version of the phoneset, while `phoneset.yaml` is a identical version in YAML.

The directory **lex** contains the pronunciation lexicon. `lex.man` is a manually revised list of entries. `lex.auto` is an automatically generated list of entires using the G2P model in `g2p`. The file `lex.tail` contains an unannotated list of very low frequency words.

The directory **g2p** contains a Grapheme-to-Phoneme (G2P) model. This was trained using CMU's [Sequence-to-Sequence G2P toolkit](https://github.com/cmusphinx/g2p-seq2seq). This method jointly models grapheme-to-phoneme, syllabification, and stress assignment. The training data for this model was the manually revised list in `lex-man`. Using 2 layers with 64 nodes each and with the remaining default hyperparameters, this model achieves a WER of 53.8%. This is somewhat high, but note that this is over G2P, syllabification, and stress assignment, and currently there are only ~1000 manually revised entries. The unrevised sequences in `lex-auto` were decoded using the trained model.

To decode additional word lists (such as `lex.tail`) or otherwise manipulate the g2p model, please install the Sequence-to-Sequence G2P toolkit and follow the instructions in the original repository.

The directory **src** contains scripts that validate and manipulate the dictionaries.


## Vocabulary

The vocabulary list was extracted from the [wikimedia data dumps](https://dumps.wikimedia.org/ptwiki/latest), using the 2015-09-01 wikipedia article data dump. This version is no longer available, but a similar result can be achieved with the latest dumps. All articles were cleaned and a list of words was extracted. These were then sorted by frequency to form the final vocabulary.

This explains some of the entries in the `lex.auto` and the `lex.tail` lists. Although the automatic process identifies many unwanted sequences and ignores them, some are still preserved. The manual verification process should remove these words. The `lex.man` list is more accurate, since it has been through this process of manual verification.

The extraction and cleanup scripts are excluded here for simplificity. If you think you could benefit from them, contact me.


## Workflow

The overall workflow now involves manually revising automatically generated pronunciations from `lex.auto` and adding them to `lex.man`. Once a large number of entries has been revised, a new (and more accurate) G2P model can be trained. If you would like to contribute to this process, please get in touch.


## Future Work

Once a stable lexicon and G2P model has been created, future plans involve generating a basic Front-End for Text-To-Speech synthesis. This could then be used with other toolkits such as [Ossian](https://github.com/CSTR-Edinburgh/Ossian) or [Merlin](https://github.com/CSTR-Edinburgh/merlin) to develop basic open-source text-to-speech systems for European Portuguese.
