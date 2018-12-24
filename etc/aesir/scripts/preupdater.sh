#!/usr/bin/env bash

echo >> /tmp/aesirupdater/log
rm -f /tmp/aesirupdater/logfile.txt
touch /tmp/aesirupdater/logfile.txt

cp -r /etc/aesir/updater /tmp/aesirupdater
python3 /tmp/aesirupdater/updater/aesirUpdater.py


