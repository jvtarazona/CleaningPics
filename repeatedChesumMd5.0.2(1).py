# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 22:08:38 2021.

@author: justme

search for repeated files in a folder comparing checksum MD5
get path and name from path, subforlders recursive
calculate checksum for all
search for repeated checksums
iform
delete automatically or ask user wich one to delete.
"""
import os
from glob import glob
import hashlib
from collections import Counter
import bcolors

_md5Files = dict()
_md5Duplicated = dict()
_targetPath = None

#
# Application/service layer
#


def printCount(md5ByFile):
    """Show the number of items with the same checksum."""
    Counter(md5ByFile)


def generateMd5(fname):
    """Get MD5 from file by chuncks of 4096 bytes.

    ;param fname: file name
    ;param type: string
    ;return: md5 Checksum for the specified file
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def getDuplicatedFiles(md5Files):
    """Get duplicated checksums.

    ;returns: dictionary with checksum as key and count duplicated as value.
    """
    md5Duplicated = dict()
    for k in dict(filter(lambda elem: elem[1] > 1,
                         Counter(md5Files.values()).items())).keys():
        md5Duplicated[k] = dict(filter(lambda elem: elem[1] == k,
                                       md5Files.values()))
    return md5Duplicated


def setMd5ToFilesInDirectory(targetPath):
    """Go recusively through all files in the directory.

    ;return: dictionary with file path as key and md5 as value.
    """
    md5 = dict()
    for fname in [y for x in os.walk(targetPath)
                  for y in glob(os.path.join(x[0], "*.*"))]:
        md5[fname] = generateMd5(fname)

    return md5


def setTargetPath(targetPath):
    """Set target path where files are stored."""
    newPath = input("Write path with the pictures: ")

    if not pathExists(newPath):
        return

    if targetPath is None:
        targetPath = newPath
    else:
        if input("{bcolors.WARN}Previous path: {} .\n \
                  Overwrite?{bcolors.ENDC} y/n: \
                      ".format(targetPath)).upper() == "Y":
            targetPath = newPath


def pathExists(targePath):
    """Check if path is correct."""
    if not(os.path.isdir(targePath)):
        print(bcolors.FAIL
              + "Error: Path not exists{}".format(targePath)
              + bcolors.ENDC)
        return False
    else:
        print(bcolors.BLUE + "Target path: {}".format(targePath)
              + bcolors.ENDC)
        return True


#
# Presentation Layer
#


# class bcolors(object):
#     """Colors for text."""

#     HEADER = "\033[95m"
#     OKBLUE = "\033[94m"
#     OKGREEN = "\033[92m"
#     WARNING = "\033[93m"
#     FAIL = "\033[91m"
#     ENDC = "\033[0m"

#     def disable(self):
#         """Disable."""
#         self.HEADER = ""
#         self.OKBLUE = ""
#         self.OKGREEN = ""
#         self.WARNING = ""
#         self.FAIL = ""
#         self.ENDC = ""


def quit_fn():
    """Finish program."""
    raise SystemExit


def invalid():
    """Message the wrong choice."""
    print("{bcolor.FAIL} INVALID CHOICE! {bcolor.ENDC}")


def cls():
    """Clear console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Execute start.

    ;param parPath: path where to operate with images
    """
    cls()

    ans = None
    menu = {"1": ("Specify target path.", setTargetPath(_targetPath)),
            "2": ("Generate Checksums.", setMd5ToFilesInDirectory(_targetPath)),
            "3": ("Show counting from All files.", printCount(_md5Files)),
            "4": ("Get duplicated pictures.", getDuplicatedFiles(_md5Files)),
            "5": ("Show Counting from Duplicated files.",
                  printCount(_md5Duplicated)),
            "0": ("Quit", quit_fn)}
    for key in sorted(menu.keys()):
        print(key+":" + menu[key][0])

    ans = input("Make A Choice: ")
    menu.get(ans, [None, invalid])[1]()

    # myPath = "C:\\Users\\justme\\Pictures"

    # myPath = "c:\\Users\\justme\\Documents\\2004volksfest2004"

    # if not(os.path.isdir(myPath)):
    #     print(bcolors.FAIL
    #           + "Error: Path not exists{}".format(myPath)
    #           + bcolors.ENDC)
    # else:
    #     print(bcolors.OKBLUE + "Target path: {}".format(myPath) + bcolors.ENDC)

    # print(Counter(setMd5ByFile(myPath)))
    # print('')
    # print(getDuplicatedFiles(setMd5ByFile(myPath)))


if __name__ == "__main__":
    main()
