'''
Created on Mar 20, 2015

@author: nwolfeeeee
'''
import os

def main():
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
                print(f + " contains " + str(len(overlap)) + " GRE words... " + str(total_usage) + " mentions, avg: " + str(avg_usage) + "\n")
                
                
                
            
            

if __name__ == '__main__':
    main()