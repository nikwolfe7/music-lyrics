import sys
import operator
from debug import debug
from collections import Counter

#txtfile = 'hip-hop-rap.txt'
#checkfile = 'rock-metal-country.txt'
txtfile = 'hip-hop-rap.txt'

def clean_list(clist):
	for i in range(len(clist)):
		l = clist[i]
		l = l.replace('&amp;','&').replace('&amp','&').replace('&#039',"'").replace('and','&').strip("[]()").upper().replace("FEATURING","FEAT.")
		clist[i] = l	
	return clist

f = [l.strip() for l in open(txtfile).readlines()]
#check = [l.strip() for l in open(checkfile).readlines()]

f = clean_list(f)
#check = clean_list(check)

#diff = set(f) - set(check)

c = Counter(f)
#for item in c.keys():
#	if not item in diff:
#		c[item] = 0

sorted_c = sorted(c.items(), key=operator.itemgetter(1), reverse=True)
f = open(txtfile.replace(".txt","-artists.list"),"w")

for artist in sorted_c:
	if artist[1]:
		f.write(artist[0] + "," + str(artist[1]) + "\n")
f.close()
