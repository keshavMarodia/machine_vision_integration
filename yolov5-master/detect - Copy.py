import os
import subprocess

subprocess.run(f"python detect.py --weights {'best.pt'} --source {'Test/620.jpg'}")

import detect

print(detect.x1,detect.y1,detect.x2,detect.y2)