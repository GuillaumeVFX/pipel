@echo off

set houdini_rel_root=Documents\houdini17.5
set home_dir_src=%userprofile%
set global_etc_path=%d%\etc
set pohm_etc=%pohm%\etc

rem "------------------------------"
rem Rarely should that be edited
rem BASHRC
set bashrc_src_fullpath=%home_dir_src%\.bashrc
set bashrc_global_etc_publish=%global_etc_path%\bashrc.%COMPUTERNAME%.txt
set bashrc_pohm_etc_publish=%pohm_etc%\bashrc.%COMPUTERNAME%.txt
rem HOUDINI
set houdini_env_source_full_path=%home_dir_src%\%houdini_rel_root%\houdini.env
set houdini_env_global_etc_publish=%global_etc_path%\houdini.env.%COMPUTERNAME%.txt
set houdini_env_pohm_etc_publish=%pohm_etc%\houdini.env.%COMPUTERNAME%.txt


rem DEBUG
set debug_file=%userprofile%\debug.txt
echo "copy %bashrc_src_fullpath% %bashrc_global_etc_publish% /y " >%debug_file%
echo "copy %bashrc_src_fullpath% %bashrc_pohm_etc_publish% /y" >>%debug_file%

echo "Publishing HOUDINI Env %houdini_env_source_full_path%">>%debug_file%
echo "copy %houdini_env_source_full_path% %houdini_env_global_etc_publish% /y">>%debug_file%
echo "copy %houdini_env_source_full_path% %houdini_env_pohm_etc_publish% /y">>%debug_file%

rem notepad %debug_file%

rem ENDDEBUG
rem This will auto pull the repo and is destined to be run by windows task manager

git pull 


cd blog && git pull 


rem "---------------publish common file to distributed system"
rem
echo " .bashrc of %COMPUTERNAME% is available on distributions for other config to inspire upgrade"
copy %bashrc_src_fullpath% %bashrc_global_etc_publish% /y
copy %bashrc_src_fullpath% %bashrc_pohm_etc_publish% /y

echo "Publishing HOUDINI Env %houdini_env_source_full_path%"
copy %houdini_env_source_full_path% %houdini_env_global_etc_publish% /y
copy %houdini_env_source_full_path% %houdini_env_pohm_etc_publish% /y


rem COMITTING CHANGES
cd %pohm_etc% &&  git commit . -m "published POHM ETC"


ginol "Hourly Workflows just ran"


pause

