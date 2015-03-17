import os
import sys
import wikipedia
import re
try: import urllib.request as urllib2
except ImportError: import urllib2
try: import BeautifulSoup as BeautifulSoup
except ImportError: from bs4 import BeautifulSoup
from debug import debug

#w1 = "http://en.wikipedia.org/wiki/List_of_hip_hop_musicians"
#w1 = "http://www.ranker.com/list/top-ten-greatest-90_s-rock-bands/styx88?format=GRID"
#w1 = "http://www.ranker.com/list/grunge-music-bands-and-musicians/reference"
#w1 = "http://digitaldreamdoor.com/pages/best_songs90s.html"
w1 = "http://en.wikipedia.org/wiki/List_of_hard_rock_musicians_(A%E2%80%93M)"
w2 = "http://en.wikipedia.org/wiki/List_of_hard_rock_musicians_(N%E2%80%93Z)"
years = ['1990','1991','1992','1993','1994','1995','1996','1997','1998','1999']
startwords = ['formed','begun','started','began','founded','first']
websites = [w1,w2]

#base_url = "http://" + website.replace("http://","").split(os.sep)[0]
rock = {}
hip_hop = {}
rock_file = 'rock-metal-country.txt'
hip_hop_file = 'hip-hop-rap.txt'

current_list = rock
current_file = rock_file

def rename_file(name):
	al.rename_file(name, os.getcwd())

def make_dir(name):
	try: os.stat(name)
	except: os.mkdir(name)

def print_shit():
	print("printing shit!")
	f = open(current_file,'a')
	for h in current_list.keys(): f.write(h+'\n')
	f.close()
	print("Done printing shit!")

def check_summary(result):
	ok = False
	sents = result.split(".")[:2]
	for sentence in sents:
		if any(x in sentence for x in startwords):
			if any(y in sentence for y in years):
				ok = True
				print(result)
	return ok

