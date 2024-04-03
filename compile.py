import PyInstaller.__main__ as pyinstaller
import os
import subprocess
import pathlib
DIRECTORY = pathlib.Path(__file__).parent.resolve()

# compile exe
pyinstaller.run([
            '--name=%s' % "r6 afk",
            '--onefile',
            # '--windowed',
            # '--icon=%s' % 'icon.ico',
            '--clean',
            # '--uac-admin',
            '--console',
            os.path.join(DIRECTORY, 'src/afk.py'),
        ])

#
os.system("pyclean .")

# copy assets
os.system(f'robocopy "{os.path.join(DIRECTORY, "assets/images")}"  "{os.path.join(DIRECTORY, "dist/assets/images")}" /COPYALL /E')