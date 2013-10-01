import os
import argparse
import sys


from filetypes import is_cellomics_image, is_cellomics_mask


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


def convert_files(out_base, path, files, error_file=None, ignore_masks=False,
                  verbose=False):
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
    verbose : bool, optional
        If ``True``, print out diagnostic info during conversions.

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
    from jython_imports import IJ, BF, ImporterOptions
    if not os.path.isdir(out_base):
        os.makedirs(out_base)
    if error_file is None:
        ferr = sys.stdout
    else:
        error_file = os.path.join(out_base, error_file)
        ferr = open(error_file, 'w')
    files = filter(is_cellomics_image, files)
    if ignore_masks:
        files = filter(lambda fn: not is_cellomics_mask(fn), files)
    files = sorted(files)
    errors_found = False
    for fn in files:
        fin = os.path.join(path, fn)
        if verbose:
            print fin
        fout = os.path.join(out_base, fn)[:-4] + '.tif'
        opts = ImporterOptions()
        opts.setUngroupFiles(True)
        if not os.path.exists(fout):
            opts.setId(fin)
            try:
                imp = BF.openImagePlus(opts)[0]
            except:
                ferr.write(fin + '\n')
                ferr.flush()
                errors_found = True
            else:
                if verbose:
                    print "creating", fout
                IJ.saveAs(imp, 'Tiff', fout)
                imp.close()
        else:
            if verbose:
                print fout, "exists"
    if not errors_found and error_file is not None:
        ferr.close()
        os.remove(error_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert a bunch of Cellomics .C01 files to TIFFs.')
    parser.add_argument('root_path', help='The path containing .C01 files')
    parser.add_argument('out_path', help='The path to output the TIFFs.')
    parser.add_argument('-E', '--error-file', metavar='FILENAME',
                        help='Log problem filenames to the given filename.')
    parser.add_argument('-m', '--ignore-masks', action='store_true',
                        help='Ignore files ending in "o1.C01".')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print out runtime information.')

    args = parser.parse_args()
    paths = os.walk(args.root_path)
    for path, dirs, files in paths:
        convert_files(path.replace(args.root_path, args.out_path, 1), path,
                      files, args.error_file, args.ignore_masks, args.verbose)
