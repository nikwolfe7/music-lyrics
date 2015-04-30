import os
import shutil
def debug(var):
	print(var)
	input("Press Enter...")
'''
Created on Apr 29, 2015

@author: nwolfe
'''
def remove_files(directory, artist_songs):
    os.chdir(os.path.join(os.getcwd(),directory))
    for root, dirs, files in os.walk(".", topdown=False):
        for dir in dirs:
            dir = os.path.abspath(dir)
            if os.path.isdir(dir):
                os.chdir(os.path.join(root, dir))
                print(os.getcwd())
                for rewt, subdirs, midifiles in os.walk(".", topdown=False):
                    artist = dir.split(os.sep)[-1]
                    try:
                        songs = artist_songs[artist]
                    except Exception as e: songs = []
                    for f in midifiles:
                        print(f)
                        fname = (dir.split(os.sep)[-1] + "-").lower()
                        flow = f.lower().replace("_","-")
                        if flow.startswith(fname): 
                            print("looks good!")
                            if "_" in f:
                                test = os.path.join(dir,f.replace("-","").replace("__","_").replace("_","-").lower())
                                if os.path.isfile(test):
                                    print("duplicate file!")
                                    os.remove(os.path.join(dir,f))
                        else:
                            print("no!")
                            os.remove(os.path.join(dir,f))
                        song = flow.replace(fname,"").replace(".mid","")
                        if song in songs:
                            print("legit song")
                        else:
                            print("WARNING!")
                            try: os.rename(f, f.upper())
                            except Exception as e: continue
                            
                            
                os.chdir("..")
    os.chdir("..")

def get_artist_song_lists(directory):
    artist_songs = {}
    pwd = os.path.abspath(os.getcwd())
    os.chdir(directory)
    for root, dirs, files in os.walk(".", topdown=False):
        for dir in dirs:
            dir = os.path.abspath(dir)
            if os.path.isdir(dir):
                os.chdir(os.path.join(root, dir))
                #print(os.getcwd())
                for rewt, subdirs, midifiles in os.walk(".", topdown=False):
                    for f in midifiles:
                        #print(f)
                        try:
                            artist_songs[dir.split(os.sep)[-1]].append(f.split(".txt")[0].replace("amp;",""))
                        except Exception as e:
                            artist_songs[dir.split(os.sep)[-1]] = []
                            artist_songs[dir.split(os.sep)[-1]].append(f.split(".txt")[0].replace("amp;",""))
                os.chdir("..")
    os.chdir(pwd)
    return artist_songs

def assign_homes_to_orphans(artist_songs, directory, send_to):
    pwd = os.path.abspath(os.getcwd())
    os.chdir(directory)
    for root, dirs, files in os.walk(".", topdown=False):
        for f in files:
            ffix = f.lower().replace("_","-").replace("---","-")
            for artist in artist_songs:
                if ffix.startswith(artist + "-"):
                    ffix = ffix.replace(artist + "-","").replace(".mid","")
                    for song in artist_songs[artist]:
                        if ffix in song and len(ffix) > 4:
                            print("Maybe? " + f)
                            newpath = os.path.join(pwd,send_to,artist)
                            if not os.path.isdir(newpath):
                                os.mkdir(newpath)
                            currpath = os.path.join(os.getcwd(),f)
                            try:
                                shutil.move(f,newpath)
                            except Exception as e:
                                print("Something went wrong! " + str(e)) 
                                continue
    os.chdir(pwd)
            
                           

if __name__ == '__main__':
    assign_homes_to_orphans(get_artist_song_lists("../hip_hop_rap"), "MIDICheck", "MIDI_hip_hop_rap")
    assign_homes_to_orphans(get_artist_song_lists("../rock_metal_country"), "MIDICheck", "MIDI_rock_metal_country")
    remove_files("MIDI_hip_hop_rap",get_artist_song_lists("../hip_hop_rap"))
    remove_files("MIDI_rock_metal_country",get_artist_song_lists("../rock_metal_country"))
    

