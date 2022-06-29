@echo off
set original_dir="%CD%"
cd [Path donde se encuentra Hashcat]
hashcat.exe %*
cd "%original_dir%"