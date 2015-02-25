import os


def fn_has_ext(fn, ext, case_sensitive=False):
    """
    Determine whether a file has a particular extension.

    Parameters
    ----------
    fn : string
        The filename of the query file.
    ext : string
        The extension being checked.
    case_sensitive : bool
        Whether or not to treat the extension as case sensitive.

    Returns
    -------
    file_has_ext : bool
        True if the filename has the specified extension.
    """
    fn_ext = os.path.splitext(fn)[1][1:]
    if case_sensitive:
        file_has_ext = fn_ext == ext
    else:
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
    is_cellom = fn_has_ext(fn, 'C01') or fn_has_ext(fn, 'DIB')
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
    base_fn = os.path.splitext(fn)[0]
    is_mask = base_fn.endswith('o1') or base_fn.endswith('o1')
    return is_mask
