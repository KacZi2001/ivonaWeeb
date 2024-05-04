#!/bin/bash

show_err() {
    echo
    echo "stdout:"
    cat ./tmp/stdout.txt
    echo
    echo "stderr:"
    cat ./tmp/stderr.txt
    exit 1
}

if [ -d ./tmp ]; then
  rm -r ./tmp
fi
mkdir ./tmp

type -P python3 >./tmp/stdout.txt 2>./tmp/stderr.txt && python_installed=1 && python_exec="python3"
type -P python >./tmp/stdout.txt 2>./tmp/stderr.txt && python_installed=1 && python_exec="python3"
type -P py3 >./tmp/stdout.txt 2>./tmp/stderr.txt && python_installed=1 && python_exec="python3"
type -P py >./tmp/stdout.txt 2>./tmp/stderr.txt && python_installed=1 && python_exec="python3"

if [ "$python_installed" = 1 ]; then
    echo "Python installation found."
else
    echo "Python is not installed."
    show_err
fi

"$python_exec" -c "import tkinter" >./tmp/stdout.txt 2>./tmp/stderr.txt && tkinter_installed=1

if [ -z "$tkinter_installed" ]; then
    echo "Tkinter is not installed."
    show_err
fi

type -P git >./tmp/stdout.txt 2>./tmp/stderr.txt && git_installed=1

if [ "$git_installed" = 1 ]; then
    echo "Pulling the newest version..."
    git pull >./tmp/stdout.txt 2>./tmp/stderr.txt && pulled=1
else
    echo "Git not found. Continuing without it."
fi

if [ -z "$pulled" ]; then
    echo "Couldn't pull the newest version."
fi

if [ -e venv/bin/activate ]; then
    venv_exist=1
else
    echo "Creating venv..."
    "$python_exec" -m venv venv >./tmp/stdout.txt 2>./tmp/stderr.txt && venv_exist=1
fi

if [ "$venv_exist" = 1 ]; then
    echo "Activating venv..."
    . venv/bin/activate
else
    echo "Couldn't create venv."
    show_err
fi

echo "Installing dependencies..."
"$python_exec" -m pip install -r requirements.txt >tmp/stdout.txt 2>tmp/stderr.txt && installed=1

if [ "$installed" = 1 ]; then
    echo "Running the program..."
    "$python_exec" main.py 2>tmp/stderr.txt && started=1
else
    echo "Couldn't install dependencies."
    show_err
fi

if [ -z "$started" ]; then
    echo "Couldn't run the program."
    show_err
fi

rm -r ./tmp