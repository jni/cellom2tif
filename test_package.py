#!/bin/env python

import os
import sys
import subprocess as sp
import shutil
from datetime import datetime as dt

import numpy as np
import pytest

# Below: switch between Mahotas and scikit-image for IO.
from skimage import io
# import mahotas as io

# Some constants
test_data_dir = 'test-data'
test_output_dir = 'test-data-out'
test_results_dir = 'test-data-results'
test_output_mask_dir = 'test-data-out-m'
test_results_mask_dir = 'test-data-results-m'


@pytest.fixture
def outdir(request):
    # clear output of previous tests, if present
    shutil.rmtree(test_output_dir, ignore_errors=True)
    shutil.rmtree(test_output_mask_dir, ignore_errors=True)
    # create file for error printing
    now = dt.strftime(dt.now(), '%Y-%m-%d-%H-%M-%S')
    fout = open('test-output-%s.txt' % now, 'w')
    def cleanup():
        shutil.rmtree(test_output_dir, ignore_errors=True)
        shutil.rmtree(test_output_mask_dir, ignore_errors=True)
        # delete fout only if empty
        fout.close()
        if os.path.exists(fout.name) and os.path.getsize(fout.name) == 0:
            os.remove(fout.name)
    request.addfinalizer(cleanup)
    return fout


def find_errors(out_dir, res_dir, ignore_masks=False):
    """Check that each output .tif file matches its reference output.

    Parameters
    ----------
    out_dir, res_dir : string
        The name of the root directories containing input, output,
        and expected results.
    ignore_masks : bool, optional
        Ignore files ending in "o1.C01".

    Returns
    -------
    missed : list of string
        A list of filenames that have no equivalent in the output being
        tested.
    not_equal : list of string
        A list of filenames in which the output image and the reference
        image don't match.
    """
    out_paths = os.walk(out_dir)
    res_paths = os.walk(res_dir)
    missed = []
    not_equal = []
    files_counted = 0
    for ((res_path, _, res_files), (out_path, _, out_files)) in \
                                        zip(res_paths, out_paths):
        res_files = filter(lambda fn: fn.endswith('.tif'), res_files)
        res_files = sorted(res_files)
        out_files = set(out_files)
        for resfn in res_files:
            files_counted += 1
            reference_file = os.path.join(res_path, resfn)
            if resfn not in out_files:
                missed.append(reference_file)
            else:
                out_im = io.imread(os.path.join(out_path, resfn))
                res_im = io.imread(reference_file)
                percent_off = (out_im - res_im).astype(np.float) / res_im.max()
                if np.any(np.abs(percent_off) > 0.01):
                    not_equal.append(reference_file)
    return missed, not_equal


def print_errors(missing, not_equal, fout=sys.stdout):
    if len(missing) > 0 or len(not_equal) > 0:
        fout.write('# Missed files:')
        for fn in missing:
            fout.write('  ' + fn + '\n')
        fout.write('# Images do not match:')
        for fn in not_equal:
            fout.write('  ' + fn + '\n')


def test_runtime_ignore_masks(outdir):
    call = ['python', 'bin/cellom2tif']
    flags = ['-m']
    indirs = [test_data_dir, test_output_mask_dir]
    resdir = test_results_mask_dir
    cmd_line = call + flags + indirs
    sp.call(cmd_line, shell=False)
    missing, not_equal = find_errors(indirs[1], resdir, ignore_masks=True)
    assert len(missing) == 0
    assert len(not_equal) == 0


def test_runtime(outdir):
    call = ['python', 'bin/cellom2tif']
    indirs = [test_data_dir, test_output_dir]
    resdir = test_results_dir
    cmd_line = call + indirs
    sp.call(cmd_line, shell=False)
    missing, not_equal = find_errors(indirs[1], resdir, ignore_masks=True)
    assert len(missing) == 0
    assert len(not_equal) == 0
