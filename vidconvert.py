#!/usr/bin/env python3

from rich.progress import (
        BarColumn,
        Progress,
        TextColumn,
        )
from rich.console import Console
from time import sleep; import os; import subprocess
import argparse
import files

supportedList = ['.mkv', '.avi'] #supported video types
convertTo = ".mp4"
workDir = os.curdir # the current working Directory TODO: add ability for user to choose this

console = Console() #creates a console type for Rich text output
parser = argparse.ArgumentParser(description= 'Mass batch conversion using ffmpeg. Converts video files into Mp4 and then sorts them.') 
parser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-ot","--outputtype", help="lets the user choose an outputtype via extension", type=str, choices=supportedList)
args = parser.parse_args() #argparse used to allow command line arguments
if args.outputtype is not None:
    convertTo = str(args.outputtype)

# move the files into directories named after their types
def sort_file(newFilename, currentFile, oldType):
    path = workDir + '/'
    try:
        os.rename(path + currentFile, path + oldType + "/" + currentFile)
        os.rename(path + newFilename, path + convertTo[1:] +"/" + newFilename)
        return f"\"{currentFile}\" was converted to \"{newFilename}\""
    except OSError as error:
        return str(error)

# converts a file into mp4 using ffmpeg
def convert(oldType, currentFile):
    newFilename = currentFile.replace(oldType, convertTo[1:])
    result = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error','-i', currentFile, '-codec', 'copy', newFilename], text=True, capture_output=True)
    output = result.stderr + "\n" + sort_file(newFilename, currentFile, oldType)
    return output 

def add_folder(vidType): #creates a folder
    try:
        os.mkdir(vidType)
        print("Directory " + str(vidType) + " created")
    except FileExistsError:
        #print("Directory " + str(vidType) + " already exists")
        return None

def vidconvert():
    with Progress(
            TextColumn("{task.description}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%"
            )  as progress:
        fileNumber = len([name for name in os.listdir(workDir) if os.path.isfile(name)])
        task = progress.add_task("Progress: ", total=fileNumber)
        ignored = 0
        for currentFile in os.listdir(workDir):
            extension = os.path.splitext(currentFile)[1]
            if extension in supportedList and extension != convertTo:
                if args.verbose:
                    progress.console.print(f"Converting: \"{currentFile}\"")
                add_folder(convertTo[1:])
                add_folder(extension[1:])
                progress.console.print(convert(extension[1:], currentFile))
                progress.advance(task)
            else:
                if args.verbose:
                    progress.console.print(f"\"{currentFile}\" ignored as type isn't supported")
                else:
                    ignored += 1 

                sleep(0.2)
                progress.advance(task)
    if not args.verbose:
        console.print(f"{ignored} files ignored.")
    console.print("""
Thank you for using vidconvert :thumbs_up:

01101010 01100001 01101110 01101001 01101011
""", style="bold red", justify="center")

if __name__ == "__main__":
    vidconvert()
