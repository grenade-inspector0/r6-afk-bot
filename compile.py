"""Compiles the application and duplicates all requiered file to the dist folder."""

import os
import shutil
import pathlib
import PyInstaller.__main__ as pyinstaller

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
SRC_DIR = ROOT_DIR / "src"
ASSETS_DIR = ROOT_DIR / "assets/tesseract"
DIST_ASSETS_DIR = ROOT_DIR / "dist/assets/tesseract"
ICON_PATH = ROOT_DIR / "assets" / "AFK_Bot.ico"

pyinstaller.run([
    "--name=R6 AFK",
    '--onefile',
    '--console',
    '--clean',
     f'--icon={ICON_PATH}',
    os.path.join(SRC_DIR, 'main.py'),
])

def clean(directory):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))
        for file_name in files:
            if file_name.endswith(('.pyc', '.pyo')):
                os.remove(os.path.join(root, file_name))
    
    build_dir = ROOT_DIR / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir)

    spec_file = ROOT_DIR / "R6 AFK.spec"
    if spec_file.exists():
        spec_file.unlink()

    dist_dir = ROOT_DIR / "dist"
    exe_file = dist_dir / "R6 AFK.exe"
    if exe_file.exists():
        shutil.move(str(exe_file), ROOT_DIR / "R6 AFK.exe")
    
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

clean(ROOT_DIR)

if os.name == 'nt':
    os.system(f'robocopy "{ASSETS_DIR}" "{DIST_ASSETS_DIR}" /COPYALL /E')
else:
    os.makedirs(DIST_ASSETS_DIR, exist_ok=True)
    os.system(f'cp -r "{ASSETS_DIR}/." "{DIST_ASSETS_DIR}"')

os.system("cls")

