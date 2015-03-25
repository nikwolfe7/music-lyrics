#!/bin/bash
VOCAB=".vocab"
TRAIN=".train.txt"
TEST=".test.txt"
VOCAB_NOSTOP=".nostop.vocab"
TRAIN_NOSTOP=".train.nostop.txt"
TEST_NOSTOP=".test.nostop.txt"
BROWN="brown"
HHR="hip_hop_rap"
RMC="rock_metal_country"
SONNETS="shakespeare_sonnets"
SHAKESPEARE="shakespeare"
LE_FABLIAUX="le_fabliaux"
DISCOUNT_METHOD="-skip"

UNIGRAM_MODEL=".unigram.txt"
BIGRAM_MODEL=".bigram.txt"
TRIGRAM_MODEL=".trigram.txt"
FOURGRAM_MODEL=".fourgram.txt"

function compute_ngram {
	printf "\n\nComputing n-grams models for "$1" corpus...\n"
	printf "\nUnigram Model:\n"
	ngram-count -order 1 -lm $1$UNIGRAM_MODEL -text $1$TRAIN $DISCOUNT_METHOD -write-vocab $1$VOCAB".srilm.txt"
	ngram -lm $1$UNIGRAM_MODEL -ppl $1$TEST
	printf "\nUnigram Model (Stop words removed):\n"
	ngram-count -order 1 -lm $1$UNIGRAM_MODEL -text $1$TRAIN_NOSTOP $DISCOUNT_METHOD -write-vocab $1$VOCAB_NOSTOP".srilm.txt"
	ngram -lm $1$UNIGRAM_MODEL -ppl $1$TEST_NOSTOP

	printf "\nBigram Model:\n"
	ngram-count -order 2 -lm $1$BIGRAM_MODEL -text $1$TRAIN $DISCOUNT_METHOD
	ngram -lm $1$BIGRAM_MODEL -ppl $1$TEST
	printf "\nBigram Model (Stop words removed):\n"
	ngram-count -order 2 -lm $1$BIGRAM_MODEL -text $1$TRAIN_NOSTOP $DISCOUNT_METHOD
	ngram -lm $1$BIGRAM_MODEL -ppl $1$TEST_NOSTOP

	printf "\nTrigram Model:\n"
	ngram-count -order 3 -lm $1$TRIGRAM_MODEL -text $1$TRAIN $DISCOUNT_METHOD
	ngram -lm $1$TRIGRAM_MODEL -ppl $1$TEST
	printf "\nTrigram Model (Stop words removed):\n"
	ngram-count -order 3 -lm $1$TRIGRAM_MODEL -text $1$TRAIN_NOSTOP $DISCOUNT_METHOD
	ngram -lm $1$TRIGRAM_MODEL -ppl $1$TEST_NOSTOP
}

compute_ngram $BROWN
compute_ngram $HHR
compute_ngram $RMC
compute_ngram $SONNETS
compute_ngram $SHAKESPEARE
compute_ngram $LE_FABLIAUX
