#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 mupdf

import sys
import os
import tempfile
import xml.etree.ElementTree as ET
import subprocess
import json

def go(root):
    for line in root.iter('line'):
        for font in line.iter('font'):
            bbox = tuple(map(float, line.attrib['bbox'].split()))
            s = ''.join([char.attrib['c'] for char in font])
            yield (s, bbox)

def pdfxml(pdfname):
    with tempfile.TemporaryDirectory() as tmpdirname:
        out = os.path.join(tmpdirname, 'out.xml')
        subprocess.run(["mutool", "convert", "-F", "stext", "-o", out, pdfname], check=True)
        with open(out, 'r') as f:
            return f.read()

if __name__ == '__main__':
    pdfname = sys.argv[1]
    json.dump(list(go(ET.fromstring(pdfxml(pdfname)))), sys.stdout)
