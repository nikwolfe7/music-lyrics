from collections import Counter
'''
Created on Mar 20, 2015

@author: nwolfeeeee
'''
import os

def main():
    original_size = 1000
    vocab_size = original_size
    GRE = set([l.strip() for l in open("GRE.txt").readlines()])
    for root, dirs, files in os.walk(".", topdown=True):
        for f in files:
            if f.endswith("unigram_word_ranks.csv"):
                print("File: "+f)
                words = set([l.strip() for l in open(f).readlines()])
                overlap = GRE.intersection(set([w.split(",")[0] for w in words]))
                #print(overlap)
                total_usage = 0
                sorted_words = []
                for word in words:
                    w = word.split(",")[0]
                    if w in overlap:
                        count = int(word.split(",")[-1])
                        total_usage += count
                        sorted_words.append((w,count))
                
                sorted_words = sorted(sorted_words, key=lambda x: x[1], reverse=True)
                avg_usage = float(total_usage) / len(overlap)         
                print(sorted_words)
                print(f + " contains " + str(len(overlap)) + " GRE words... " + str(total_usage) + " mentions, avg: " + str(avg_usage))
                
                # pseudocount smooting for GRE words...
                while vocab_size < 250000:
                    words = [(l.split(",")[0], int(l.split(",")[-1])) for l in open(f).readlines()]
                    #words += [(word,1) for word in list(GRE)]
                    words = words[:vocab_size]
                    unigram = {}
                    for word in words: unigram[word[0]] = word[1]
                    total = sum(unigram.values())
                    for word in unigram: unigram[word] = unigram[word] / total
                    
                    gre_score = 0.0
                    for word in GRE: 
                        try:
                            gre_score += unigram[word]
                        except KeyError as e: continue
                            
                    print("Total probability of GRE vocabulary in " + f + ": " + str(gre_score) + " with vocab size: " + str(vocab_size))
                    vocab_size += 25000
                
                print("\n")
                vocab_size = original_size
                
if __name__ == '__main__':
    main()