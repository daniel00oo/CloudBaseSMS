@echo off
set result=false
if "%1"=="help" (set result=true)

if "%result%"=="true" (python receive.py "help") else (python receive.py %1 %2 %3 > log.txt | echo "----Press <ctr> + <c> to exit----")