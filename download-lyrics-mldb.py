import os
import sys
import re
import time
import http
try: import urllib.request as urllib2
except ImportError: import urllib2
try: import BeautifulSoup as BeautifulSoup
except ImportError: from bs4 import BeautifulSoup
from debug import debug

#http://search.mldb.com/search.php?q=ERIC+B.+%26+RAKIM
baseurl = "http://www.mldb.org/"
category = "hip_hop_rap"
pagenum = 0
mldb_search = "http://www.mldb.org/search?mq=[QUERY]&si=1&mm=1&ob="
#listfile = "hip-hop-rap-artists.list"
listfile = "hip-hop-rap-artists-current.list"
artist_websites = set()
lyrics_map = {}
seconds_to_wait = 0.1
retry_time = seconds_to_wait

def delay(s):
	print("Waiting "+str(s)+"s so we don't bother these assholes...")
	while s > 0:
		time.sleep(1)
		print(str(s)+"...")
		s += -1

def check_is_file(f):
	return os.path.exists(f)
		
def make_dir(name):
	try: os.stat(name)
	except: os.mkdir(name)

def clean_name(name):
	name = str(name)
	return re.sub("[<{(._'*#%@!?)}>]","",name).replace(os.sep,'').replace('&','and').replace('"','').replace('/','-').replace(' ','-').lower().strip()

def extract_mldb_name_url_from_anchor(a):
	a = str(a).split('">')
	url = baseurl + a[0]
	name = a[1].split('</a>')[0].strip()
	return (name,url)

def get_soup(url):
	wp = baseurl
	try:
		print(url)
	except UnicodeError as e: 
		print(e)
		url = wp
		pass
	wp = BeautifulSoup(urllib2.urlopen(url).read())
	#delay(seconds_to_wait)
	return wp
		
def get_mldb_search_url(artist):
	artist = artist.replace(' ','+').replace('&','and').strip()
	return mldb_search.replace('[QUERY]',artist)

'''
def get_mldb_artist_url(search_url):
	wp = get_soup(search_url)
	searchwp = str(wp)
	result_marker = "Artist results:"
	if not result_marker in searchwp:
		print("No search results for "+search_url+" on mldb.com!")
		return False
	else:
		print("Found artist!")
		searchwp = [l.strip() for l in searchwp.split(result_marker)[-1].split("\n")]
		link_marker = '1. <a href="http://www.mldb.com/'
		for s in searchwp:
			if s.startswith(link_marker):
				s = s.split('"')[1]
				artist_websites.add(s)
				return s
'''

def get_mldb_song_urls(artist_url, page, artist):
	
	song_urls = []
	wp = get_soup(artist_url + str(page))
	
	evens = wp.find_all('tr',attrs={"class":"h"})
	odds = wp.find_all('tr',attrs={"class":"n"})
	links = [(baseurl + a['href']) for a in wp.find_all('a',attrs={"onfocus":"this.blur()"})]

	# get the pagination!!!
	for l in links:
		wp = get_soup(l)
		evens += wp.find_all('tr',attrs={"class":"h"})
		odds += wp.find_all('tr',attrs={"class":"n"})
	
	wp = evens + odds 
	song_prefix = '<a href="song'
	
	for w in wp:
		try:
			# make sure artist name is in the string
			print(artist)
			cleaned_artist = clean_name(artist.lower().replace("the ","").strip()) #note the space...
			cleaned_artist_noand = clean_name(cleaned_artist.replace("-and","").strip())
			print(cleaned_artist)	
			cleaned_tr = clean_name(w)
			print(cleaned_tr)
			if str(cleaned_artist) in str(cleaned_tr) or str(cleaned_artist_noand) in str(cleaned_tr):
				print("Got it!")
				w = str(w).split('href="')[-1]
				t = extract_mldb_name_url_from_anchor(w)
				song_urls.append(t)
		except UnicodeEncodeError as e: 
			print("get_mldb_song_urls")
			print(e)
			pass
	

	return song_urls

def clean_mldb_html(lyric_string):
	lyric_string = lyric_string.encode('ascii', 'ignore').decode('utf8')
	lyric_string = lyric_string.replace("&amp;","&").replace("&amp","&")
	lyric_string = lyric_string.replace("<i>","").replace("</i>","")
	lyric_string = lyric_string.replace("<br />","").replace("<br/>","")
	lyric_string = re.sub("[()]",'',lyric_string)
	return lyric_string

def write_mldb_song_to_file(song,artist):
	make_dir(category)
	clean_artist_name = clean_name(artist)
	make_dir(category+os.sep+clean_artist_name)
	song_file = category + os.sep + clean_artist_name + os.sep + clean_name(song[0]) + ".txt"
	try:
		print(song_file)
		if not check_is_file(song_file):
			
			song_wp = get_soup(song[1]).find_all('p',attrs={"class":"songtext"})
			if len(song_wp):
				song_wp = song_wp[0].get_text()
				clean_song_lyrics = clean_mldb_html(song_wp)
				print(clean_song_lyrics)
			
				song_file = open(song_file,"w")
				song_file.write(clean_song_lyrics)
				song_file.close()

			else:
				check_if_done = get_soup(song[1]).find_all('td',attrs={"class":"centerplane"})
				if len(check_if_done):
					message = clean_mldb_html(check_if_done[0].get_text())
					done_for_today = "You viewed more than 300 lyrics for today! You are banned for 2 days.Please avoid viewing more than 300 lyrics for one day if you don't want to be banned again.If you get banned more than 3 times you will be banned for an year."
					if done_for_today in message:
						print("\n\n###############################################\n"
							"Time for a new IP address, mang! They onto you!\n"
							"###############################################\n\n")
						sys.exit(0)
		
		else: print(song_file + " already exists!")
	except UnicodeEncodeError as e: 
		print("write_mldb_song_to_file")
		print(e)
		pass

if __name__ == "__main__":
	
	artists = [l.split(",")[0] for l in open(listfile).readlines()]
	finished = False
	while not finished:
		try:
			for artist in artists:

					# 1.) SEARCH db
					url = get_mldb_search_url(artist)

					# 2.) GET ARTIST OR RESULTS
					# artist_url = get_mldb_artist_url(url)

					if url:

						# 3.) SONG URLs
						song_urls = get_mldb_song_urls(url, pagenum, artist)
						
						for song in song_urls:
							write_mldb_song_to_file(song,artist)

			# only if we complete the artist loop...
			finished = True

		except http.client.BadStatusLine:
			print("These fucking assholes are delaying you again...")
			print("Last time we waited a while... "+str(retry_time)+ "s... ")
			if retry_time > 30: 
				retry_time *= 2
				seconds_to_wait += 1
			else: retry_time += 5
			delay(retry_time)
