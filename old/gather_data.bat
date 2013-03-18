@ECHO OFF
SET DJANGO_SETTINGS_MODULE=weathersite.settings
SET OLD_PWD=%CD%
SET TIMEOUT=900
SET SAMPLES=96

for /L %%n in (1,1,%SAMPLES%) DO (
echo Gathering data...
REM CD /D %~dp0
python sensor_data_gatherer.py
REM CD /D %OLD_PWD%
echo Done.
timeout /T %TIMEOUT% /NOBREAK
)

