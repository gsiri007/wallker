#!/usr/bin/env bash

rm -r ./build
rm -r ./dist
rm ./wallker.spec

pyinstaller --onefile --noconsole  --hidden-import='PIL._tkinter_finder' --name wallker main.py
