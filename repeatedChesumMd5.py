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
import logging
from glob import glob
import hashlib
from collections import Counter
import json
from datetime import datetime
import sys
import time
import shutil
from ntpath import split, basename

LOG_FILENAME = datetime.now().strftime('./log/logfile_%Y_%m_%d_%H_%M_%S_%d.log')

logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)


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
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
            f.close()
    except OSError as err:
        logging.error("OSError when processing {} : {}".format(fname, err))
        print("OS error: {0}".format(err))
    except:
        print("Unexpected error:{}".format(sys.exc_info()[0]))
        logging.error("OSError when processing {}".format(sys.exc_info()[0]))
        raise

    return hash_md5.hexdigest()


def getDuplicatedFiles(md5Files):
    """Get duplicated checksums.

    ;returns: dictionary with checksum as key and count as value.
    """
    md5Duplicated = dict()
    for k in dict(filter(lambda elem: elem[1] > 1,
                         Counter(md5Files.values()).items())).keys():
        md5Duplicated[k] = dict(filter(lambda elem: elem[1] == k,
                                       md5Files.values()))
    return md5Duplicated


def getKeysByValue(d1, l1):
    """Filter d1 keys if exists in the list.

    Returns the paths where it's checksum is in the list.

    ;returns: list of keys/paths
    """
    filteredKeys = list()
#    for i in l1:
#        filteredKeys.append({k: v for k, v in d1.items() if v == i})
    filteredKeys = ({k for k, v in d1.items() if v in l1})
    return filteredKeys


def setMd5ByFile(targetPath):
    """Go recusively through all files in the directory.

    ;return: dictionary with file path as key and md5 as value.
    """
    md5 = dict()

    i = 0

    for fname in [y for x in os.walk(targetPath)
                  for y in glob(os.path.join(x[0], "*.*"))]:
        md5[fname] = generateMd5(fname)
        i = i + 1
        logging.info("{} -> {}".format(i, fname))
        print("{} -> {}".format(i, fname))

    return md5


def dict_compareBykey(d1, d2):
    """Compare two dictionaries."""
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    return added, removed, modified, same


def compareValuesBetween2Dicts(d1, d2):
    """Compare values from 2 dicts.

    Get distinct values for each dict.
    compare.
    """
    return dict_compareBykey(getUniqueKeys(d1), getUniqueKeys(d2))


def getUniqueKeys(d):
    """Get unique keys from dict.

    ;return: dictionary with only non repeated keys
    """
    return dict.fromkeys(set(d.values()), 0)


def main():
    """Execute start.

    ;param parPath: path where to operate with images
    """
    cls()

    myPath = "C:\\Users\\justme\\Pictures"
    myPathTarget = "E:\\Recuerdos"

    # myPath = "c:/Users/justme/Documents/2004volksfest2004"

    if not(os.path.isdir(myPath)):
        print(bcolors.FAIL
              + "Error: Path not exists{}".format(myPath)
              + bcolors.ENDC)
    else:
        print(bcolors.OKBLUE + "Target path: {}".format(myPath) + bcolors.ENDC)

    if False:
        md5 = setMd5ByFile(myPath)
        print(Counter(md5))
        print('')
        duplicatedFiles = getDuplicatedFiles(md5)
        print(Counter(duplicatedFiles))

        with open('./todos.json', 'w') as json_file:
            json.dump(md5, json_file)

        with open('./duplicados.json', 'w') as json_file:
            json.dump(duplicatedFiles, json_file)

        md5Target = setMd5ByFile(myPathTarget)

        with open('./todosTarget.json', 'w') as json_file:
            json.dump(md5Target, json_file)

    # Read from files already created
    # select dupplicated from todos.txt
    # show them and select wich ones to delete

    with open('./todos.json') as json_file:
        filesMd5 = json.load(json_file)
        json_file.close

    with open('./duplicados.json') as json_file:
        dupsMd5 = json.load(json_file)
        json_file.close

    with open('./todosTarget.json') as json_file:
        filesTarget = json.load(json_file)
        json_file.close

    print("Number of files = {}".format(len(filesMd5)))
    print(bcolors.OKBLUE + "Number of distinct dups = {}".format(len(dupsMd5))
          + bcolors.ENDC)
    print(bcolors.OKBLUE +
          "Number of files in target = {}".format(len(filesTarget))
          + bcolors.ENDC)
    added, removed, modified, same = compareValuesBetween2Dicts(filesTarget,
                                                                filesMd5)

    print("Number of files in both = {}".format(len(same)))
    print("Number of files only in Recuerdos = {}".format(len(removed)))
    print("Number of files only in Pictures = {}".format(len(added)))

    """
    print("PATHS In recuerdos/ touro not in Pictures") #Solo los thumb.db
    print(getKeysByValue(filesTarget, added))


    print("PATHS In Pictures not in recuerdos/Touro")
    print(getKeysByValue(filesMd5, removed))

    #Para cada path devuelto por getKeysByValue de Touro a pictures
    pegarlo en pictures si no es Thumbs.db
    si existe el directorio pegar
    si no, crear y pegar
    """
    sourcePaths = getKeysByValue(filesTarget, added)
    # convertir en targetPath y quitar nombre de fichero pq copia file to path
    #                               pathname in the sequence paths.
    targetPaths = [x.replace("E:\\Recuerdos\\",
                             "C:\\Users\\justme\\Pictures\\")
                   for x in sourcePaths]
    targetPaths = ({os.path.dirname(path) for path in targetPaths})
    print(targetPaths)

    sys.exit()
    # Check sorting of items sourcepaths[i] = targetpaths[i]
    shutil.copy(sourcePaths, targetPaths)
    shutil.copy2(sourcePaths, targetPaths,)
    sys.exit()
    """
    #Luego hacer limpieza de Pictures
    Hacer una compresión del directorio a limpiar y almacenar como bkp
    Limpiar pictures

    #Borrar touro recuerdos
    #Pegar Pictures

    Después hay que hacer limpieza en recuerdos

    """


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
