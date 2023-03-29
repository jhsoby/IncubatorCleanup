#!/usr/bin/env python3
import os
import time
from argparse import ArgumentParser
import re, urllib.request, json

parser = ArgumentParser()
parser.add_argument("filename",nargs=1,help="the filename which should be split")
args = parser.parse_args()

filename = args.filename[0]
directory = filename.replace(".xml", "").replace(".ready", "")
try:
    os.mkdir(directory)
except OSError:
    print("Could not create directory '" + directory + "'. It probably exists already.")
else:
    print("Directory '" + directory + "' created.")

def ulen(s):
    return len(s.encode('utf-8'))

prepend = ""
append = "</mediawiki>"

maxsize = int(2.5*(10**6)) # 2.5 MB
maxpages = 250

with open(filename, "r") as file:
    hitpage = False
    slicesize = 0
    slicenumber = 1
    pagesinslice = 0
    stop = False
    currentslice = ""
    firsttitle = ""
    lasttitle = ""
    for line in file:
        if not hitpage and not "<page>" in line:
            prepend += line
        if "<title>" in line:
            title = re.sub(r".*\<title\>", "", line)
            title = re.sub(r"\</title\>.*\n*", "", title)
            firsttitle = firsttitle or title
            lasttitle = title
        if "<page>" in line:
            hitpage = True
            pagesinslice += 1
        if hitpage:
            slicesize += ulen(line)
            currentslice += line
        if ("</mediawiki>" in line) and (currentslice != "</mediawiki>\n"):
            with open(directory + "/" + directory + "_" + str(slicenumber) + ".xml", "w") as slice:
                slice.write(prepend + currentslice)
                print("Slice " + str(slicenumber) + ": Final slice")
        if "</page>" in line:
            if (slicesize > maxsize) or (pagesinslice >= maxpages):
                if slicesize > maxsize:
                    print("Slice " + str(slicenumber) + ": Split because of file size")
                elif pagesinslice >= maxpages:
                    print("Slice " + str(slicenumber) + ": Split because of number of pages")
                print("          - First page: " + firsttitle)
                print("          - Last page: " + lasttitle)
                print("") # line break
                firsttitle = ""
                with open(directory + "/" + directory + "_" + str(slicenumber) + ".xml", "w") as slice:
                    slice.write(prepend + currentslice + append)
                slicenumber += 1
                currentslice = ""
                slicesize = 0
                pagesinslice = 0
