"""FileNotReadable Exception"""


class FileNotReadableError(Exception):
    """return a file not readable exception"""

    def __init__(self, classname: str, filename: str):
        super().__init__(F"{classname}: {filename} not readable")
