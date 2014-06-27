#from distutils.core import setup
from setuptools import setup

descr = """cellom2tif: Convert Cellomics .C01 images to TIFF.

This package uses the python-bioformats library to traverse directories
and convert files in the Cellomics format (.C01) to TIFF files.
"""

DISTNAME            = 'cellom2tif'
DESCRIPTION         = 'Convert Cellomics images to TIFF.'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Juan Nunez-Iglesias'
MAINTAINER_EMAIL    = 'juan.n@unimelb.edu.au'
URL                 = 'https://github.com/jni/cellom2tif'
LICENSE             = 'BSD 3-clause'
DOWNLOAD_URL        = 'https://github.com/jni/cellom2tif'
VERSION             = '0.1'
PYTHON_VERSION      = (2, 7)
INST_DEPENDENCIES   = {} 


if __name__ == '__main__':

    setup(name=DISTNAME,
        version=VERSION,
        url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        license=LICENSE,
        packages=['cellom2tif'],
        install_requires=INST_DEPENDENCIES,
        scripts=["bin/cellom2tif"]
    )

