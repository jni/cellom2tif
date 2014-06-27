"""cellom2tif package: functions to convert Cellomics images to TIFF.
"""
from cellom2tif import read_image, convert_files
from filetypes import is_cellomics_image, is_cellomics_mask

__all__ = ['read_image', 'convert_files',
           'is_cellomics_image', 'is_cellomics_mask']
