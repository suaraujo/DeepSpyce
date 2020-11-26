def getsize(f):
    # Copiado de https://stackoverflow.com/questions/4677433
    pos = f.tell()
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(pos)
    return size

def test_getsize():

    os_getsize = os.path.getsize("archivo_raw")

    with open("archivo_raw", "rb") as fp:
        my_getsize = deepspyce.getsize(fp)
    
    assert my_getsize == os_getsize
