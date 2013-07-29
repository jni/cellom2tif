import os
import argparse
import sys

from filetypes import is_cellomics_image, is_cellomics_mask


class open_write(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if value == '-':
            setattr(namespace, self.dest, sys.stdout)
        else:
            try:
                fout = open(value, 'w')
            except IOError:
                print 'Could not open file %s, falling back on stdout.' % value
                setattr(namespace, self.dest, sys.stdout)
            else:
                setattr(namespace, self.dest, fout)


def missed_conversions(in_dir, out_dir, ignore_masks=False):
    """Check that each cellomics .C01 file has a corresponding TIFF file.

    This function is designed to be used with `os.walk`.

    Parameters
    ----------
    out_base : string
        The name of the sibling directory in which to place converted files.
    path : string
        The path to the files to be converted.
    files : list of string
        The filenames of files, including non-.C01 files.
    ignore_masks : bool, optional
        Ignore files ending in "o1.C01".

    Returns
    -------
    missed : list of string
        A list of filenames in their original location that were not
        converted.

    Examples
    --------
    >>> in_dir = 'cellomics_files'
    >>> out_dir = 'tiff_files'
    >>> files = os.listdir(in_dir)
    >>> files
    ['image1.c01', 'image2.c01']
    >>> out_files = os.listdir(out_dir)
    >>> out_files
    ['image1.tif']
    >>> missed_conversions(in_dir, out_dir)
    ['cellomics_files/image2.c01']
    """
    in_paths = os.walk(in_dir)
    out_paths = os.walk(out_dir)
    missed = []
    for ((in_path, _, in_files), (_, _, out_files)) in \
                                                    zip(in_paths, out_paths):
        in_files = filter(is_cellomics_image, in_files)
        if ignore_masks:
            in_files = filter(lambda fn: not is_cellomics_mask(fn), in_files)
        in_files = sorted(in_files)
        out_files = set(out_files)
        for infn in in_files:
            outfn = infn[:-4] + '.tif'
            if outfn not in out_files:
                missed.append(os.path.join(in_path, infn))
    return missed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert a bunch of Cellomics .C01 files to TIFFs.')
    parser.add_argument('root_path', help='The path containing .C01 files')
    parser.add_argument('out_path', help='The path to output the TIFFs.')
    parser.add_argument('-m', '--ignore-masks', action='store_true',
                        help='Ignore files ending in "o1.C01".')
    parser.add_argument('-o', '--output-file', dest='fout', action=open_write,
                        default=sys.stdout,
                        help='Write output to this file, or stdout if not ' +
                        'provided. Caution: will overwrite existing files.')

    args = parser.parse_args()
    missed = missed_conversions(args.root_path, args.out_path,
                                args.ignore_masks)
    for fn in missed:
        args.fout.write(fn+'\n')

