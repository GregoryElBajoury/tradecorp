import os
import sys
import pytest

# Ajout de la racine du projet et du dossier src au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

if __name__ == "__main__":
    exit_code = pytest.main(["/home/jovyan/tests", "-v"])
    sys.exit(exit_code)