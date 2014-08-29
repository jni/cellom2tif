from cellom2tif import cellom2tif

def test_start():
    cellom2tif.start()
    assert cellom2tif.VM_STARTED
