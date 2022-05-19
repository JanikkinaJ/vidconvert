#!/usr/bin/env python3

from rich.progress import (
        BarColumn,
        Progress,
        TextColumn,
        )
from rich.console import Console
from time import sleep; import os; import subprocess
import argparse
console = Console() #creates a console type for Rich text output
parser = argparse.ArgumentParser(description= 'Mass batch conversion using ffmpeg. Converts video files into Mp4 and then sorts them.')
parser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

workDir = os.curdir # the current working Directory TODO: add ability for user to choose this
supportedList = ['.mkv', '.avi'] #supported video types

# move the files into directories named after their types
def sort_file(newFilename, currentFile, oldType):
    path = workDir + '/'
    try:
        os.rename(path + currentFile, path + oldType + "/" + currentFile)
        os.rename(path + newFilename, path + "mp4/" + newFilename)
        return f"\"{currentFile}\" was converted to \"{newFilename}\""
    except OSError as error:
        return str(error)

# converts a file into mp4 using ffmpeg
def convert(oldType, currentFile):
    newFilename = currentFile.replace(oldType, "mp4")
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
        for currentFile in os.listdir(workDir):
            extension = os.path.splitext(currentFile)[1]
            if extension in supportedList:
                if args.verbose:
                    progress.console.print(f"Converting: \"{currentFile}\"")
                add_folder("mp4")
                add_folder(extension[1:])
                progress.console.print(convert(extension[1:], currentFile))
                progress.advance(task)
            else:
                if args.verbose:
                    progress.console.print(f"\"{currentFile}\" ignored as type isn't supported")
                sleep(0.2)
                progress.advance(task)

    console.print("""
Thank you for using vidconvert :thumbs_up:

01101010 01100001 01101110 01101001 01101011
""", style="bold red", justify="center")


if __name__ == "__main__":
    vidconvert()
