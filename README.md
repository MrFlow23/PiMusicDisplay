# PiMusicDisplay

PiMusicDisplay is a graphical application to show the information of a currently running music track from [mopidy](https://www.mopidy.com/) or [spotify-connect-web](https://github.com/Fornoth/spotify-connect-web) (a spotify connect client). It is optimised to run frameless on the official raspberry pi touch screen.
<br><br>
![alt text](https://raw.githubusercontent.com/mrflow23/pimusicdisplay/master/screenshot.png)

### Features

- optimised for a display resolution of 800x480
- show artist, album and track name
- show cover - retrieved from last.fm or spotify (to get covers from spotify an enhancement in spotify-connect-web is needed; I am going to add it in my fork soon)
- show play status (play/pause)
- show track time
- simple player control via on screen buttons (play, pause, skip)
- simple player control via ir-remote control (lirc)
- control display on/off state according to player status

### Requirements

- python 3
- required python packages: python3, python3-tk, python3-dbus, python3-pil, python3-pil.imagetk, xorg, lirc, python3-lirc (I hope that's all; if not, the console will tell you what is missing ;-)
- mopidy and/or spotify-connect-web (both connecting via their http api's)
- lirc for ir-remote control

### Running

- make settings in config.ini (at least activate the player you want to retrieve the track information from)
- run \_\_main__.py
- see also the attached script StartPiMusic.sh for remote start (ssh) and dpms (display) settings for the case you want PiMusicDisplay to control your display state

Thanks a lot to the mopidy community and Fornoth for spotify-connect-web.

Have fun
