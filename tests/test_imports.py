def test_import_paths():
    from convolens.utils import paths

    assert paths.ROOT_DIR.exists()
    assert paths.DATA_DIR.exists()