#!/usr/bin/python3

from PyPDF4.pdf import PdfFileReader

from os.path import basename, join
from subprocess import Popen, PIPE
from shlex import split


global inkscape, pdftk
inkscape = None
pdftk = None

def which(program):
    return Popen(["which", program], stdout=PIPE).communicate()[0]

def getInkscape():
    global inkscape
    if inkscape is None:
        inkscape = which("inkscape")
    return inkscape

def getPDFtk():
    global pdftk
    if pdftk is None:
        pdftk = which("pdftk")
    return pdftk


#
# A class to allow import of a PDF
# and access to every page's DOM as SVG
#
def PDFReader(PdfFileReader):
    def __init__(self, filename=None, debug=False):
        self.debug = debug
        if filename != None:
            self.fromFile(filename)

    def fromFile(self, filename):
        self.filename = filename
        self.f = open(filename, "rb")
        PdfFileReader.__init__(self, self.f)
        # TODO: Use pypdf

    def __len__(self):
        return self.getNumPages()

    def getPageAsSVG(self, pageNumber):
        # TODO: Use pypdf, if possible
        #page = self.getPage(pageNumber)
        # TODO: yield SVGReader

        # Use pdftk to extract the requested page
        pdfpagename = join("/tmp", "{:s}_page{:d}.pdf".format(basename(self.filename)[:-4], pageNumber))
        Popen([getPDFtk(), self.filename, "cat", str(pageNumber), "output", pdfpagename]).wait()

        # Use inkscape to convert the page to SVG
        svgame = pdfpagename[:-4] + ".svg"
        Popen([getInkscape(), "--without-gui", "--export-plain-svg="+svgname, pdfpagename]).wait()
        os.remove(pdfpagename)

        # Import the SVG
        svg = SVGReader(filename=svgname)
        os.remove(svgname)

        return svg
