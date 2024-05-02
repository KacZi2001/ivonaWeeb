@echo off

mkdir tmp

python -V >NUL 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 set PYTHON=python && goto :check_venv
python3 >NUL 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 set PYTHON=python3 && goto :check_venv
py -V >NUL 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 set PYTHON=py && goto :check_venv
py3 -V >NUL 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 set PYTHON=py3 && goto :check_venv
echo Python is not installed
goto :show_error

:check_venv
echo Python installation found
if EXIST "venv\Scripts\python.exe" goto :activate_venv
echo Creating venv
%PYTHON% -m venv venv >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :activate_venv
echo Couldn't create venv
goto :show_error

:activate_venv
call venv/Scripts/activate.bat
echo Venv activated

:install
echo Installing dependencies
%PYTHON% -m pip install -r requirements.txt >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :run
echo Couldn't install dependencies
goto :show_error

:run
echo Dependencies installed
echo Running the program
%PYTHON% main.py 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto execution:
echo Couldn't run the program
goto :show_error

:show_error
echo.
echo stdout:
type tmp/stdout.txt
echo.
type tmp/stderr.txt

:execution
pause
rmdir /s /q tmp