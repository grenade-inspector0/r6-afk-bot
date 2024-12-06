# Quick Start
- Download and extract the .zip folder from releases.
- Double click the r6 afk.exe to run it.
- Press F2 to start and stop.

# Usage
This application is for afk botting Tom Clancy's Rainbow Six: Siege. The main purpose is to farm levels and renown, or to improve reputation (yes, improve).
It currently will get your reputation to exemplary (Highest reputation level), with no text/voice abuse or friendly fire, so it's useful for clearing out your penalties without actually having to play the game.

Requirements:
- Change these settings (In Settings -> Display):
  - Turn HUD Display Area to 100
  - Turn Menu Display Area to 100
- Download the [latest tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki "Latest Tesseract Installer") and do the following:
  - Click INSTALL FOR ONLY ME when asked if you want to installl for anyone on this pc or just you.
  - Make sure to install to the default directory. (Looks something like C:\Users\YOUR_USER\AppData\Local\Programs\Tesseract-OCR)
- Make sure to ALWAYS keep a monitor plugged into the pc you're AFKing on.
  - The montior can be turned off, however it needs to be plugged into the pc. This is due to how Python's Pillow module takes screenshots.
  - Virtual Displays may work, but I haven't had any success with them.

Won't work on ultra-wide monitors.

You can either run the compiled exe in releases, or you can download the source code, install python and the necessary packages.
Run main.py if you choose to use the source code.

Press F2 to start/stop the bot.

# How Does it Work?
It screenshots specific regions of your screen, then converts that screenshot to text, and finally it compares that text to keywords that are different depending on the region. After that it does certain actions based upon the state detected, such as when in a game it will randomly move the mouse and press a random amount of the WASD keys, of which, none will repeat to ensure you don't get kicked for inactivity.

Some other benefits:
- It clicks 'ok' on pop-ups, like the common 'connection to server failed' lmao.
- It will improve your positive reputation points, which in theory, should let you teamkill more often and lead to less 2-day toxic behavior suspensions.
- It won't send keypresses if "Rainbow Six" isn't the current window, so you can safely alt-tab around with the bot running, and if the game crashes, it won't
do anything with other open applications or the desktop.

# Credits 
Made By :
- Verybannable (youtube.com/verybannable)
  - [Original Repository](https://github.com/VeryBannable/r6-scraping-afk "Original Repository")

Edited By : 
- Grenade Inspector 

# SUBSCRIBE ALREADY
youtube.com/verybannable

# Disclaimer
If you get banned, it's your fault. Get owned. Loser. 
