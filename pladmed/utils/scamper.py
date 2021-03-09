import subprocess
import zlib
from tempfile import NamedTemporaryFile
import json
from jsonstream import loads

def run_scamper_cmd(content, cmd):
    tmpfile = NamedTemporaryFile()
    tmpfile.write(content)
    tmpfile.flush()

    res = subprocess.run(
        [
            cmd,
            tmpfile.name,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    tmpfile.close()

    return res.stdout.decode("utf-8")

def warts2json(content):
    res = run_scamper_cmd(content, "sc_warts2json")

    return list(loads(res))

def warts2dump(content):
    return run_scamper_cmd(content, "sc_analysis_dump")

def gzip2text(data):
    # 15 + 16 are binary flags which tell zlib to accept gzip data and reject zlib data
    # The byte array returned by the decompress function is decoded into an UTF-8 string.
    # This allows newlines and other control characters to be rendered correctly
    return zlib.decompress(data, 15 + 16).decode("utf-8")
