"""Windows compatibility shim for Unix resource module."""


def getpagesize() -> int:
    return 4096
