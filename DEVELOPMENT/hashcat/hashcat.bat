@echo off
set original_dir="%CD%"
cd "G:\TFG-CODIGO\maskcat\hashcat"
hashcat.exe %*
cd "%original_dir%"
