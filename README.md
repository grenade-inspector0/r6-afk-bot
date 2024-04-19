# Quick Start
- Download and extract the .zip folder from releases.
- Double click the r6 afk.exe to run it.
- Press F2 to start and stop.

# Usage
This application is for afk botting Tom Clancy's Rainbow Six: Siege. The main purpose is to farm levels and renown, or to improve reputation (yes, improve).
It currently will get your reputation to 'disruptive' (the second lowest), with no text/voice abuse or friendly fire and a maxed out griefing bar.
Griefing currently has no in-game penalties, unlike the others, so it's useful for clearing out your penalties without actually having to play the game.

Should work with any 16:9 resolution. Won't work on ultra-wide monitors.

It looks on the screen for in-game buttons, namely buttons to start queue or find another game. It compares the images in the 'assets' folder with regions of the screen.
It clicks 'ok' on pop-ups, like the common 'connection to server failed' lmao. It also commends teammates when the game ends.
It presses '5' repeatedly to not get kicked for inactivity. I have plans to add movement later, but for now that's all it does.
It won't send keypresses if "Rainbow Six" isn't the current window, so you can safely alt-tab around with the bot running, and if the game crashes, it won't
do anything with other open applications or the desktop.

You can either run the compiled exe in releases, or you can download the source code, install python and the necessary packages.
Run afk.py if you choose to use the source code.

Press F2 to start/stop the bot.

# Configuration
The bot generates a config.json file when first run. You can open this with any text editor (notepad works).
Later I will add more here, but for now, it has the following:
    spam_link - this can be "true" or "false". "false" (default) disables text chat. "true" enables posting a link in text chat every once in awhile.
    link - the bot will post this text in all chat if spam_link is true. default "youtube.com/verybannable".
    link_delay - how often to post the text, in seconds. default 300 (5 minutes).

It loads these on start, so if you don't want to use the defaults, run the bot once to generate the file, close it, edit the file, and run the program again.
You should disable link spamming or increase the link_delay if it increases your text chat abuse. I haven't had an issue with the default 300 seconds.
You can set the link to your own channel, or some other text you like. Or you can leave it on my channel and help me out.

# Disclaimer
If you get banned, it's your fault. Get owned. Loser. 

# SUBSCRIBE ALREADY
youtube.com/verybannable