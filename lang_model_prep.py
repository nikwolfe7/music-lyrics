import os
import wordstats
from collections import Counter
'''
Created on Mar 23, 2015

@author: nwolfe
'''
# ===================================== #
# STUFF YOU CAN CHANGE
# ===================================== #
corpus_name = "shakespeare"
directory = corpus_name
output = "lang_model"
remove_stops = True
filetype = ".txt"
# ===================================== #
# STUFF YOU LEAVE ALONE
# ===================================== #

def clean_brown_line(line):
    if not "/" in line: return line
    cleaned = ["\t"]
    for word in line.split():
        if not "``" in word and not "''" in word:
            cleaned.append(word.split("/")[0])
    return " ".join(cleaned)
    

def make_dir(name):
    try: os.stat(name)
    except: os.mkdir(name)
    
def main():
    make_dir(output)
    train_data = []
    test_data = []
    count = 1
    for root, dirs, files in os.walk(directory, topdown=True):
        for dir in dirs:
            print("Artist: "+dir)
        for f in files:
            if f.endswith(filetype):
                print("Document: " + f)
                f = os.path.abspath(root + os.sep + f)
                data = [l.strip() for l in open(f).readlines() if l.strip() != ""]
                for line in data:
                    line = clean_brown_line(line)
                    wordstats.remove_stops = remove_stops
                    (a, b, c, bow, e) = wordstats.get_song_stats(line.split(), oneline=True, suppress_output=True)
                    if count % 10 == 0:
                        test_data.append(bow)
                    else:
                        train_data.append(bow)
                    count += 1
    # output stuff
    if remove_stops: o = open(output + os.sep + corpus_name + ".train.nostop.txt","w")
    else: o = open(output + os.sep + corpus_name + ".train.txt","w") 
    for line in train_data: o.write(" ".join(line) + "\n")
    o.close()
    
    if remove_stops: o = open(output + os.sep + corpus_name + ".test.nostop.txt","w")
    else: o = open(output + os.sep + corpus_name + ".test.txt","w")
    for line in test_data: o.write(" ".join(line) + "\n")
    o.close()
    
    # vocab file
    linear_train_data = []
    for line in train_data: linear_train_data += line
    linear_train_data = Counter(linear_train_data)
    linear_train_data = sorted(linear_train_data.items(), key=lambda x: x[1], reverse=True)
    
    if remove_stops: o = open(output + os.sep + corpus_name + ".nostop.vocab","w")
    else: o = open(output + os.sep + corpus_name + ".vocab","w")
    for word in linear_train_data: o.write(word[0] + "\n")
    o.close()
    
        
    

if __name__ == '__main__':
    main()
    