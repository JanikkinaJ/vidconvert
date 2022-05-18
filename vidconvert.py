#!/usr/bin/env python3

from rich.progress import (
        BarColumn,
        Progress,
        TextColumn,
        )
from time import sleep; import os; import subprocess

workDir = os.curdir # the current working Directory TODO: add ability for user to choose this
supportedList = ['.mkv', '.avi']

# move the files into directories named after their types
def sort_file(newFilename, currentFile, oldType):
    path = workDir + '/'
    try:
        os.rename(path + currentFile, path + oldType + "/" + currentFile)
        os.rename(path + newFilename, path + "mp4/" + newFilename)
        return "Moved"
    except OSError as error:
        return str(error)

# converts a file into mp4 using ffmpeg
def convert(oldType, currentFile):
    newFilename = currentFile.replace(oldType, "mp4")
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error','-i', currentFile, '-codec', 'copy', newFilename])
    sort_file(newFilename, currentFile, oldType)
    return f"\"{currentFile}\" was converted to \"{newFilename}\""

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
                progress.console.print(f"Converting: \"{currentFile}\"")
                add_folder("mp4")
                add_folder(extension[1:])
                progress.console.print(convert(extension[1:], currentFile))
                progress.advance(task)
            else:
                progress.console.print(f"\"{currentFile}\" ignored as type isn't supported")
                sleep(0.2)
                progress.advance(task)

    print("""
          _       _                                                _   
         (_)     | |                                              | |  
 __   __  _    __| |   ___    ___    _ __   __   __   ___   _ __  | |_ 
 \ \ / / | |  / _` |  / __|  / _ \  | '_ \  \ \ / /  / _ \ | '__| | __|
  \ V /  | | | (_| | | (__  | (_) | | | | |  \ V /  |  __/ | |    | |_ 
   \_/   |_|  \__,_|  \___|  \___/  |_| |_|   \_/    \___| |_|     \__|
""")


if __name__ == "__main__":
    vidconvert()
