## About This Repository
This repository contains a Python script that can be used to clean up exported
XML files for projects that are ready to be imported from
[Wikimedia Incubator](https://incubator.wikimedia.org/) to their permanent
wikis.

## Usage
Download this repository (or, if you want, just the file `IncubatorCleanup.py`,
that's all you'll really need). The file is run with two obligatory arguments
and two optional arguments:

* `prefix` needs to be the prefix used by the pages on the Wikimedia Incubator.
So for a Wikipedia in Esperanto, the prefix would be `Wp/eo`.
* `XMLfile` is the filename of the XML file you got when you exported all the
contents from the test wiki on the Incubator.
* (optional) `--wiktionary` is used if pagenames on the wiki will be
case-sensitive. On Wikipedias, [[This]] and [[this]] will link to the same page,
but on Wiktionaries, they will be different pages. This also applies to any
other non-Wiktionary wikis with the `$wgCapitalLinks` option set to false, such
as the Wikipedias in [Lojban](https//jbo.wikipedia.org) or
[Sakizaya](https://szy.wikipedia.org/).
* (optional) `--notranslate` will *not* translate namespace names (such as
Category:, Talk:, File:, etc) into the target language, instead keeping them
in English (which is the interface language on Incubator). If the wiki you're
running the script for has not yet been created, you will have to use this, as
the script fetches the namespace names from the wiki's API, which will not work
if the wiki doesn't exist yet.

For a Wikipedia in Esperanto you would run the script like this:

`python3 IncubatorCleanup.py Wp/eo EsperantoWikipedia.xml`

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
present in the resulting XML file. This normally happens because of human error,
like if an editor has omitted an / or the prefix is not properly inside a link
or a template (e.g. if someone has put one too few square brackets around a
link). The script will print the lines where this occurs, so you can go over the
exported XML file and check to see what was the cause of these errors, save, and
run the script again.

## Test cases
In this repository there is a file named `testcases.txt`, that you can run the
script on to see what happens. The testcases file does not test for the errors
mentioned above, but tests various other replacements that will be made.

Run the script with the test case file like this:

`python3 IncubatorCleanup.py Wp/ru testcases.txt`

Then review the resulting file `testcases-READY.txt`. You should also try it
with the optional parameters to see what the differences are.
