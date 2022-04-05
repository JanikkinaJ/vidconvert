#!/usr/bin/python

import os
import subprocess

# move the files into directories named after their types
def sort_file(new_filename, filename, old_type):
    path = os.curdir
    path = path + '/'
    try:
        os.rename(path + filename, path + old_type + "/" + filename)
        os.rename(path + new_filename, path + "mp4/" + new_filename)
    except OSError as error:
            print(error)

# converts a file into mp4 using ffmpeg
def convert(old_type, filename):
    new_filename = filename.replace(old_type, "mp4")
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error','-i', filename, '-codec', 'copy', new_filename])
    print(filename, " was converted to ", new_filename)
    sort_file(new_filename, filename, old_type)

# uses convert() and then adds a folder for the type if not already created
def process(folder_present, mp4_folder, filename, endswith):
    if not folder_present: 
        add_folder(endswith)
    if not mp4_folder:
        add_folder("mp4")
    convert(endswith, filename)

#checks current directory for supported file types and creates a mp4 version of them
def vidconvert():
    mkv_folder = False
    avi_folder = False
    mp4_folder  = False
    for filename in os.listdir(os.curdir):
        if filename.endswith('mkv'):
            process(mkv_folder, mp4_folder, filename, "mkv")
            mkv_folder = True
            mp4_folder = True
        elif filename.endswith('avi'):
            process(avi_folder, mp4_folder, filename, "avi")
            avi_folder = True
            mp4_folder = True
        else:
            print(filename, " ignored as type isn't supported")
            continue
    print("""
We did our best chief.
          _       _                                                _   
         (_)     | |                                              | |  
 __   __  _    __| |   ___    ___    _ __   __   __   ___   _ __  | |_ 
 \ \ / / | |  / _` |  / __|  / _ \  | '_ \  \ \ / /  / _ \ | '__| | __|
  \ V /  | | | (_| | | (__  | (_) | | | | |  \ V /  |  __/ | |    | |_ 
   \_/   |_|  \__,_|  \___|  \___/  |_| |_|   \_/    \___| |_|     \__|
""")


def add_folder(vid_type): #creates folder
    try:
        os.mkdir(vid_type)
        print("Directory ", vid_type, " created")
    except FileExistsError:
        print("Directory", vid_type, " already exists")

vidconvert()
