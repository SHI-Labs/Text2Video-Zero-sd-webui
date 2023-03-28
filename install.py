import os
import sys

debug = False
try:
    from modules import shared
    is_auto = True
except:
    pass

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if debug:
    print(f"Base dir (auto1111) is: {base_dir} from {__file__}")
ext_dir = os.path.join(base_dir, 'extensions', 'Text2Video-Zero-sd-webui')

if ext_dir not in sys.path:
    if debug:
        print(f"Appending (install): {ext_dir}")
    sys.path.insert(0, ext_dir)
else:
    if debug:
        print(f"Ext dir already in path? {ext_dir}")
        print(sys.path)

import subprocess
import launch

launch.run_pip(f"install -r \"{os.path.join(ext_dir, 'requirements.txt')}\"", "requirements for Text2Video-Zero")
