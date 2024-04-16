"""Compiles the application and duplicates all requiered file to the dist folder."""

import os
import pathlib
import PyInstaller.__main__ as pyinstaller
DIRECTORY = pathlib.Path(__file__).parent.resolve()

# compile exe
pyinstaller.run([
            "--name= R6 AFK",
            '--onefile',
            # '--windowed',
            # '--icon=%s' % 'icon.ico',
            '--clean',
            # '--uac-admin',
            '--console',
            os.path.join(DIRECTORY, 'src/main.py'),
        ])

# cleanup
os.system("pyclean .")

# copy assets
os.system(f'robocopy "{os.path.join(DIRECTORY, "assets/images")}" \
    "{os.path.join(DIRECTORY, "dist/assets/images")}" /COPYALL /E')
os.system(f'robocopy "{os.path.join(DIRECTORY, "assets/movements")}"  \
"{os.path.join(DIRECTORY, "dist/assets/movements")}" /COPYALL /E')