def go_get_stuff(soup):
	links = []

	##########################################################
	#w1 = "http://en.wikipedia.org/wiki/List_of_hip_hop_musicians"
	#w1 = "http://en.wikipedia.org/wiki/List_of_hard_rock_musicians_(A%E2%80%93M)"
	#w2 = "http://en.wikipedia.org/wiki/List_of_hard_rock_musicians_(N%E2%80%93Z)"
	
	stuff = [str(s) for s in soup.findAll('li')]
	pattern = '<li><a href="/wiki/'
	for s in stuff:
		if pattern in s:
			s = s.split('</a>')[0].split('">')[-1].replace('&amp;','&').strip()
			if len(s): 
				print("Artist: "+s)
				try:
					result = wikipedia.summary(s)
					if check_summary(result):
						current_list[s] = True

				except Exception:
					print('woops')
					try:
						result = wikipedia.summary(s + " (band)")
						if check_summary(result):
							current_list[s] = True
						
					except Exception:
						print('woops')
						try:
							result = wikipedia.summary(s + " (musician)")
							if check_summary(result):
								current_list[s] = True
						except Exception:
							print('woops')

	debug(current_list)
	print_shit()
	


	##########################################################
	'''
	w1 = "http://www.billboard.com/archive/charts/1990/rap-song"
	w2 = "http://www.billboard.com/archive/charts/1991/rap-song"
	w3 = "http://www.billboard.com/archive/charts/1992/rap-song"
	w4 = "http://www.billboard.com/archive/charts/1993/rap-song"
	w5 = "http://www.billboard.com/archive/charts/1994/rap-song"
	w6 = "http://www.billboard.com/archive/charts/1995/rap-song"
	w7 = "http://www.billboard.com/archive/charts/1996/rap-song"
	w8 = "http://www.billboard.com/archive/charts/1997/rap-song"
	w9 = "http://www.billboard.com/archive/charts/1998/rap-song"
	w10 = "http://www.billboard.com/archive/charts/1999/rap-song"
	current_list = {}
	stuff = soup.prettify().split('tbody')[1].split('td')
	pattern='class="views-field views-field-field-chart-item-artist"'
	for s in stuff:
		if pattern in s:
			s = s.split('&gt;')
			for i in xrange(len(s)):
				sub = s[i]
				if i == 1:
					sub = sub.split('&lt;')[0].strip().replace('&amp;','&')
					if len(sub.strip()):
						current_list[sub.strip()] = True
				if i == 2:
					sub = sub.replace('&lt;','').replace('&gt','').replace('/a','')
					if len(sub.strip()):
						current_list[sub.strip()] = True

	debug(current_list)
	print_shit()
	'''

	##########################################################
	'''
	w1 = "http://www.billboard.com/archive/charts/1990/alternative-songs"
	w2 = "http://www.billboard.com/archive/charts/1990/hot-mainstream-rock-tracks"
	w3 = "http://www.billboard.com/archive/charts/1990/country-songs"
	w4 = "http://www.billboard.com/archive/charts/1990/country-airplay"
	w5 = "http://www.billboard.com/archive/charts/1990/country-albums"

	w6 = "http://www.billboard.com/archive/charts/1991/alternative-songs"
	w7 = "http://www.billboard.com/archive/charts/1991/hot-mainstream-rock-tracks"
	w8 = "http://www.billboard.com/archive/charts/1991/country-songs"
	w9 = "http://www.billboard.com/archive/charts/1991/country-airplay"
	w10 = "http://www.billboard.com/archive/charts/1991/country-albums"

	w11 = "http://www.billboard.com/archive/charts/1992/alternative-songs"
	w12 = "http://www.billboard.com/archive/charts/1992/hot-mainstream-rock-tracks"
	w13 = "http://www.billboard.com/archive/charts/1992/country-songs"
	w14 = "http://www.billboard.com/archive/charts/1992/country-airplay"
	w15 = "http://www.billboard.com/archive/charts/1992/country-albums"

	w16 = "http://www.billboard.com/archive/charts/1993/alternative-songs"
	w17 = "http://www.billboard.com/archive/charts/1993/hot-mainstream-rock-tracks"
	w18 = "http://www.billboard.com/archive/charts/1993/country-songs"
	w19 = "http://www.billboard.com/archive/charts/1993/country-airplay"
	w20 = "http://www.billboard.com/archive/charts/1993/country-albums"

	w21 = "http://www.billboard.com/archive/charts/1994/alternative-songs"
	w22 = "http://www.billboard.com/archive/charts/1994/hot-mainstream-rock-tracks"
	w23 = "http://www.billboard.com/archive/charts/1994/country-songs"
	w24 = "http://www.billboard.com/archive/charts/1994/country-airplay"
	w25 = "http://www.billboard.com/archive/charts/1994/country-albums"

	w26 = "http://www.billboard.com/archive/charts/1995/alternative-songs"
	w27 = "http://www.billboard.com/archive/charts/1995/hot-mainstream-rock-tracks"
	w28 = "http://www.billboard.com/archive/charts/1995/country-songs"
	w29 = "http://www.billboard.com/archive/charts/1995/country-airplay"
	w30 = "http://www.billboard.com/archive/charts/1995/country-albums"

	w31 = "http://www.billboard.com/archive/charts/1996/alternative-songs"
	w32 = "http://www.billboard.com/archive/charts/1996/hot-mainstream-rock-tracks"
	w33 = "http://www.billboard.com/archive/charts/1996/country-songs"
	w34 = "http://www.billboard.com/archive/charts/1996/country-airplay"
	w35 = "http://www.billboard.com/archive/charts/1996/country-albums"

	w36 = "http://www.billboard.com/archive/charts/1996/alternative-songs"
	w37 = "http://www.billboard.com/archive/charts/1996/hot-mainstream-rock-tracks"
	w38 = "http://www.billboard.com/archive/charts/1996/country-songs"
	w39 = "http://www.billboard.com/archive/charts/1996/country-airplay"
	w40 = "http://www.billboard.com/archive/charts/1996/country-albums"

	w41 = "http://www.billboard.com/archive/charts/1997/alternative-songs"
	w42 = "http://www.billboard.com/archive/charts/1997/hot-mainstream-rock-tracks"
	w43 = "http://www.billboard.com/archive/charts/1997/country-songs"
	w44 = "http://www.billboard.com/archive/charts/1997/country-airplay"
	w45 = "http://www.billboard.com/archive/charts/1997/country-albums"

	w46 = "http://www.billboard.com/archive/charts/1998/alternative-songs"
	w47 = "http://www.billboard.com/archive/charts/1998/hot-mainstream-rock-tracks"
	w48 = "http://www.billboard.com/archive/charts/1998/country-songs"
	w49 = "http://www.billboard.com/archive/charts/1998/country-airplay"
	w50 = "http://www.billboard.com/archive/charts/1998/country-albums"

	w51 = "http://www.billboard.com/archive/charts/1999/alternative-songs"
	w52 = "http://www.billboard.com/archive/charts/1999/hot-mainstream-rock-tracks"
	w53 = "http://www.billboard.com/archive/charts/1999/country-songs"
	w54 = "http://www.billboard.com/archive/charts/1999/country-airplay"
	w55 = "http://www.billboard.com/archive/charts/1999/country-albums"

	stuff = [s.get_text().strip() for s in soup.find_all(attrs={'href':re.compile('^/artist/')})]
	for s in stuff:
		print(s)
		current_list[s] = True

	print(current_list)
	print_shit()
	'''


	##########################################################
	#w1 = "http://www.billboard.com/archive/charts/1990/r-b-hip-hop-songs"
	'''
	w1 = "http://www.billboard.com/archive/charts/1990/r-b-hip-hop-songs"
	w2 = "http://www.billboard.com/archive/charts/1991/r-b-hip-hop-songs"
	w3 = "http://www.billboard.com/archive/charts/1992/r-b-hip-hop-songs"
	w4 = "http://www.billboard.com/archive/charts/1993/r-b-hip-hop-songs"
	w5 = "http://www.billboard.com/archive/charts/1994/r-b-hip-hop-songs"
	w6 = "http://www.billboard.com/archive/charts/1995/r-b-hip-hop-songs"
	w7 = "http://www.billboard.com/archive/charts/1996/r-b-hip-hop-songs"
	w8 = "http://www.billboard.com/archive/charts/1997/r-b-hip-hop-songs"
	w9 = "http://www.billboard.com/archive/charts/1998/r-b-hip-hop-songs"
	w10 = "http://www.billboard.com/archive/charts/1999/r-b-hip-hop-songs"
	
	stuff = soup.prettify().split('tbody')[1].split('\n')
	pattern='a href="/artist/'
	for s in stuff:
		if pattern in s:
			s = s.split(';')
			for i in xrange(len(s)):
				sub = s[i]
				if i == 2:
					sub = sub.replace('&lt','').replace('&gt','')
					print("i = "+ str(i) + " " + sub)	
					if len(sub.strip()):
						current_list[sub.strip()] = True

	debug(current_list)
	print_shit()
	'''

	##########################################################
	# w1 = http://digitaldreamdoor.com/pages/best_songs90s.html
	'''
	stuff = [s.get_text().strip() for s in soup.findAll('span')]
	debug(stuff)
	debug(len(stuff))
	for a in stuff:
		if len(a) and a.startswith("- "):
			a = a.replace("- ","").strip()
			current_list[a.strip()] = True

	debug(current_list)
	print_shit()
	'''

	##########################################################
	# w1 = "http://digitaldreamdoor.com/pages/best_rap-alb-90.html"	
	'''
	stuff = soup.findAll('span')
	#debug(len(stuff))
	for s in stuff:
		a = s.contents[0].encode('utf8').strip()
		if len(a) and "-" in a:
			a = a.strip("- ").strip(a.split()[-1]).replace(" (1999","").replace('&amp;','&')
			debug(a)
			current_list[a.strip()] = True

	debug(current_list)
	print_shit()
	'''

	##########################################################
	'''
	w1 = "http://rateyourmusic.com/list/diction/90s_hip_hop__top_250/1/"
	w2 = "http://rateyourmusic.com/list/diction/90s_hip_hop__top_250/2/"
	w3 = "http://rateyourmusic.com/list/diction/90s_hip_hop__top_250/3/"
	w4 = "http://rateyourmusic.com/list/diction/90s_hip_hop__top_250/4/"
	w5 = "http://rateyourmusic.com/list/diction/90s_hip_hop__top_250/5/"
	w6 = "http://rateyourmusic.com/list/diction/90s_hip_hop__top_250/6/"
	w7 = "http://rateyourmusic.com/list/diction/90s_hip_hop__top_250/7/"
	w8 = "http://rateyourmusic.com/list/diction/90s_hip_hop__top_250/8/"
	w9 = "http://rateyourmusic.com/list/diction/90s_hip_hop__top_250/9/"
	w10 = "http://rateyourmusic.com/list/diction/90s_hip_hop__top_250/10/"
	
	stuff = soup.findAll(attrs={'class' : 'list_artist'})
	#debug(len(stuff))
	for s in stuff:
		a = s.contents[0].encode('utf8').strip()
		print(a)
		if len(a):
			current_list[a] = True

	debug(current_list)
	#print_shit()
	'''

	##########################################################
	#w1 = "http://www.ranker.com/list/best-_90s-rappers-v1/whatevayoulike"
	'''
	stuff = soup.findAll(attrs={'itemprop' : 'name', 'class' : 'block oNode'})
	#debug(len(stuff))
	for s in stuff:
		a = s.contents[0].encode('utf8').strip()
		print(a)
		if len(a):
			current_list[a] = True

	debug(current_list)
	print_shit()
	'''

	##########################################################
	#w1 = "http://www.ranker.com/list/complex-and-_39_s-90-best-rap-albums-of-the-90s/complex?page=1"
	#w2 = "http://www.ranker.com/list/complex-and-_39_s-90-best-rap-albums-of-the-90s/complex?page=2"
	'''
	stuff = soup.findAll(attrs={'class' : 'block grey data dataColumn'})
	#debug(len(stuff))
	for s in stuff:
		a = s.contents[0].encode('utf8').strip()
		print(a)
		if len(a):
			current_list[a] = True

	debug(current_list)
	print_shit()
	'''

	##########################################################
	#w1 = "http://www.ranker.com/list/the-10-best-rappers-of-the-_90s/complex"
	#w1 = "http://www.ranker.com/list/best-hard-rock-cd-and-_39_s-of-the-90-and-_39_s/scarcrifice?page=1"
	#w2 = "http://www.ranker.com/list/best-hard-rock-cd-and-_39_s-of-the-90-and-_39_s/scarcrifice?page=2"
	#w3 = "http://www.ranker.com/list/best-hard-rock-cd-and-_39_s-of-the-90-and-_39_s/scarcrifice?page=3"
	#w4 = "http://www.ranker.com/list/best-hard-rock-cd-and-_39_s-of-the-90-and-_39_s/scarcrifice?page=4"
	#w5 = "http://www.ranker.com/list/best-hard-rock-cd-and-_39_s-of-the-90-and-_39_s/scarcrifice?page=5"
	#w6 = "http://www.ranker.com/list/best-hard-rock-cd-and-_39_s-of-the-90-and-_39_s/scarcrifice?page=6"
	# ex: <span class="block grey data dataColumn"> Dangerous Toys</span>
	'''
	stuff = [s.get_text().strip() for s in soup.find_all('span', attrs={'class' : 'block grey data dataColumn'})]
	debug(stuff)
	debug(len(stuff))
	for s in stuff:
		if len(s):
			current_list[s] = True

	debug(current_list)
	print_shit()
	'''

	##########################################################
	#w1 = "http://www.ranker.com/list/the-10-best-rappers-of-the-_90s/complex"
	'''
	stuff = soup.findAll(attrs={'itemprop' : 'name', 'class' : 'block oNode'})
	debug(len(stuff))
	for s in stuff:
		a = s.contents[0].encode('utf8').strip()
		current_list[a] = True

	debug(current_list)
	print_shit()
	'''

	##########################################################
	#w1 = "http://www.ranker.com/crowdranked-list/best-_90s-rappers?page=2&format=GRID"
	#w2 = "http://www.ranker.com/crowdranked-list/best-_90s-rappers"
	#w1 = "http://www.ranker.com/list/top-ten-greatest-90_s-rock-bands/styx88?format=GRID"
	#w1 = "http://www.ranker.com/list/grunge-music-bands-and-musicians/reference"
	#w1 = "http://www.ranker.com/list/best-selling-grunge-bands/music-lover"
	#w2 = "http://www.ranker.com/crowdranked-list/greatest-artists-of-the-_90s?page=1"
	#w3 = "http://www.ranker.com/crowdranked-list/greatest-artists-of-the-_90s?page=2"
	#w4 = "http://www.ranker.com/crowdranked-list/greatest-artists-of-the-_90s?page=3"
	#w5 = "http://www.ranker.com/crowdranked-list/greatest-artists-of-the-_90s?page=4"
	#w6 = "http://www.ranker.com/crowdranked-list/greatest-artists-of-the-_90s?page=5"
	#w1 = "http://www.ranker.com/list/90s-seattle-grunge-bands/dan808"
	'''
	stuff = soup.findAll(attrs={'itemprop' : 'name', 'class' : 'block oNode'})
	debug(stuff)
	debug(len(stuff))
	for s in stuff:
		a = str(s.contents[0]).strip()
		current_list[a] = True

	debug(current_list)
	print_shit()
	'''
	##########################################################



	##########################################################
	#website = "http://kzok.cbslocal.com/2011/07/14/100-greatest-rock-artists-of-the-1990s/"
	'''
	use = False
	items = [l.strip() for l in str(soup).split('tbody')[1].split('\n')][2:]
	i = 0
	pastfifty = False
	while i < len(items):
		item = items[i]
		if not item.endswith('</strong></span></a></td>'):
			i += 1
			index = i
			if pastfifty: index = i-1
			sp = str(i)+". "
			line = item.split(str(index)+". ")[-1].replace('<br />','').replace('&#8217;',"'").replace('&amp;','&')
			if line.startswith('<span style="color:#990000;">'):
				line = line.replace('<span style="color:#990000;">','').replace('</span>','')
				if not "<" in line:
					print("i = "+str(i)+" current_list: " + line)
					current_list[line] = True
			else:
				if not "<" in line:
					print("i = "+str(i)+" rock: "+line)
					rock[line] = True
		else:
			i += 1 
			pastfifty = True
	print_shit()
	'''

	##########################################################
	# old shit
	'''
	for a in soup('a'):
		try:
			href = a['href']
			for f in filetypes:
				if href.endswith(f):
					print("Found: " + href)
					use = True
					break
		except: pass
		if not use: continue
		try:
			links.append(a['href'])
		except: continue
	for name in links:
		for l in langs:
			if l.lower() in name.lower():
				arrange_audio(name,l)
	'''

for website in websites:
	soup = BeautifulSoup(urllib2.urlopen(website).read())
	go_get_stuff(soup)