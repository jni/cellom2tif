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
    is_mask = fn.endswith('o1.C01') or fn.endswith('o1.c01')
    return is_mask


