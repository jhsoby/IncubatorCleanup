#!/usr/bin/python3.6
# -*- coding: utf-8  -*-
"""
Clean up a Wikimedia Incubator project before importing it to the new home wiki.

usage:
    python3 cleaner.py prefix XMLfilename.xml [--notranslate --wiktionary]
"""

from argparse import ArgumentParser
import re, urllib.request, json

strings = {
    "exception_filename": "ERROR: The filename (given as \"%s\") needs to have a three- or four-letter extension (typically .xml).",
    "exception_pagename": "ERROR: The title in line %d would start with a space or a colon after the prefix is stripped. Remove the space or colon from the <title> tag, but make sure this won't lead to duplicate pagenames. If the page is a redirect, you can just remove the entire <page> object from the export file, and run the script again.\n\n%s                  ^",
    "warning_prefix": "WARNING: The prefix (%s) is still present in the following lines in the export file. This is probably due to human error, such as editors omitting the slash after the prefix or incorrect wiki syntax. But just to be safe, you should check a few of them to see if it is something you need to fix by hand.\n\n"
    }

parser = ArgumentParser()
parser.add_argument("prefix",nargs=1,help="the prefix used by the test wiki")
parser.add_argument("XMLfile",nargs=1,help="the name of the exported XML file")
parser.add_argument("--notranslate",action="store_true",
    help="use if namespaces should not be translated (not recommended)")
parser.add_argument("--wiktionary",action="store_true",
    help="use if the project separates between cases in initial letters of pagenames")
args = parser.parse_args()

wiktionary = args.wiktionary
namespaces = {}
if not args.notranslate:
    urlmap = {
        "wp": "wikipedia",
        "wb": "wikibooks",
        "wn": "wikinews",
        "wq": "wikiquote",
        "wy": "wikivoyage",
        "wt": "wiktionary"
    }
    with urllib.request.urlopen("https://" + args.prefix[0].lower().split("/")[1] + "." + urlmap[args.prefix[0].lower().split("/")[0]] + ".org/w/api.php?action=query&meta=siteinfo&siprop=namespaces&format=json") as url:
        data = json.loads(url.read().decode())["query"]["namespaces"]
        for ns in data:
            if not ns == "0":
                namespaces[data[ns]["canonical"]] = data[ns]["*"]
            if ns == "6":
                namespaces["Image"] = data[ns]["*"]

file = args.XMLfile[0]
resultfile = re.sub(r'\.(\w{3,4})', r'.ready.\1', file)
if file == resultfile:
    raise Exception(strings["exception_filename"] % file)
open(resultfile, "w").close()
prefix = args.prefix[0]
prefix = "[" + prefix[0].upper() + prefix[0].lower() + "]" + prefix[1:]

def cleanup_incubator(text):
    # Remove all instances of the prefix (including /)
    text = re.sub(r" *(?i:" + prefix + r")/", "", text)
    if not wiktionary:
        # Turn [[Abc|abc]] into [[abc]]
        text = re.sub(r"\[\[ *((?i:\w))(.*?) *\| *((?i:\1)\2)\ *\]\]", r"[[\3]]", text)
        # Turn [[Abc|abcdef]] into [[abc]]def
        text = re.sub(r"\[\[ *((?i:\w))(.*?) *\| *((?i:\1)\2)(\w+) *\]\]", r"[[\3]]\4", text)
    else:
        # Turn [[abc|abc]] into [[abc]]
        text = re.sub(r"\[\[ *(.*?) *\| *\1 *\]\]", r"[[\1]]", text)
        # Turn [[abc|abcdef]] into [[abc]]def
        text = re.sub(r"\[\[ *(.*?) *\| *\1(\w+) *\]\]", r"[[\1]]\2", text)
    # Remove the base category
    text = re.sub(r"\n?\[\[ *[Cc]ategory *: *" + prefix + ".*?\]\]", "", text)
    # Remove {{PAGENAME}} category sortkeys, and one-letter-only sortkeys
    text = re.sub(r"\[\[ *[Cc]ategory *: *(.+?)\|{{(SUB)?PAGENAME}} *\]\]", r"[[Category:\1]]", text)
    text = re.sub(r"\[\[ *[Cc]ategory *: *(.+?)\|\w *\]\]", r"[[Category:\1]]", text)
    # Translate namespaces
    for key in namespaces:
        key_reg = "[" + key[0].upper() + key[0].lower() + "]" + key[1:]
        text = re.sub(r"\[\[ *" + key_reg + " *: *([^\|\]])", r"[[" + namespaces[key] + r":\1", text)
    return text

with open(file, "r", encoding="utf-8") as origin, open(resultfile, "a", encoding="utf-8") as output:
    linenumber = 0
    lines_with_prefix = []
    for line in origin:
        linenumber += 1
        resultline = cleanup_incubator(line)
        if re.search(prefix, resultline, flags=re.IGNORECASE):
            lines_with_prefix.append(str(linenumber))
        if re.search(r"<title>[: ]", resultline):
            raise Exception(strings["exception_pagename"] % (linenumber, line))
        if resultline == "\n" and line != "\n":
            continue
        else:
            output.write(resultline)
    if len(lines_with_prefix) != 0:
        print(strings["warning_prefix"] % prefix + ", ".join(lines_with_prefix))
