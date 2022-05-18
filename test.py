from rich.progress import Progress
from time import sleep; import os; import subprocess

workDir = os.curdir # the current working Directory TODO: add ability for user to choose this
supportedList = ['.mkv', '.avi']

# move the files into directories named after their types
def sort_file(newFilename, filename, oldType):
    path = workDir + '/'
    try:
        os.rename(path + filename, path + oldType + "/" + filename)
        os.rename(path + newFilename, path + "mp4/" + newFilename)
        return "Moved"
    except OSError as error:
        return str(error)

# converts a file into mp4 using ffmpeg
def convert(oldType, filename):
    newFilename = filename.replace(oldType, "mp4")
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error','-i', filename, '-codec', 'copy', newFilename])
    sort_file(newFilename, filename, oldType)
    return (str(filename) + " was converted to " + str(newFilename))

def add_folder(vidType): #creates a folder
    try:
        os.mkdir(vidType)
        return ("Directory" + str(vidType) + " created")
    except FileExistsError:
        return ("Directory" + str(vidType) + " already exists")

def vidconvert():
    with Progress() as progress:
        fileNumber = len([name for name in os.listdir(workDir) if os.path.isfile(name)])
        task = progress.add_task("Progress", total=fileNumber)
        for filename in os.listdir(workDir):
            extension = os.path.splitext(filename)[1]
            if extension in supportedList:
                progress.console.print(f"Converting {filename}")
                add_folder("mp4")
                add_folder(extension[1:])
                convert(extension[1:], filename)
                progress.console.print(f"Converted {filename}")
                progress.advance(task)
            else:
                progress.console.print(f"{filename} ignored as type isn't supported")
                sleep(0.4)
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
