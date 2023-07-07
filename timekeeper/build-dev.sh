#! /usr/bin/bash
git clone https://github.com/gvtrindade/time-keeper.git
cd time-keeper/
git switch dev
cd ..
rm -rf timekeeper/
mv time-keeper/timekeeper/ ./
rm -rf time-keeper/
