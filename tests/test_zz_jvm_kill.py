from cellom2tif import cellom2tif
import bioformats as bf
import pytest


cfile = 'test-data/d1/MFGTMP_120628160001_C18f00d0.C01'


def test_read_image():
    im = cellom2tif.read_image(cfile)
    assert im.shape == (512, 512)


def test_read_image_from_reader():
    rdr = bf.ImageReader(cfile)
    im = cellom2tif.read_image(rdr)
    assert im.shape == (512, 512)


def test_done():
    cellom2tif.done()
    assert cellom2tif.VM_KILLED


def test_vm_killed_error():
    cellom2tif.done()
    with pytest.raises(RuntimeError) as err:
        cellom2tif.read_image(cfile)
    assert err.value.message.startswith('The Java Virtual Machine')
