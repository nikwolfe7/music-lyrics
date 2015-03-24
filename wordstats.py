import os
from collections import Counter
from debug import debug
import codecs
import re

#=========================================#
# STUFF YOU CHANGE
#=========================================#
#folder = "test_data"
folder = "brown_corpus"
#folder = "rock_metal_country"
#folder = "shakespeare"
#folder = "le_fabliaux"
subfolder = "data"
#=========================================#
# STUFF YOU LEAVE ALONE
#=========================================#

stuff = []
counter = Counter()
artist_document_map = {}

song_stats = folder + "_song_stats.csv"
artist_stats = folder + "_artist_stats.csv"
genre_stats = folder + "_genre_stats.csv"
unigram_word_rank = folder + "_unigram_word_ranks.csv"
bigram_word_rank = folder + "_bigram_word_ranks.csv"
trigram_word_rank = folder + "_trigram_word_rank.csv"

stops = ['the','a','you','i','to','of','and','me','my','in','it','on',"i'm",'that','we','your','for','like','be','is','with']
remove_stops = True

#debug(line)
#debug(counter)
#print("Word Types: "+str(len(counter.keys())))
#print("Word Tokens: "+str(len(stuff)))

def make_dir(name):
	try: os.stat(name)
	except: os.mkdir(name)

def write_ngram_stats(ngram, filename):
	f = open(subfolder + os.sep + filename,'a')
	for n in ngram:
		csv = ",".join([str(n[0]),str(n[1])])
		f.write(str(csv.encode(encoding='ascii', errors='replace').decode()) + "\n")
	f.close()

def new_s_stat(): 
	return Counter(['ARTIST','SONG','TYPES','TOKENS','AVG_LINE_LENGTH','MOST_COMMON_WORD','MOST_COMMON_BIGRAM','MOST_COMMON_TRIGRAM'])

def write_s_stat(s): 
	f = open(subfolder + os.sep + song_stats,'a')
	for item in s: s[item] = str(s[item])
	csv = "\t".join([s['ARTIST'],s['SONG'],s['TYPES'],s['TOKENS'],s['AVG_LINE_LENGTH'],s['MOST_COMMON_WORD'],s['MOST_COMMON_BIGRAM'],s['MOST_COMMON_TRIGRAM']])
	f.write(str(csv.encode(encoding='ascii', errors='replace').decode()) + "\n")
	f.close()

def new_a_stat(): 
	return Counter(['ARTIST','NUM_SONGS','NUM_TYPES','NUM_TOKENS','MEAN_AVG_LINE_LENGTH','MOST_COMMON_WORD','MOST_COMMON_BIGRAM','MOST_COMMON_TRIGRAM'])

def write_a_stat(a): 
	f = open(subfolder + os.sep + artist_stats,'a')
	for item in a: a[item] = str(a[item])
	csv = "\t".join([a['ARTIST'],a['NUM_SONGS'],a['NUM_TYPES'],a['NUM_TOKENS'],a['MEAN_AVG_LINE_LENGTH'],a['MOST_COMMON_WORD'],a['MOST_COMMON_BIGRAM'],a['MOST_COMMON_TRIGRAM']])
	f.write(str(csv.encode(encoding='ascii', errors='replace').decode()) + "\n")
	f.close()

def new_g_stat(): 
	return Counter(['NUM_ARTISTS','NUM_SONGS','NUM_TYPES','NUM_TOKENS','MEAN_AVG_LINE_LENGTH','MOST_COMMON_WORD','MOST_COMMON_BIGRAM','MOST_COMMON_TRIGRAM'])

def write_g_stat(g): 
	f = open(subfolder + os.sep + genre_stats,'a')
	for item in g: g[item] = str(g[item])
	csv = "\t".join([g['NUM_ARTISTS'],g['NUM_SONGS'],g['NUM_TYPES'],g['NUM_TOKENS'],g['MEAN_AVG_LINE_LENGTH'],g['MOST_COMMON_WORD'],g['MOST_COMMON_BIGRAM'],g['MOST_COMMON_TRIGRAM']])
	f.write(str(csv.encode(encoding='ascii', errors='replace').decode()) + "\n")
	f.close()


