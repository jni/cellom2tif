import os
import argparse
import shutil

from . import tifffile as tif
import javabridge as jv
import bioformats as bf

from .filetypes import is_cellomics_image, is_cellomics_mask


VM_STARTED = False
VM_KILLED = False


def start(max_heap_size='8G'):
    """Start the Java Virtual Machine, enabling bioformats IO.

    Parameters
    ----------
    max_heap_size : string, optional
        The maximum memory usage by the virtual machine. Valid strings
        include '256M', '64k', and '2G'. Expect to need a lot.
    """
    jv.start_vm([], class_path=bf.JARS, max_heap_size=max_heap_size)
    global VM_STARTED
    VM_STARTED = True


def done():
    """Kill the JVM. Once killed, it cannot be restarted.

    Notes
    -----
    See the python-javabridge documentation for more information.
    """
    jv.kill_vm()
    global VM_KILLED
    VM_KILLED = True


def read_image(filelike):
    """Read an image volume from a file.

    Parameters
    ----------
    filelike : string or bf.ImageReader
        Either a filename containing a BioFormats image, or a
        `bioformats.ImageReader`.

    Returns
    -------
    image : numpy ndarray, 5 dimensions
        The read image.
    """
    if not VM_STARTED:
        start()
    if VM_KILLED:
        raise RuntimeError("The Java Virtual Machine has already been "
                           "killed, and cannot be restarted. See the "
                           "python-javabridge documentation for more "
                           "information. You must restart your program "
                           "and try again.")
    if isinstance(filelike, bf.ImageReader):
        rdr = filelike
    else:
        rdr = bf.ImageReader(filelike)
    image = rdr.read(rescale=False)
    return image


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
    >>> path = 'path/to/some/files'
    >>> split_top(path)
    ('path', 'to/some/files')
    >>> path = '/root/path'
    >>> split_top(path)
    ('/', 'root/path')
    >>> path = 'file'
    >>> split_top(path)
    ('file', '')
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


def convert_files(out_base, path, files, ignore_masks=False, verbose=False):
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
    ignore_masks : bool, optional
        Ignore files ending in "o1.C01".
    verbose : bool, optional
        If ``True``, print out diagnostic info during conversions.

    Returns
    -------
    None : Use for side effects only.

    Examples
    --------
    >>> in_dir = 'tests/cellomics_files'
    >>> out_dir = 'tests/all_tiff_files'
    >>> files = sorted(os.listdir(in_dir))
    >>> files
    ['image1.c01', 'image2.c01']
    >>> convert_files(out_dir, in_dir, files)
    >>> sorted(os.listdir(out_dir))
    ['image1.tif', 'image2.tif']
    >>> convert_files(out_dir, in_dir, files, verbose=True) # print files
    tests/cellomics_files/image1.c01
    ('tests/all_tiff_files/image1.tif', 'exists')
    tests/cellomics_files/image2.c01
    ('tests/all_tiff_files/image2.tif', 'exists')
    >>> shutil.rmtree(out_dir, ignore_errors=True) # cleanup after doctest
    """
    if not os.path.isdir(out_base):
        os.makedirs(out_base)
    files = filter(is_cellomics_image, files)
    if ignore_masks:
        files = filter(lambda fn: not is_cellomics_mask(fn), files)
    files = sorted(files)
    for fn in files:
        fin = os.path.join(path, fn)
        if verbose:
            print(fin)
        fout = os.path.join(out_base, fn)[:-4] + '.tif'
        if not os.path.exists(fout):
            im = read_image(fin)
            tif.imsave(fout, im)
        else:
            if verbose:
                print(fout, "exists")


def main():
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
                      files, args.ignore_masks, args.verbose)
    done()


if __name__ == '__main__':
    main()
