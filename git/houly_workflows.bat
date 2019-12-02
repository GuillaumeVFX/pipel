@echo off

rem This will auto pull the repo and is destined to be run by windows task manager

git pull 


cd blog && git pull 


rem "---------------publish common file to distributed system"
rem
rem " .bashrc of Gaia is available on distributions for other config to inspire upgrade"
copy %userprofile%\.bashrc %d%\etc\gaia_bashrc /y
copy %userprofile%\.bashrc %pohm%\bashrc.gaia.txt /y



ginol "Hourly Workflows just ran"
