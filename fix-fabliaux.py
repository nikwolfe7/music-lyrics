import os
directory="le_fabliaux"
 
def main():
    for root, dirs, files in os.walk(directory, topdown=True):
        for dir in dirs:
            print("Artist: "+dir)
        for f in files:
            print(f)
            splitext = []
            lines = [l.strip() for l in open(os.path.abspath(root + os.sep + f)).readlines()]
            for line in lines:
                line = line.replace(". . .",".")
                splitext += line.split(".")
            o = open(os.path.abspath(root + os.sep + f), "w")
            for line in splitext: o.write(line + "\n")
            o.close()
            
            
if __name__ == '__main__': main()