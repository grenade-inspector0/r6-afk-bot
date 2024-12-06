"""Compiles the application"""

import os
import time
import shutil
import pathlib
import PyInstaller.__main__ as pyinstaller

os.system("cls")
ROOT_DIR = pathlib.Path(__file__).parent.resolve()
SRC_DIR = ROOT_DIR / "src"
ICON_PATH = ROOT_DIR / "assets" / "AFK_Bot.ico"

def compile_main(name, source):
    pyinstaller.run([
        f"--name={name}",
        '--onefile',
        '--console',
        '--clean',
        '--add-data=assets/messages.txt;assets',
        f'--icon={str(ICON_PATH)}',
        str(source),
    ])

while True:
    answer = input("Would you also like to compile the craptop version of the file? (Y/N)\n> ").lower()
    if answer in ["y", "n"]:
        compile_craptop = answer == "y"
        break
    else:
        print("Respond with y/n...")
        time.sleep(3)
        continue

exe_files = {
    "R6_AFK.exe": ROOT_DIR / "R6_AFK.exe",
    "R6_AFK_Craptops.exe": ROOT_DIR / "R6_AFK_Craptops.exe"
}

for exe_name, target_path in exe_files.items():
    if target_path.exists():
        target_path.unlink()

compile_main("R6_AFK", os.path.join(SRC_DIR, "main.py"))

if compile_craptop:
    temp_main = SRC_DIR / "main_temp.py"
    with open(SRC_DIR / "main.py", 'r') as file:
        lines = file.readlines()

    with open(temp_main, 'w') as file:
        for line in lines:
            if line.strip().startswith("CRAPTOP ="):
                file.write("CRAPTOP = True\n")
            else:
                file.write(line)
    compile_main("R6_AFK_Craptops", temp_main)
    temp_main.unlink()

os.system("cls")
for root, dirs, files in os.walk(ROOT_DIR):
    for dir_name in dirs:
        if dir_name == '__pycache__':
            shutil.rmtree(os.path.join(root, dir_name))
    for file_name in files:
        if file_name.endswith(('.pyc', '.pyo')):
            os.remove(os.path.join(root, file_name))

build_dir = ROOT_DIR / "build"
if build_dir.exists():
    shutil.rmtree(build_dir)

spec_files = [ROOT_DIR / "R6_AFK.spec", ROOT_DIR / "R6_AFK_Craptops.spec"]
for spec_file in spec_files:
    if spec_file.exists():
        spec_file.unlink()

dist_dir = ROOT_DIR / "dist"
exe_files = {
    "R6_AFK.exe": ROOT_DIR / "R6_AFK.exe",
    "R6_AFK_Craptops.exe": ROOT_DIR / "R6_AFK_Craptops.exe"
}
for exe_name, target_path in exe_files.items():
    exe_file = dist_dir / exe_name
    if exe_file.exists():
        shutil.move(str(exe_file), str(target_path))

if dist_dir.exists():
    shutil.rmtree(dist_dir)

temp_main = SRC_DIR / "main_temp.py"
if temp_main.exists():
    temp_main.unlink()
