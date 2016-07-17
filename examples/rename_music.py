#James Gilles, 2012
#DWTFYWWI License

# Source: https://gist.github.com/kazimuth/3334942

from mutagen.easyid3 import EasyID3
import os

print "input directory for processing: "
path = raw_input()
os.chdir(path)

file_list = filter((lambda x: '.mp3' in x), os.listdir(path))

for i in file_list:
        print "file: "+i
        try:
                current = EasyID3(i)
                newname = current["title"][0] + ".mp3"
                newname.replace(" ", "_")
                del current
                print "renaming "+i+" to "+newname
                os.rename(i, newname)
        except:
print "...that file didn't work for some reason.