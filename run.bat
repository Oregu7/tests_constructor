@echo off
for /f "tokens=2" %%a in ('netsh interface ipv4 show addresses^|find "IP-"') do set LocIP=%%a& Goto extNetsh
:extNetsh
start http://%LocIP%:8000
echo http://%LocIP%:8000 > tests_url.txt
python manage.py runserver 0.0.0.0:8000