def fill_buckets(directory):
	for root, dirs, files in os.walk(directory, topdown=True):
		for dir in dirs:
			print("Artist: "+dir)
			artist_document_map[dir] = {}
			fill_buckets(dir)
		
		for name in files:
			if not name.startswith("."):
				filename = os.path.join(root, name)
				fname = filename.split(os.sep) 
				song = fname[-1]
				artist = fname[1]
				#print("Song: "+song)
				with codecs.open(filename, encoding="ascii", errors="replace") as filename:
					file_contents = [l.strip() for l in filename.readlines() if len(l.strip())]
					artist_document_map[artist][song] = file_contents	


def get_counted_sorted_list(list2sort):
	return sorted(Counter(list2sort).items(), key=lambda item: item[1], reverse=True)


def get_song_stats(song, oneline=False, suppress_output=False):
	#print("SONG: ")
	#print(song)

	punc = '''!()[]{};:"+=\,<>./?@#$%^&*_~'''
	bag_of_words = []
	line_count = len(song)
	tokens = 0
	types = 0

	for line in song:
		#print("before: " + line)
		line = line.lower()
		line = line.replace('quot;','').replace('&amp;','and').replace('&amp','and')
		line = line.replace("n'","n").replace("l'","l")#.replace("'", " '")
		line = line.replace('-',' ')
		newline = ""
		for char in line:
			if char not in punc:
				newline += char
		#print("after: " + newline)
		if remove_stops:
			line = [n.strip() for n in newline.split() if n.strip() not in stops]
		else:
			line = [n.strip() for n in newline.split()]
		tokens += len(line)
		bag_of_words += line

	# handle the stupid case...
	if oneline:
		if len(song) <= 1:
			song = ["empty"]
			bag_of_words = song
			line_count = 1
			types = 1
			tokens = 1

	frequencies = Counter(bag_of_words)
	types = len(frequencies.keys())
	average_line_length = round(float(len(bag_of_words))/float(line_count),2)
	if not suppress_output:
		print("avg line: "+str(average_line_length))
		print("tokens: " + str(tokens))
	return (types, tokens, average_line_length, bag_of_words, frequencies)

				
def do_ngram_stuff(bow):
	append = "_"
	bgrams = []
	tgrams = []
	for i in range(len(bow)-2):
		bigram = bow[i] + append + bow[i+1]
		bgrams.append(bigram)
		#print(bigram)
		trigram  = bow[i] + append + bow[i+1] + append + bow[i+2]
		tgrams.append(trigram)
		#print(trigram)
	
	if len(bow) >= 2:
		last_bigram = bow[-2] + append + bow[-1]
		bgrams.append(last_bigram)
	
	#print(bgrams)
	#print(tgrams)
	if len(bgrams) <= 1 or len(tgrams) <= 2: 
		bgrams = bow
		tgrams = bow

	return (bgrams,tgrams)


