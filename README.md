## About This Repository
This repository contains a Python script that can be used to clean up exported
XML files for projects that are ready to be imported from Wikimedia Incubator
to their permanent wikis.

## Usage
Download this repository (or, if you want, just the file `IncubatorCleanup.py`,
that's all you'll really need). The file is run with two obligatory arguments,
namely `prefix` and `XMLfile`, and the optional (but recommended!) argument
`--translatens`.

The `prefix` needs to be the prefix used by the pages on the Wikimedia
Incubator. So for a Wikipedia in Esperanto, the prefix would be `Wp/eo`.

The `XMLfile` is the filename of the XML file you got when you exported all the
contents from the test wiki on the Incubator.

The optional (but recommended) `--translatens` translates all namespaces names
(such as Category:, Talk:, File:, etc) into the target language instead of
keeping them in English (which is the interface language on Incubator). **This
parameter will only work if the wiki has already been created.**

For a Wikipedia in Esperanto you would run the script like this:

`python3 IncubatorCleanup.py Wp/eo EsperantoWikipedia.xml --translatens`

And, assuming no errors, the resulting file will be named
`EsperantoWikipedia-READY.xml`.

Once you are finished, you should use a diff tool such as
[Meld](http://meldmerge.org/) to compare the two files to make sure that
everything looks good.

### Errors and warnings
The script will throw errors in two cases:

1. If the filename given doesn't have a three- or four-letter extension. This is
because the output filename would be malformed.
2. If, after the prefix is stripped, a pagename in the XML file would be
invalid or potentially cause duplicate pagenames. This is the case if the
pagename starts with a colon or a space (which can happen if there is a prefix
present, but can't happen if there is no prefix). The solution to this is to
(1) check in the XML file would be a duplicate (do a search for the resulting
pagename without the colon or space), and then (2a) remove the page from the XML
file in case it is a redirect or (2b) remove the offending characters in case
there are no pagename conflicts.

Additionally, the script will **print a warning** in case the prefix is still
present in the resulting XML file. This normally happens because of human error.
The editor of a revision has omitted a /, or they have written the prefix with
more CAPTITAL LETTERS than they should. The script will print the lines where
this occurs, so you can go over the exported XML file and check to see what was
the cause of these errors, save, and run the script again.

## Test cases
In this repository there is a file named `testcases.txt`, that you can run the
script on to see what happens. The testcases file does not test for the errors
mentioned above, but tests various other replacements that will be made.

Run the script with the test case file like this:

`python3 IncubatorCleanup.py Xx/und testcases.txt`

Then review the resulting file `testcases-READY.txt`.

## Caveats
The script is currently not optimized for use for wikis where `$wgCapitalLinks`
is false. This includes all Wiktionaries, and any projects in the Lojban
language.
