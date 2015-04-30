import os
import sys
import re
import time
import http
import wget
import codecs
from piston_mini_client.serializers import get_serializer
try: import urllib.request as urllib2
except ImportError: import urllib2
try: import BeautifulSoup as BeautifulSoup
except ImportError: from bs4 import BeautifulSoup
from debug import debug

#===================================================================#
# CONSTANTS --------------------------------------------------------#
#===================================================================#
baseurl = "http://www.midiworld.com/"
category = sys.argv[1]
check_folder = "MIDICheck"
search = "http://www.midiworld.com/search/?q="
#listfile = "hip-hop-rap-artists-current.list"
listfile = sys.argv[2]
artist_song_urls_db = "MIDI_artist_song_urls.list"
possibly_unnecessary_words = ['the','ft']
lyrics_map = {}
seconds_to_wait = 0
retry_time = seconds_to_wait
no_result_marker = "found nothing!"
content_link_identifier = "download"
def is_content_link(link): return link.text == content_link_identifier
def get_result_marker(search_wp): return (no_result_marker in search_wp) 
def is_correct_file(artist, song_file): return (str_regex(artist).replace(" ","_") + "_-_").lower() in song_file.lower()
def str_regex(string): return re.sub("[<{(._'!?)}>]","",string)
#===================================================================#
# CONSTANTS --------------------------------------------------------#
#===================================================================#

def get_file_contents(filename):
	return [l.strip() for l in codecs.open(filename,'r','utf-8').readlines()]

def update_url_list(url_list):
	if check_is_file(artist_song_urls_db):
		curr = set(get_file_contents(artist_song_urls_db))
		url_list = url_list | curr
		f = open(artist_song_urls_db,'w')
		for url in url_list: f.write(url+"\n")
		f.close()
		return url_list.difference(curr)
	else:
		f = open(artist_song_urls_db,'w')
		for url in url_list: f.write(url+"\n")
		f.close()
		return url_list
		
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
	return str_regex(name).replace('&','and').replace('"','').replace('/','-').replace(' ','-').lower().strip()

def get_soup(url):
	print(url)
	delay(seconds_to_wait)
	web_response = urllib2.urlopen(url)
	wp = BeautifulSoup(web_response.read())
	return wp

def get_site_urls(url):
	links = []
	for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
		if link.has_attr('href'):
			print(str(link['href']))
			links.append(link)
        	

def get_search_url(artist):
	artist = str_regex(artist).replace(' ','+').replace('&','and').strip()
	return search + artist

def get_artist_urls(artist):
	artist_song_urls = set()
	urls = [get_search_url(artist)]
	for word in possibly_unnecessary_words: 
		if word.lower() in artist.lower():
			urls.append(get_search_url(artist.lower().replace(word.lower(),"").strip()))
	
	for search_url in urls:
		wp = get_soup(search_url)
		search_wp = str(wp)
		if get_result_marker(search_wp):
			print("No search results for "+search_url+" on "+baseurl)
		else:
			print("Found artist!")
			retval = False
			for link in wp.findAll('a'):
				if is_content_link(link):
					retval = True
					artist_song_urls.add(link.attrs['href'])
	return artist_song_urls

def download_midi(artist, url):
	make_dir(category)
	clean_artist_name = clean_name(artist)
	make_dir(category+os.sep+clean_artist_name)
	song_file = wget.download(url)
	if not check_is_file(category+os.sep+clean_artist_name+os.sep+song_file):
		if is_correct_file(artist, song_file):
			os.rename(song_file, category+os.sep+clean_artist_name+os.sep+song_file)
		else: os.rename(song_file, check_folder + os.sep + song_file)
	else: os.remove(song_file)

if __name__ == "__main__":
	artists = [l.split(',')[0] for l in get_file_contents(listfile)]
	make_dir(check_folder)
	finished = False
	while not finished:
		try:
			for artist in artists: 
				artist_song_urls = get_artist_urls(artist)
				artist_song_urls = update_url_list(artist_song_urls)
				for url in artist_song_urls:
					download_midi(artist, url)
				
			# only if we complete the artist loop...
			finished = True
		except Exception as e:
			print(e)
			print("These fucking assholes are delaying you again...")
			print("Last time we waited a while... "+str(retry_time)+ "s... ")
			if retry_time > 30: 
				retry_time *= 2
				seconds_to_wait += 1
			else: retry_time += 5
			delay(retry_time)