#====================================#
# MAIN SHIT
#====================================#
if __name__ == "__main__":

	make_dir(subfolder)

	#(['NUM_ARTISTS','NUM_SONGS','NUM_TYPES','NUM_TOKENS','MEAN_AVG_LINE_LENGTH','MOST_COMMON_WORD','MOST_COMMON_BIGRAM','MOST_COMMON_TRIGRAM'])
	g_stat = new_g_stat()
	for g in g_stat: g_stat[g] = 0

	fill_buckets(folder)
	total_artists = len(artist_document_map.keys())
	debug("Num total artists: " + str(total_artists))
	g_stat['NUM_ARTISTS'] = total_artists

	genre_bow = []
	genre_bigram_bow = []
	genre_trigram_bow = []

	# compute artist statistics
	for artist in artist_document_map.keys():

		#(['ARTIST','NUM_SONGS','NUM_TYPES','NUM_TOKENS','MEAN_AVG_LINE_LENGTH','MOST_COMMON_WORD','MOST_COMMON_BIGRAM','MOST_COMMON_TRIGRAM'])
		a_stat = new_a_stat()
		a_stat['ARTIST'] = artist
		
		songs = artist_document_map[artist]
		num_songs = len(songs)

		a_stat['NUM_SONGS'] = num_songs
		g_stat['NUM_SONGS'] += num_songs

		artist_bow = []
		artist_bigram_bow = []
		artist_trigram_bow = []
		
		for song in songs:

			#(['ARTIST','SONG','TYPES','TOKENS','AVG_LINE_LENGTH','MOST_COMMON_WORD','MOST_COMMON_BIGRAM','MOST_COMMON_TRIGRAM'])
			s_stat = new_s_stat()

			(types, tokens, avg_line_length, bag_of_words, frequencies) = get_song_stats(songs[song])
			(bigrams, trigrams) = do_ngram_stuff(bag_of_words)
			
			frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
			bgram_freq = get_counted_sorted_list(bigrams)
			tgram_freq = get_counted_sorted_list(trigrams)
			
			# song level 
			s_stat['ARTIST'] = artist
			s_stat['SONG'] = song.replace(".txt","")
			s_stat['TYPES'] = types
			s_stat['TOKENS'] = tokens
			s_stat['AVG_LINE_LENGTH'] = avg_line_length
			s_stat['MOST_COMMON_WORD'] = frequencies[0]
			s_stat['MOST_COMMON_BIGRAM'] = bgram_freq[0]
			s_stat['MOST_COMMON_TRIGRAM'] = tgram_freq[0]
			
			# artist level 
			a_stat['NUM_TOKENS'] += tokens
			a_stat['MEAN_AVG_LINE_LENGTH'] += avg_line_length
			artist_bow += bag_of_words
			artist_bigram_bow += bigrams
			artist_trigram_bow += trigrams
			
			# genre level
			g_stat['MEAN_AVG_LINE_LENGTH'] += avg_line_length
			g_stat['NUM_TOKENS'] += tokens
			genre_bow += bag_of_words
			genre_bigram_bow += bigrams
			genre_trigram_bow += trigrams
			
			# write song stats to file			
			write_s_stat(s_stat)
			print(s_stat)

		# artist stats...
		#(['ARTIST','NUM_SONGS','NUM_TYPES','NUM_TOKENS','MEAN_AVG_LINE_LENGTH','MOST_COMMON_WORD','MOST_COMMON_BIGRAM','MOST_COMMON_TRIGRAM'])
		artist_unigram_freq = get_counted_sorted_list(artist_bow)
		artist_bigram_freq = get_counted_sorted_list(artist_bigram_bow)
		artist_trigram_freq = get_counted_sorted_list(artist_trigram_bow)

		sum_avg_line_lengths = a_stat['MEAN_AVG_LINE_LENGTH']
		a_stat['MEAN_AVG_LINE_LENGTH'] = round(sum_avg_line_lengths/float(a_stat['NUM_SONGS']), 2)
		a_stat['NUM_TYPES'] = len(artist_unigram_freq)
		a_stat['MOST_COMMON_WORD'] = artist_unigram_freq[0]
		a_stat['MOST_COMMON_BIGRAM'] = artist_bigram_freq[0]
		a_stat['MOST_COMMON_TRIGRAM'] = artist_trigram_freq[0]

		write_a_stat(a_stat)
		#debug(a_stat)

	# genre level
	#(['NUM_ARTISTS','NUM_SONGS','NUM_TYPES','NUM_TOKENS','MEAN_AVG_LINE_LENGTH','MOST_COMMON_WORD','MOST_COMMON_BIGRAM','MOST_COMMON_TRIGRAM'])
	genre_unigram_freq = get_counted_sorted_list(genre_bow)
	genre_bigram_freq = get_counted_sorted_list(genre_bigram_bow)
	genre_trigram_freq = get_counted_sorted_list(genre_trigram_bow)
	
	sum_avg_line_lengths = g_stat['MEAN_AVG_LINE_LENGTH']
	g_stat['MEAN_AVG_LINE_LENGTH'] = round(sum_avg_line_lengths/float(g_stat['NUM_SONGS']), 2)
	g_stat['NUM_TYPES'] = len(genre_unigram_freq)
	g_stat['MOST_COMMON_WORD'] = genre_unigram_freq[0]
	g_stat['MOST_COMMON_BIGRAM'] = genre_bigram_freq[0]
	g_stat['MOST_COMMON_TRIGRAM'] = genre_trigram_freq[0]

	write_g_stat(g_stat)
	write_ngram_stats(genre_unigram_freq, unigram_word_rank)
	write_ngram_stats(genre_bigram_freq, bigram_word_rank)
	write_ngram_stats(genre_trigram_freq, trigram_word_rank)
	print(g_stat)

	print("\n\n****** DONE! ******\n\n")

	#debug(artist_document_map.keys())
	#debug(artist_document_map.values())	
	#print("Word Types: "+str(len(counter.keys())))
	#print("Word Tokens: "+str(len(stuff)))
		
