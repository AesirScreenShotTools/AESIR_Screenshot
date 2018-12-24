#!/bin/bash


# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
exec > >(tee -i /tmp/aesirupdater/logfile.txt)

# Without this, only stdout would be captured - i.e. your
# log file would not contain any error messages.
# SEE (and upvote) the answer by Adam Spiers, which keeps STDERR
# as a separate stream - I did not want to steal from him by simply
# adding his answer to mine.
exec 2>&1

echo "prepare" > /tmp/aesirupdater/log
echo "Checking super user rights!"
if [ "$EUID" -ne 0 ]
  then echo "error" > /tmp/aesirupdater/log
  exit
fi

if ! [ -x "$(command -v wget)" ]; then
  echo 'Error: wget is not installed.' >&2
  echo 'trying to install wget using apt'
  apt install wget -y
  echo "download" > /tmp/aesirupdater/log
  exit 1
fi


echo "download" > /tmp/aesirupdater/log

cd /tmp
mkdir aesirupdater
wget https://github.com/AesirScreenShotTools/packages/raw/master/aesir.deb
echo "uninstall" > /tmp/aesirupdater/log
apt-get remove aesir-ss -y
echo "install" > /tmp/aesirupdater/log
apt-get install /tmp/aesirupdater/aesir.deb -y
echo "success" > /tmp/aesirupdater/log

chmod 444 /tmp/aesirupdater/logfile.txt
exit


