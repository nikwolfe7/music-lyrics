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

baseurl = "http://www.azlyrics.com/"
category = "hip_hop_rap"
azlyrics_search = "http://search.azlyrics.com/search.php?q="
#listfile = "hip-hop-rap-artists-current.list"
listfile = "hip-hop-rap-artists.list"
#listfile = "eric-b-rakim.list"
artist_websites = set()
lyrics_map = {}
seconds_to_wait = 3
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
	return re.sub("[<{(._'!?)}>]","",name).replace('&','and').replace('"','').replace('/','-').replace(' ','-').lower().strip()

def extract_azlyrics_name_url_from_anchor(a):
	a = str(a)
	url = a.split('"')[1]
	name = a.split('</a>')[0].split('>')[-1].strip()
	return (name,url.replace("../",baseurl))

def get_soup(url):
	print(url)
	wp = BeautifulSoup(urllib2.urlopen(url).read())
	delay(seconds_to_wait)
	return wp

def get_azlyrics_search_url(artist):
	artist = artist.replace(' ','+').replace('&','and').strip()
	return azlyrics_search + artist

def get_azlyrics_artist_url(search_url):
	wp = get_soup(search_url)
	searchwp = str(wp)
	result_marker = "Artist results:"
	if not result_marker in searchwp:
		print("No search results for "+search_url+" on azlyrics.com!")
		return False
	else:
		print("Found artist!")
		searchwp = [l.strip() for l in searchwp.split(result_marker)[-1].split("\n")]
		link_marker = '1. <a href="http://www.azlyrics.com/'
		for s in searchwp:
			if s.startswith(link_marker):
				s = s.split('"')[1]
				artist_websites.add(s)
				return s

def get_azlyrics_song_urls(artist_url):
	song_urls = []
	wp = get_soup(artist_url).findAll('a')
	song_prefix = '<a href="../lyrics/'
	for w in wp:
		if str(w).startswith(song_prefix):
			t = extract_azlyrics_name_url_from_anchor(w)
			song_urls.append(t)
	return song_urls

def clean_azlyrics_html(lyric_string):
	lyric_string = lyric_string.encode('ascii', 'ignore').decode('utf8')
	lyric_string = lyric_string.replace("&amp;","&").replace("&amp","&")
	lyric_string = lyric_string.replace("<i>","").replace("</i>","")
	lyric_string = lyric_string.replace("<br />","").replace("<br/>","")
	lyric_string = re.sub("[()]",'',lyric_string)
	return lyric_string

def write_azlyrics_song_to_file(song,artist):
	make_dir(category)
	clean_artist_name = clean_name(artist)
	make_dir(category+os.sep+clean_artist_name)
	song_file = category + os.sep + clean_artist_name + os.sep + clean_name(song[0]) + ".txt"
	try:
		print(song_file.encode('utf8','ignore'))
		if not check_is_file(song_file):
			song_wp = str(get_soup(song[1]))
			start = '<!-- start of lyrics -->'
			end = '<!-- end of lyrics -->'
			song_wp = song_wp.split(start)[-1].split(end)[0]
			clean_song_lyrics = clean_azlyrics_html(song_wp)
			print(clean_song_lyrics)
			song_file = open(song_file,"w")
			song_file.write(clean_song_lyrics)
			song_file.close()
		else: print(song_file + " already exists!")
	except UnicodeEncodeError: pass

if __name__ == "__main__":
	f = open(listfile).readlines()
	finished = False
	while not finished:
		try:
			for artist in artists:
					url = get_azlyrics_search_url(artist)
					artist_url = get_azlyrics_artist_url(url)
					if artist_url:
						song_urls = get_azlyrics_song_urls(artist_url)
						for song in song_urls:
							write_azlyrics_song_to_file(song,artist)
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
