import os
import argparse
import sys

from ij import IJ
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
#import WindowManager


def split_top(path):
    """Like `os.path.split`, but splitting from the topmost directory.

    Parameters
    ----------
    path : string
        The path to be split.

    Returns
    -------
    (head, tail) : string tuple
        The topmost directory in path (`head`) and the rest of the path
        (`tail`).

    Examples
    --------
    >>> path = '/path/to/some/files'
    >>> split_top(path)
    ('/path', 'to/some/files')
    """
    split = os.path.split
    tails = []
    head = path
    tail = ''
    while len(head) != 0 and head != '/':
        head, tail = split(head)
        tails.append(tail)
    if head == '/':
        tails.append(head)
    tails.reverse()
    head = tails[0]
    if len(tails[1:]) > 0:
        tail = os.path.join(*tails[1:])
    else:
        tail = ''
    return head, tail


def is_cellomics_image(fn):
    """Determine whether a file is a Cellomics image.

    Parameters
    ----------
    fn : string
        The filename of the file in question.

    Returns
    -------
    is_cellom : bool
        True if the filename points to a Cellomics image.
    """
    is_cellom = fn.endswith('.C01') or fn.endswith('.c01')
    return is_cellom


def is_cellomics_mask(fn):
    """Determine whether a file is a Cellomics mask image.

    Parameters
    ----------
    fn : string
        The filename.

    Returns
    -------
    is_mask : bool
        True if the filename points to a Cellomics mask image.
    """
    is_mask = x.endswith('o1.C01') or x.endswith('o1.c01')
    return is_mask


def convert_files(out_base, path, files, error_file=None, ignore_masks=False):
    """Convert cellomics .C01 files to TIFF files in a sibling directory.

    This function is designed to be used with `os.walk`.

    Parameters
    ----------
    out_base : string
        The name of the sibling directory in which to place converted files.
    path : string
        The path to the files to be converted.
    files : list of string
        The filenames of files, including non-.C01 files.
    error_file : string, optional
        A file to which to log "corrupted" images.
    ignore_masks : bool, optional
        Ignore files ending in "o1.C01".

    Returns
    -------
    None : Use for side effects only.

    Examples
    --------
    >>> in_dir = 'cellomics_files'
    >>> out_dir = 'tiff_files'
    >>> files = os.listdir(in_dir)
    >>> files
    ['image1.c01', 'image2.c01']
    >>> convert_files(out_dir, in_dir, files)
    >>> os.listdir(out_dir)
    ['image1.tif', 'image2.tif']
    """
    in_base, in_tail = split_top(path)
    out_path = os.path.join(out_base, in_tail)
    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    if error_file is None:
        ferr = sys.stdout
    else:
        ferr = open(os.path.join(out_base, error_file), 'w')
    files = filter(is_cellomics_image, files)
    if ignore_masks:
        files = filter(lambda fn: not is_cellomics_mask(fn), files)
    files = sorted(files)
    for fn in files:
        fin = os.path.join(path, fn)
        print fin
        fout = os.path.join(out_path, fn)[:-4] + '.tif'
        opts = ImporterOptions()
        opts.setUngroupFiles(True)
        if not os.path.exists(fout):
            opts.setId(fin)
            try:
                imp = BF.openImagePlus(opts)[0]
            except:
                ferr.write(fin + '\n')
                ferr.flush()
            else:
                print "creating", fout
                IJ.saveAs(imp, 'Tiff', fout)
                imp.close()
        else:
            print fout, "exists"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert a bunch of Cellomics .C01 files to TIFFs.')
    parser.add_argument('root_path', help='The path containing .C01 files')
    parser.add_argument('out_path', help='The path to output the TIFFs.')
    parser.add_argument('-E', '--error-file', metavar='FILENAME',
                        help='Log problem filenames to the given filename.')
    parser.add_argument('-m', '--ignore-masks', action='store_true',
                        help='Ignore files ending in "o1.C01".')

    print sys.argv
    args = parser.parse_args()
    paths = os.walk(args.root_path)
    for path, dirs, files in paths:
        convert_files(path.replace(args.root_path, args.out_path), path,
                      files, args.error_file, args.ignore_masks)
