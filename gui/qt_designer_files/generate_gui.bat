cd ..
cd ..
virtenv/Scripts/activate.bat
cd gui/qt_designer_files
python -m PyQt5.uic.pyuic mirrorless_mirrors.ui -o ../main_gui.py
deactivate