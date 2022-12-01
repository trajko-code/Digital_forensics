This folder contains Qt Designer .ui files.

To export .ui file to Python classes use pyuic5 command:

    pyuic5 -x file.ui -o file.py

After exporting, the manually added/changed code in the same .py script from ui/ dir needs to be also added in the newly generated file.py script.