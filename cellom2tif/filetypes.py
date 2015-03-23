import os


def has_extension(filename, ext):
    """
    Determine whether a file has a particular extension.

    Parameters
    ----------
    filename : string
        The filename of the query file.
    ext : string
        The extension being checked.

    Returns
    -------
    file_has_ext : bool
        True if the filename has the specified extension.

    Examples
    --------
    >>> dib_file = 'AS_09125_050116110001_A01f00d0.DIB'
    >>> has_extension(dib_file, 'dib')
    True
    """
    fn_ext = os.path.splitext(filename)[1][1:]
    file_has_ext = fn_ext.lower() == ext.lower()
    return file_has_ext


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
    is_cellom = has_extension(fn, 'C01') or has_extension(fn, 'DIB')
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

    Examples
    --------
    >>> mask_fn = 'MFGTMP_120628160001_C18f00o1.C01'
    >>> is_cellomics_mask(mask_fn)
    True
    """
    base_fn = os.path.splitext(fn)[0]
    is_mask = base_fn.endswith('o1') or base_fn.endswith('o1')
    return is_mask
