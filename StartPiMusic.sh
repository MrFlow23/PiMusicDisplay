# for remote start / x-server setting
export DISPLAY=:0.0
# initialise x-server
xinit -- -nocursor &
sleep 3
# deactivate os display state and backlight control (will be controlled by PiMusicDisplay)
xset s noblank
xset s off
xset dpms 0 0 0
# start PiMusicDisplay in backround and write log file
/usr/bin/python3 -u __main__.py &> PiMusic.log &
