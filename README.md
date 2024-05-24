# QR-Code Generator

## Project setup
```
pip install qrcode
pip install Pillow
pip install watchdog
pip install pyinstaller
pyinstaller --onefile --noconsole main.py // to create the .exe file
```

## Project description
This qr-code generator creates a folder on your desktop that can be used to drag and drop a .txt text file or an .url hyperlink into the folder.
After dropping the file into the folder the program will automatically detect the new file, create a matching qr-code on the desktop and delete the old file within the folder.
If the filetype is wrong, like f.e. an exe file, it gets moved out of the folder again, without changing the filetype.

