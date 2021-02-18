import subprocess
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
