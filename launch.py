# ALTERNATIVE APP LAUNCHER

import os
from pathlib import Path
from src.main import main

root = Path(__file__).resolve().parent
os.chdir(root)

if __name__ == "__main__":
    main()