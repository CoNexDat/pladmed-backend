import subprocess
import zlib
from tempfile import NamedTemporaryFile


def warts2text(content):
    tmpfile = NamedTemporaryFile()
    tmpfile.write(content)
    tmpfile.flush()

    res = subprocess.run(
        [
            "sc_warts2text",
            tmpfile.name,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    tmpfile.close()

    return res.stdout.decode("utf-8")


def gzip2text(data):
    # 15 + 16 are binary flags which tell zlib to accept gzip data and reject zlib data
    # The byte array returned by the decompress function is decoded into an UTF-8 string.
    # This allows newlines and other control characters to be rendered correctly
    return zlib.decompress(data, 15 + 16).decode("utf-8")
