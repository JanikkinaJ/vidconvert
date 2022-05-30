#!/usr/bin/env python3

from enum import Enum

class vType(Enum):
    mp4 = auto()
    avi = auto()
    mkv = auto()

class File:
    def __init__(self, name, videoType, path):
        self.name = name
        self.videoType = videoType
        self.extension = f".{videoType}"
        self.path = path

    def __str__(self):
        return f"{path}"
