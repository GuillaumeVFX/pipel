@echo off

rem This will auto pull the repo and is destined to be run by windows task manager

git pull && ginol "NAD-Previz Repo was just pulled"


cd blog && git pull && ginol "NAD-Previz WPApp Repo was just pulled"
