cellom2tif
==========

Python script to convert Cellomics .C01 files to TIFF.

Read the BioFormats [report card for Cellomics
files](https://www.openmicroscopy.org/site/support/bio-formats5/formats/cellomics.html).
In short: it's not a great format. So you might as well convert all your
Cellomics files to TIFF and forget about them forever. Software developers
will thank you.


# Continuous integration

Cellom2tif uses Travis-CI and Coveralls for continuous integration:

[![Build Status](https://travis-ci.org/jni/cellom2tif.svg?branch=master)](https://travis-ci.org/jni/cellom2tif)
[![Coverage Status](https://img.shields.io/coveralls/jni/cellom2tif.svg)](https://coveralls.io/r/jni/cellom2tif)

# Dependencies

Uses [python-bioformats](http://pythonhosted.org/python-bioformats) and
[javabridge](http://pythonhosted.org/javabridge) to perform the conversion.

- numpy >= 1.6
- javabridge >= 1.0.3
- python-bioformats >= 1.0.3

Note that (much of) Python BioFormats is GPL-licensed (v2). All the code
in cellom2tif is BSD-licensed (3-clause), *except where it is forbidden by the
GPL* by the import of Python BioFormats.  Consult your lawyer.
(I don't have one.)

# Usage

```
$ cellom2tif -h
usage: cellom2tif [-h] [-E FILENAME] [-m] [-v] root_path out_path

Convert a bunch of Cellomics .C01 files to TIFFs.

positional arguments:
  root_path             The path containing .C01 files
  out_path              The path to output the TIFFs.

optional arguments:
  -h, --help            show this help message and exit
  -E FILENAME, --error-file FILENAME
                        Log problem filenames to the given filename.
  -m, --ignore-masks    Ignore files ending in "o1.C01".
  -v, --verbose         Print out runtime information.
```

Note that weird behavior may occur when the input and output directories are
the same, or subdirectories of one another, since the script recurses down
subdirectories and recreates the subdirectory structure in the output path.

# Licenses

Christoph Gohlke's excellent
[tifffile.py](http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html) is included
for easy writing of TIFF files, and is itself BSD-licensed (3-clause).

As noted above (Dependencies), cellom2tif is BSD-licensed (where possible), and
GPLv2-licensed (where required).

# Author

Juan Nunez-Iglesias (juan.n@unimelb.edu.au).
