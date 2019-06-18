cd ..
cd ..
cd virtenv
cd Scripts
call activate
cd ..
cd ..
cd gui\qt_designer_files
python -m PyQt5.uic.pyuic mirrorless_mirrors.ui -o main_gui_ui.py
pause