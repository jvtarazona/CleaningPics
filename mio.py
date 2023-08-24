# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 22:08:38 2021

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
import json


class bcolors(object):
    """Colors for text."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

    def disable(self):
        """Disable."""
        self.HEADER = ""
        self.OKBLUE = ""
        self.OKGREEN = ""
        self.WARNING = ""
        self.FAIL = ""
        self.ENDC = ""


def cls():
    """Clear console."""
    os.system('cls' if os.name == 'nt' else 'clear')


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


def setMd5ByFile(targetPath):
    """Go recusively through all files in the directory.

    ;return: dictionary with file path as key and md5 as value.
    """
    md5 = dict()
    for fname in [y for x in os.walk(targetPath)
                  for y in glob(os.path.join(x[0], "*.*"))]:
        md5[fname] = generateMd5(fname)

    return md5


def main():
    """Execute start.

    ;param parPath: path where to operate with images
    """
    cls()

    myPath = "C:\\Users\\justme\\Pictures"

    # myPath = "c:/Users/justme/Documents/2004volksfest2004"

    if not(os.path.isdir(myPath)):
        print(bcolors.FAIL
              + "Error: Path not exists{}".format(myPath)
              + bcolors.ENDC)
    else:
        print(bcolors.OKBLUE + "Target path: {}".format(myPath) + bcolors.ENDC)

    md5 = setMd5ByFile(myPath)
    print(Counter(md5))
    print('')
    duplicatedFiles = getDuplicatedFiles(md5)
    print(Counter(duplicatedFiles))

    with open('c:/Users/justme/Documents/todos.json', 'w') as json_file:
        json.dump(md5, json_file)

    with open('c:/Users/justme/Documents/duplicados.json', 'w') as json_file:
        json.dump(duplicatedFiles, json_file)


if __name__ == "__main__":
    main()
