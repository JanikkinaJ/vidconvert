```
         _       _                                                _   
        (_)     | |                                              | |  
__   __  _    __| |   ___    ___    _ __   __   __   ___   _ __  | |_ 
\ \ / / | |  / _` |  / __|  / _ \  | '_ \  \ \ / /  / _ \ | '__| | __|
 \ V /  | | | (_| | | (__  | (_) | | | | |  \ V /  |  __/ | |    | |_ 
  \_/   |_|  \__,_|  \___|  \___/  |_| |_|   \_/    \___| |_|     \__|
```
Converts all mkv and avi files inside current directory into mp4 files and keeps a copy
of the original files using ffmpeg. Then sorts converted and convertee files into folders named the same as their filetypes.
##Compatibility
Right now vidconvert only supports Linux

## Install
- clone repository
- `cd vidconvert`
- `sudo make setup`

## Usage
after install just move inside the directory where you want to convert files to mp4, 
then type `vidconvert`
