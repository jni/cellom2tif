cellom2tif
==========

Fiji Jython script to convert Cellomics .C01 files to TIFF.

# Dependencies

Needs to be run through [Fiji](http://fiji.sc), not the Python interpreter.

# Usage

Be sure to download Fiji and update it (it will prompt to update upon
launch). Then:

```
/path/to/fiji /path/to/cellom2tif/cellom2tif.py path/to/c01/files output/path
```

On Mac OS X, the Fiji executable is usually at:

```
/Applications/Fiji.app/Contents/MacOS/fiji-macosx
```

On Linux, it's

```
$DOWNLOAD_DIR/Fiji.app/ImageJ-linux64
```

# Licenses

`argparse.py` is distributed under the [Python Software Foundation License](
http://opensource.org/licenses/Python-2.0).

The rest of the project is distributed under the [3-clause BSD license](
http://opensource.org/licenses/BSD-3-Clause)

# Author

Juan Nunez-Iglesias (juan.n@unimelb.edu.au), inspired by a Fiji macro from
Cameron Nowell (cameron.nowell@wehi.edu.au).

# Thanks

Albert Cardona (cardonaa@janelia.hhmi.org).

