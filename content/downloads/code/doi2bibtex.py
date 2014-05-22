#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# doi2bibtex.py
#
# purpose:  Fetch bibtex references using the Digital Object Identifier DOI
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.github.io/python4oceanographers
# created:  26-Jul-2008
# modified: Thu 27 Mar 2014 03:06:23 PM BRT
#
# obs: Very messy script!
#

import re
import sys
import httplib2
import argparse
from urllib import request, parse

from gscholar import query
from bs4 import BeautifulSoup


def parse_args(arglist):
    """Parse options with argparse."""
    usage = """\nUsage: %(prog)s doinumber > ref.bib\n
    e.g.: %(prog)s -m ADS "10.1016/j.ocemod.2003.12.003" """

    description = "Search bibtex reference using the doi"

    parser = argparse.ArgumentParser(usage=usage,
                                     description=description)
    parser.add_argument('positional',
                        metavar='doi',
                        help='e.g.: "10.1016/j.ocemod.2003.12.003"')
    parser.add_argument('-v', '--verbose',
                        dest="verbose",
                        default=False,
                        action="store_true",
                        help="increase verbosity, default=False")

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-m', '--method',
                       dest='method',
                       type=str,
                       default='CrossRef',
                       help="ADS, PANGAEA, GSCHOLAR, and CrossRef.")

    args = parser.parse_args()

    return args


def search_doi(text):
    """Return a list with doi numbers found in a text.
    stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
    TODO: This is unfinished. I want to scrap a pdftotext output from a paper
    and get all DOIs found.
    """
    dval = re.compile(r'10.(\d)+/(\S)+')
    # Good for web scrapping
    dval = re.compile(r'(10.(\d)+/([^(\s\>\"\<)])+)')
    doi = dval.findall(dval)
    return doi


class Bibtex(object):
    """ Convert doi number to bibtex entries."""
    def __init__(self, doi=None, title=None):
        """
        Input doi number ou title (actually any text/keyword.)
        Returns doi, encoded doi, and doi url or just the title.
        """
        _base_url = "http://dx.doi.org/"
        self.doi = doi
        self.title = title
        self.bibtex = None
        if doi:
            self._edoi = parse.quote(doi)
            self.url = _base_url + self._edoi  # Encoded doi.
        else:
            self.url = None

    def validate_doi(self):
        """Validate doi number and return the url."""
        # TODO: urllib2 does not redirect all possible doi(s).
        # once I figure out why I'll eliminate httplib2.
        h = httplib2.Http()
        h.request(self.url, "GET")
        req = httplib2.Http()
        try:
            self.header, self.html = req.request(self.url, "GET")
            self.paper_url = self.header['content-location']
            return self.paper_url
        except Exception as e:
            print("Could not resolve doi url at: %s \n" % self.url)
            print('Error: %s\n' % str(e))
            return None

    def _soupfy(self, url):
        """Returns a soup object."""
        html = request.urlopen(url).read()
        self.soup = BeautifulSoup(html)
        return self.soup

    def getCrossRef(self):
        """Turn DOIs into formatted citation by making a request
        "text/bibliography" content type.
        http://www.crossref.org/CrossTech/
        2011/11/turning_dois_into_formatted_ci.html
        """
        def format_bibtext(bibtext):
            """Quick-and-dirty formatting function."""

        headers = dict(Accept='text/bibliography; style=bibtex')
        req = request.Request(self.url, headers=headers)
        self.bibtex = request.urlopen(req).read().decode('utf-8')
        return self.bibtex

    def getADS(self):
        """Get bibtex entry from doi using ADS database."""
        uri = "http://adsabs.harvard.edu/cgi-bin/basic_connect?qsearch="
        url = uri + self._edoi

        # Make soup and look for ADS bibcode.
        soup = self._soupfy(url)
        try:
            tag = soup.findAll('input', attrs={"name": "bibcode"})[0]
        except IndexError:
            print("\nADS failed\n")
        else:
            bibcode = tag.get('value') if tag.get('value') else None
            uri = 'http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode='
            end = '&data_type=BIBTEX&db_key=AST%26nocookieset=1'
            url = uri + bibcode + end
            bib = request.urlopen(url).read().decode('utf-8')
            # Remove empty lines and query info.
            bib = bib.split('\n')
            self.bibtex = '\n'.join(bib[5:-1])
        finally:
            return self.bibtex

    def getPANGAEA(self):
        """Get bibtex entry from doi using PANGEA database
        doi example: 10.1594/PANGAEA.726855."""
        uri = "http://doi.pangaea.de"
        url = uri + "/{}?format=citation_bibtex".format(self._edoi)
        self.bibtex = request.urlopen(url).read().decode('utf-8')
        return self.bibtex

    def getGScholar(self):
        """If you are feeling lucky."""
        bibtex = query(self.doi, 4)[0]
        self.bibtex = bibtex.decode('utf-8')
        return self.bibtex


def main(argv=None):
    """TODO: unittest with several doi searches."""
    if argv is None:
        argv = sys.argv

    args = parse_args(argv[1:])

    doi = args.positional
    method = args.method

    def allfailed():
        """All failed message+google try."""
        bold, reset = "\033[1m", "\033[0;0m"
        bib.getGScholar()
        # FIXME: Has no meaning when using title
        url = bold + bib.url + reset
        msg = """Unable to resolve this DOI using database
        \nTry opening, \n\t{0}\nand download it manually.
        \n...or if you are lucky check the Google Scholar search below:
        \n{1}
        """.format(url, bib.bibtex)
        return msg

    # Create the bib object.
    bib = Bibtex(doi=doi)

    # Forces PANGAE if doi has the string? Or suggest it?
    if (method == "PANGAEA") or ("PANGAEA" in doi):
        print("\nPANGAEA\n")
        bib.getPANGAEA()
    elif method == "ADS":
        print("\nADS\n")
        bib.getADS()
    elif method == "GSCHOLAR":
        print("\nGSCHOLAR\n")
        bib.getGScholar()
    elif method == "CrossRef":
        print("\nCrossRef\n")
        bib.getCrossRef()
    else:
        print("Unrecognized method.")

    # Check if successful and print bibtex.
    if bib.bibtex:
        print(bib.bibtex)
    else:
        print(allfailed())

if __name__ == '__main__':
    sys.exit(main(sys.argv))

    if False:
        # ADS:
        doi = "10.1175/1520-0426(1993)010<0041:MTPOAA>2.0.CO;2"
        bib = Bibtex(doi)
        print(bib.getADS())

        # ADS Fails:
        doi = "10.1109/JOE.2007.895277"
        bib = Bibtex(doi)
        print(bib.getADS())

        # PANGAEA:
        doi = "10.1594/PANGAEA.726855"
        bib = Bibtex(doi)
        print(bib.getPANGAEA())

        # GSCHOLAR:
        doi = "10.1109/JOE.2007.895277"
        bib = Bibtex(doi)
        print(bib.getGScholar())

        # CrossRef:
        doi = "10.1590/S1679-87592011000100002"
        doi = "10.1109/JOE.2007.895277"
        bib = Bibtex(doi)
        print(bib.getCrossRef())

        # Title query test (GSCHOLAR and ADS):
        title = "Correlation scales, objective mapping, and absolute "
        title += "geostrophic flow in the California Current"
        bib = Bibtex(title)
        print(bib.getGScholar())
        print(bib.getADS())
