@echo off

if EXIST tmp rmdir /s /q tmp
mkdir tmp

python -V >NUL 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 set PYTHON=python && goto :check_git
python3 >NUL 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 set PYTHON=python3 && goto :check_git
py -V >NUL 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 set PYTHON=py && goto :check_git
py3 -V >NUL 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 set PYTHON=py3 && goto :check_git
echo Python is not installed.
goto :show_error

:check_git
echo Python installation found.
git -v >NUL 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :pull_newest
echo Git not found. Continuing without it.
goto :check_venv

:pull_newest
echo Pulling the newest version...
git pull >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :check_venv
echo Couldn't pull the newest version.
echo.
echo stdout:
type tmp/stdout.txt
echo.
type tmp/stderr.txt

:check_venv
if EXIST "venv\Scripts\python.exe" goto :activate_venv
echo Creating venv...
%PYTHON% -m venv venv >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :activate_venv
echo Couldn't create venv.
goto :show_error

:activate_venv
echo Activating venv...
call venv/Scripts/activate.bat

:install
echo Installing dependencies...
%PYTHON% -m pip install -r requirements.txt >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :run
echo Couldn't install dependencies.
goto :show_error

:run
echo Running the program...
%PYTHON% main.py 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto execution:
echo Couldn't run the program.
goto :show_error

:show_error
echo.
echo stdout:
type tmp/stdout.txt
echo.
type tmp/stderr.txt
pause

:execution
rmdir /s /q tmp