import os
import argparse
import sys

from ij import IJ
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


def convert_files(out_base, path, files):
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

    Returns
    -------
    None : Use for side effects only.

    Examples
    --------
    >>> in_dir = 'cellomics_files'
    >>> out_dir = 'tiff_files'
    >>> files = os.listdir(in_dir)
    >>> files
    ['image1.c01', 'image2.c02']
    >>> convert_files(out_dir, in_dir, files)
    >>> os.listdir(out_dir)
    ['image1.tif', 'image2.tif']
    """
    in_base, in_tail = split_top(path)
    out_path = os.path.join(out_base, in_tail)
    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    files = filter(lambda x: x.endswith('.C01'), files)
    for fn in files:
        fin = os.path.join(path, fn)
        print fin
        fout = os.path.join(out_path, fn)[:-4] + '.tif'
        print fout
        IJ.run('Bio-Formats (Windowless)', 'open=%s' % fin)
        IJ.saveAs('Tiff', fout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert a bunch of Cellomics .C01 files to TIFFs.')
    parser.add_argument('root_path', help='The path containing .C01 files')
    parser.add_argument('out_path', help='The path to output the TIFFs.')

    print sys.argv
    args = parser.parse_args()
    paths = os.walk(args.root_path)
    for path, dirs, files in paths:
        convert_files(path.replace(args.root_path, args.out_path), path,
                      files)
