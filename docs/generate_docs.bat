@echo off
echo Cleaning previous documentation...
if exist "html" rd /s /q "html"
if exist "latex" rd /s /q "latex"
if exist "processed_python" rd /s /q "processed_python"

echo Converting Ren'Py files to Python...
python convert_renpy.py

echo Generating Doxygen documentation...
doxygen Doxyfile

echo Done! Documentation generated in docs/html/
echo You can view it by opening docs/html/index.html in your browser.
pause 