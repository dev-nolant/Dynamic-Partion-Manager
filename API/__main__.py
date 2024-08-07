# __main__.py
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

import API.api as api

if __name__ == "__main__":
    api.app.run(debug=True)
